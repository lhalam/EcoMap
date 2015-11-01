import os
import jinja2
import logging

from flask import Flask, render_template, request, redirect, jsonify
from flask.ext.wtf import Form
from flask_wtf import Form
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms import StringField, SubmitField
from wtforms.validators import Required, Length, DataRequired
from flask.ext.bootstrap import Bootstrap

from ecomap.pool_final import pool_obj
from ecomap.utils import get_logger

app = Flask(__name__)
# app.config['APPLICATION_ROOT'] = '/home/padalko/ss_projects/Lv-164.UI/ecomap'
app.config['SECRET_KEY'] = 'topsecret!'
bootstrap = Bootstrap(app)


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

#
# @app.route('/submit', methods=('GET', 'POST'))
# def submit():
#     form = MyForm()
#     if form.validate_on_submit():
#         print 'submit'
#         return redirect('/success')
#     return render_template('submit.html', form=form)


def check_user(mail, password):
    with pool_obj.manager() as conn:
        q1 = conn['connection'].cursor()
        try:
            q1.execute('select password from user where email="%s";' % mail)
            db_user_password = q1.fetchone()
            app.logger.info(db_user_password[0])
            app.logger.info(password)
            if check_password_hash(db_user_password[0], password):
                return True
        except:
            return False


def is_user_exist(mail):
    with pool_obj.manager() as conn:
        q1 = conn['connection'].cursor()
        try:
            q1.execute('select email from user where email="%s";' % mail)
            db_user = q1.fetchone()
            if db_user:
                return True
        except:
            return False


def register_user(firstname, lastname, mail, password):
    hash_password = generate_password_hash(password)
    with pool_obj.manager() as conn:
        q1 = conn['connection'].cursor()
        q1.execute('INSERT INTO user (first_name, last_name, email, password) VALUES ("%s", "%s", "%s", "%s");'
                   % (firstname, lastname, mail, hash_password))
        conn['connection'].commit()


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        app.logger.debug('request %s' % request)  # <Request 'http://ecomap.new:81/login' [POST]>
        app.logger.debug('req data %s' % request.data)  # {"email":"vadime.padalko@gmail.com","password":"666664"}
        app.logger.debug('req json %s' % request.json)  # {u'password': u'666664', u'email': u'vadime.padalko@gmail.com'}
        user_mail = request.json['email']
        user_pass = request.json["password"]
        if check_user(user_mail, user_pass):
            app.logger.info('can login')
            status = 'checked, log in'
        else:
            status = 'no user in db or wrong paswd, cannot login'
        return jsonify({'check_user': status, 'paswd': user_pass, 'umail': user_mail})
    return jsonify({'method': 'GET'})


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        app.logger.info(request.json)
        user_firstname = request.json['firstname']
        user_lastname = request.json["lastname"]
        user_mail = request.json['email']
        user_pass = request.json["password"]
        if not is_user_exist(user_mail):
            register_user(user_firstname, user_lastname, user_mail, user_pass)
            status = 'added %s %s' % (user_firstname, user_lastname)
        else:
            status = 'user with this email is already exists'
        return jsonify({'status': status})

if __name__ == '__main__':
    get_logger()
    app.logger = logging.getLogger('ecomap')
    app.run()
