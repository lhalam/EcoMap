import logging
import os
import jinja2

from flask import Flask, render_template, request, session
from flask.ext.bootstrap import Bootstrap
from flask.ext.wtf import Form
from wtforms import StringField, SubmitField
from wtforms.ext import csrf
from wtforms.validators import Length, DataRequired

from pool_final import pool_obj
from utils import get_logger
# from flask_wtf.csrf import CsrfProtect


app = Flask(__name__)
app.config['APPLICATION_ROOT'] = '/home/padalko/ss_projects/Lv-164.UI/ecomap'
app.config['CSRF_ENABLED'] = True
app.config['SECRET_KEY'] = 'topsecret!'
bootstrap = Bootstrap(app)
# CsrfProtect(app)

app.jinja_loader = jinja2.FileSystemLoader('/home/padalko/ss_projects/Lv-164.UI/ecomap/www/templates')


class NameForm(Form):
    name = StringField('What is your name?', validators=[Length(1, 16)])
    submit = SubmitField('Submit')


@app.route('/')
def index(name='start', name2='def_page'):
    return render_template('base.html', name=name, secname=name2)


@app.route('/page1')
def page1():
    name = '%username'
    name2 = os.environ
    return render_template('page1.html', name=name, secname=name2)


@app.route('/page2')
def page2(name=None, name2 = "Default"):
    name = '%username'
    name2 = 'Second_Name'
    return render_template('hi.html', name=name, secname=name2)


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
    name = 'dsds'
    form = NameForm()
    print 'router'
    print form.name
    print form.submit
    print form.csrf_enabled
    print form.csrf_token
    print form.data
    print form.hidden_tag()
    # if form.validate_on_submit():  # invoke here a validate on submitting
    name = form.data['name']
    print 'valid'

    form.name.data = ''

    return render_template('adv_form.html', form=form, name=name)


@app.errorhandler(404)
def not_found(e):
    return render_template('404.html')


@app.route('/db', methods=['GET', 'POST'])
def db(sql=None):

    if request.method == 'POST' and 'sql_query' in request.form:
        sql = request.form['sql_query']
        with pool_obj.manager() as conn:
            q1 = conn['connection'].cursor()
            q1.execute(sql)
            sql = q1.fetchall()
    return render_template('sql.html', sql_query=sql)



if __name__ == '__main__':
    print app.config
    app.run(debug=True, host='0.0.0.0')
    get_logger()
    logger = logging.getLogger('Flask')