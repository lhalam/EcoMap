import os
from datetime import timedelta
from flask.ext.login import UserMixin, LoginManager, login_user, logout_user, login_required
import jinja2
import logging

from flask import Flask, render_template, request, redirect, jsonify, session, url_for
from flask.ext.wtf import Form
from flask_wtf import Form
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import Required, Length, DataRequired
from flask.ext.bootstrap import Bootstrap
from itsdangerous import URLSafeTimedSerializer

from ecomap.pool_final import pool_obj, retry
from ecomap.utils import get_logger

app = Flask(__name__)
# app.config['APPLICATION_ROOT'] = '/home/padalko/ss_projects/Lv-164.UI/ecomap'
# app.config['SECRET_KEY'] = 'topsecret!'
app.secret_key = "topsecret!"
bootstrap = Bootstrap(app)
lm = LoginManager(app)
lm.login_view = 'login_templ'

login_serializer = URLSafeTimedSerializer(app.secret_key)
app.config["REMEMBER_COOKIE_DURATION"] = timedelta(days=14)

class MyForm(Form):
    name = StringField('name', validators=[DataRequired()])


class NameForm(Form):
    name = StringField('Enter value', validators=[Length(min=2, max=25),
                                                  DataRequired()])
    textfield = StringField('additional test field', validators=[Length(max=20), DataRequired()])
    submit = SubmitField('Submit')


@app.route('/')
def index(name='start', name2='def_page'):
    return render_template('base.html', name=name, secname=name2)


@app.route('/index')
def index_ecomap(name='start', name2='def_page'):
    return render_template('index.html', name=name, secname=name2)


@app.route('/page1')
@login_required
def page1():
    name = 'Flask Config'
    config = app.config
    return render_template('page1.html', name=name, conf=config)


@app.route('/page2')
def page2(name=None, name2="Default"):
    name = 'SERVER ENVIRON variables'
    environ = os.environ
    return render_template('page2.html', name=name, env=environ)


@app.route('/users/<var>')
def test(var):
    # name = 'petro'
    name2 = 'pool_obj._db_name'
    return render_template('page1.html', name=var, secname=name2)


@app.route('/form', methods=['GET', 'POST'])
def form():
    name = None
    if request.method == 'POST' and 'name' in request.form:
        name = request.form['name']
    return render_template('form.html', name=name)


@app.route('/advancedForm', methods=['GET', 'POST'])
def advancedForm():
    name = None
    test_text = None
    form = NameForm()
    # app.logger.warning('form', form)
    print 'formdata', form.data
    print 'formname', form.name
    # app.logger.warning('formsubmit', form.submit)
    # app.logger.warning('ERRORS', form.SECRET_KEY)
    print app.config['SECRET_KEY']
    if form.validate_on_submit():  # invoke here a submitting
        name = form.name.data
        test_text = form.textfield.data
        form.name.data = ''  # cleaning up placeholder
        form.textfield.data = ''
        app.logger.info('*!*!*!*!*!**!*!*!*!*!*!**!*!')
    return render_template('adv_form.html', form=form, name=name, text=test_text)


@app.errorhandler(404)
def not_found(e):
    return render_template('404.html')


@app.route('/db', methods=['GET', 'POST'])
def db(sql=None, initial=None):
    if request.method == 'POST' and 'sql_query' in request.form:
        sql = request.form['sql_query']
        initial = request.form['sql_query']
        with pool_obj.manager() as conn:
            q1 = conn['connection'].cursor()
            q1.execute(sql)
            sql = q1.fetchall()
    return render_template('sql.html', sql_query=sql, basic=initial)

# Log-in methods start here
class User(UserMixin):
    """
    basic model for working with user data in sessions.
    duplicating sql table
    """
    def __init__(self, id, first_name, last_name, email, password):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password

    def __repr__(self):
        return '<User name:%s lastname:%s email:%s>' % (self.first_name, self.last_name, self.email)

    def set_password(self, password):
        """
        method needed for generate unique pasword hash to store in db.
        uses built-in flask function
        :param password: clean password
        :return:
        """
        self.password = generate_password_hash(password)

    def verify_password(self, password):
        """
        method for checking and comparing passwords from db and login form
        :param password:
        :return:
        """
        return check_password_hash(self.password, password)

    def get_auth_token(self):
        """
        encode a secure token for cookie
        :return:
        """
        data = [str(self.id), self.password]
        app.logger.warning('DATATATATA %s' %data)
        return login_serializer.dumps(data)

    @staticmethod
    def get(userid):
        """
        method for checking existing users in db by unique email field
        :param userid: unique user identifier (email field)
        :return: User object if user exists in db or None
        """
        with pool_obj.manager() as conn:
            q1 = conn['connection'].cursor()
            try:
                q1.execute('select * from user where email="%s";' % userid)
                db_userid = q1.fetchone()
                app.logger.warning('log from GET USER')
                return User(db_userid[0], db_userid[1], db_userid[2], db_userid[3], db_userid[4])
            except:
                return None

    @staticmethod
    def get_user_by_id(userid):
        """
        method needed by flask-loging load_manager.
        it checks user's id before each request.
        :param userid:
        :return: User Object
        """
        with pool_obj.manager() as conn:
            q1 = conn['connection'].cursor()
            try:
                q1.execute('select * from user where id="%s";' % userid)
                db_userid = q1.fetchone()
                app.logger.warning('log from get_user by ID')
                app.logger.warning(User(db_userid[0], db_userid[1], db_userid[2], db_userid[3], db_userid[4]))
                return User(db_userid[0], db_userid[1], db_userid[2], db_userid[3], db_userid[4])
            except:
                return None

def register_user(firstname, lastname, mail, password):
    """
    :param firstname:
    :param lastname:
    :param mail:
    :param password:
    :return:
    """
    hash_password = generate_password_hash(password)
    with pool_obj.manager() as conn:
        q1 = conn['connection'].cursor()
        q1.execute('INSERT INTO user (first_name, last_name, email, password) VALUES ("%s", "%s", "%s", "%s");'
                   % (firstname, lastname, mail, hash_password))
        conn['connection'].commit()


@lm.user_loader
def load_user(id):
    return User.get_user_by_id(id)


@lm.token_loader
def load_token(token):
    """
    Flask-Login token_loader callback.
    The token_loader function asks this function to take the token that was
    stored on the users computer process it to check if its valid and then
    return a User Object if its valid or None if its not valid.
    """
    max_age = app.config["REMEMBER_COOKIE_DURATION"].total_seconds()
    app.logger.warning('max_age !!!!!!!!!!!!!!!!!!!!!!!! %s' ) % max_age
    data = login_serializer.loads(token, max_age=max_age)
    app.logger.warning('token_loader DATA %s' % data)
    user = User.get_user_by_id(data[0])
    app.logger.warning(user)
    app.logger.warning('data[1] %s' % data[1])
    app.logger.warning('user.pasword %s' % user.password)
    if user and data[1] == user.password:
        return user
    return None



# def check_user(mail, password):
#     with pool_obj.manager() as conn:
#         q1 = conn['connection'].cursor()
#         try:
#             q1.execute('select password from user where email="%s";' % mail)
#             db_user_password = q1.fetchone()
#             app.logger.info(db_user_password[0])
#             app.logger.info(password)
#             if check_password_hash(db_user_password[0], password):
#                 return True
#         except:
#             return False
#
#
# def is_user_exist(mail):
#     with pool_obj.manager() as conn:
#         q1 = conn['connection'].cursor()
#         try:
#             q1.execute('select email from user where email="%s";' % mail)
#             db_user = q1.fetchone()
#             if db_user:
#                 return True
#         except:
#             return False




# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         app.logger.debug('request %s' % request)  # <Request 'http://ecomap.new:81/login' [POST]>
#         app.logger.debug('req data %s' % request.data)  # {"email":"vadime.padalko@gmail.com","password":"666664"}
#         app.logger.debug('req json %s' % request.json)  # {u'password': u'666664', u'email': u'vadime.padalko@gmail.com'}
#         user_mail = request.json['email']
#         user_pass = request.json["password"]
#         if check_user(user_mail, user_pass):
#             app.logger.info('can login')
#             status = 'checked, log in'
#             # session['user'] = user_mail
#             print User.get(user_mail)
#         else:
#             status = 'no user in db or wrong paswd, cannot login'
#         return jsonify({'check_user': status, 'paswd': user_pass, 'umail': user_mail})
#     return jsonify({'method': 'GET'})\


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        app.logger.debug('request %s' % request)  # <Request 'http://ecomap.new:81/login' [POST]>
        app.logger.debug('req data %s' % request.data)  # {"email":"vadime.padalko@gmail.com","password":"666664"}
        app.logger.debug('req json %s' % request.json)  # {u'password': u'666664', u'email': u'vadime.padalko@gmail.com'}
        user_mail = request.json['email']
        user_pass = request.json["password"]
        user = User.get(user_mail)
        if user is None or not user.verify_password(user_pass):
            status = 'no user in db or wrong paswd, cannot login'
            return jsonify({'login_status': status, 'email': user_mail})
        login_user(user, remember=True)
        status = 'user checked, logged in'
        return jsonify({
            'login_status': status,
            'password': user.password,
            'email': user.email,
            'firstname': user.first_name,
            'lastname': user.last_name,
            'id': user.id,
            'token': user.get_auth_token()
        })
    return jsonify({'method': 'GET'})


@app.route('/logout', methods=['GET', 'POST'])
# @login_required
def logout():
    logout_user()
    status = 'logged out'
    return jsonify({'check_user': status})


# @app.route('/register', methods=['GET', 'POST'])
# def register():
#     if request.method == 'POST':
#         app.logger.info(request.json)
#         user_firstname = request.json['firstname']
#         user_lastname = request.json["lastname"]
#         user_mail = request.json['email']
#         user_pass = request.json["password"]
#         if not User.get(user_mail):
#             register_user(user_firstname, user_lastname, user_mail, user_pass)
#             status = 'added %s %s' % (user_firstname, user_lastname)
#         else:
#             status = 'user with this email is already exists'
#         return jsonify({'status': status})


def create_user(json):
    with pool_obj.manager() as conn:
        cur = conn['connection'].cursor()
        cur.execute('INSERT INTO user (first_name, last_name, email, password)'
            'VALUES ("%s", "%s", "%s", "%s");' % (json['firstname'], json['lastname'], json['email'], json['password']))
        conn['connection'].commit()


@app.route('/register', methods=['GET', 'POST'])
def register():
    json = request.json
    app.logger.debug(json)
    create_user(json)
    return jsonify(request.json)


#FLASK TEMPLATE VERSION!
class LoginForm(Form):
    username = StringField('Username', validators=[DataRequired(), Length(1, 30)])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Submit')


@app.route('/login_templ', methods=['GET', 'POST'])
def login_templ():
    form = LoginForm()
    if form.validate_on_submit():
        user_mail = form.username.data
        app.logger.warning(user_mail)
        user = User.get(user_mail)
        if user is None or not user.verify_password(form.password.data):
            return redirect(url_for('login_templ', **request.args))
        login_user(user, form.remember_me.data)
        return redirect(request.args.get('next') or url_for('index'))
    return render_template('login.html', form=form)


@app.route('/logout_templ', methods=['GET', 'POST'])
@login_required
def logout_templ():
    logout_user()
    return redirect(url_for('index'))


class RegisterForm(Form):
    firstname = StringField('firstname', validators=[Length(min=2), DataRequired()])
    lastname = StringField('lastname', validators=[Length(min=2), DataRequired()])
    email = StringField('email', validators=[Length(min=2), DataRequired()])
    password = PasswordField('password', validators=[Length(max=20), DataRequired()])
    submit = SubmitField('Submit')


@app.route('/register_templ', methods=['GET', 'POST'])
def register_templ():
    user_firstname = None
    status = None
    # user_lastname = None
    # user_mail = None
    # user_pass = None
    form = RegisterForm()
    if form.validate_on_submit():
        user_firstname = form.firstname.data
        user_lastname = form.lastname.data
        user_mail = form.email.data
        user_pass = form.password.data
        form.firstname.data = ''
        form.lastname.data = ''
        form.email.data = ''
        form.password.data = ''
        if not User.get(user_mail):
            register_user(user_firstname, user_lastname, user_mail, user_pass)
            status = 'User added %s %s' % (user_firstname, user_lastname)
            login_user(User.get(user_mail), remember=False)
        else:
            status = 'user with this email is already exists'
    return render_template('hello.html', form=form, name=user_firstname, status=status)


@app.route('/protected')
@login_required
def protected():
    return render_template('protected.html')


if __name__ == '__main__':
    get_logger()
    app.config["REMEMBER_COOKIE_DURATION"] = timedelta(days=14)
    app.logger = logging.getLogger('ecomap')
    app.run()
