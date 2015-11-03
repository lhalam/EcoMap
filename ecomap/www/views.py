import logging
from datetime import timedelta
from flask.ext.login import UserMixin, LoginManager, login_user, logout_user, login_required


from itsdangerous import URLSafeTimedSerializer
from flask import Flask, render_template, request, redirect, jsonify, url_for, abort
from flask.ext.bootstrap import Bootstrap
from flask.ext.triangle import Triangle
from werkzeug.security import generate_password_hash, check_password_hash

from ecomap.pool_final import pool_obj, retry
from ecomap.utils import get_logger


app = Flask(__name__)
app.secret_key = "topsecret!"
bootstrap = Bootstrap(app)
lm = LoginManager(app)
lm.login_view = 'login'
Triangle(app)

login_serializer = URLSafeTimedSerializer(app.secret_key)
app.config["REMEMBER_COOKIE_DURATION"] = timedelta(days=14)


@app.route('/index')
def index_ecomap():
    return render_template('index.html')


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
        app.logger.warning('DATA from get_auth_token %s' % data)
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
    data = login_serializer.loads(token, max_age=max_age)
    user = User.get_user_by_id(data[0])
    if user and data[1] == user.password:
        return user
    return None


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        app.logger.debug('login json request %s' % request.json)
        user = User.get(request.json['email'])
        if user is None or not user.verify_password(request.json["password"]):
            status = 'no user in db or wrong paswd, cannot login'
            # abort(401)
            return jsonify({'login_status': status, 'email': request.json['email']}), 401
        login_user(user, remember=True)
        app.logger.info('user %s logged in' % user.email)
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
    return abort(400)


@app.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    status = 'logged out'
    # return jsonify({'check_user': status})
    return redirect(url_for('index_ecomap'), 302)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        app.logger.debug('registration JSON' % request.json)
        user_firstname = request.json['first_name']
        user_lastname = request.json["last_name"]
        user_mail = request.json['email']
        user_pass = request.json["password"]
        if not User.get(user_mail):
            register_user(user_firstname, user_lastname, user_mail, user_pass)
            app.logger.info('user %s was registered' % user_mail)
            status = 'added %s %s' % (user_firstname, user_lastname)
            login_user(User.get(user_mail), remember=True)
            return jsonify({'status': status}), 200
        else:
            status = 'user with this email is already exists'
            # abort(400)
            return jsonify({'status': status}), 400


if __name__ == '__main__':
    get_logger()
    app.config["REMEMBER_COOKIE_DURATION"] = timedelta(days=14)
    app.logger = logging.getLogger('ecomap')
    app.run()
