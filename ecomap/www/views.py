import os
import jinja2
import logging

from flask import Flask, render_template, request, redirect
from flask.ext.wtf import Form
from flask_wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import Required, Length, DataRequired
from flask.ext.bootstrap import Bootstrap

from ecomap.pool_final import pool_obj
from ecomap.utils import get_logger


app = Flask(__name__)
# app.config['APPLICATION_ROOT'] = '/home/padalko/ss_projects/Lv-164.UI/ecomap'
app.config['SECRET_KEY'] = 'topsecret!'
bootstrap = Bootstrap(app)

# sys.path.insert(0, '/home/padalko/ss_projects/Lv-164.UI/ecomap/www')
# app.jinja_loader = jinja2.FileSystemLoader('/home/padalko/ss_projects/Lv-164.UI/ecomap/www/templates')
# sys.path.insert(0, '/home/padalko/ss_projects/Lv-164.UI/ecomap/src/python/ecomap')


class MyForm(Form):
    name = StringField('name', validators=[DataRequired()])


class NameForm(Form):
    name = StringField('What is your name?', validators=[Length(min=4, max=25)])
    submit = SubmitField('Submit')


@app.route('/')
def index(name='start', name2='def_page'):
    return render_template('base.html', name=name, secname=name2)


@app.route('/page1')
def page1():
    name = 'Flask Config'
    config = app.config
    return render_template('page1.html', name=name, conf=config)


@app.route('/page2')
def page2(name=None, name2 = "Default"):
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
    form = NameForm()
    print 'form', form
    print 'formdata', form.data
    print 'formname', form.name
    print 'formsubmit', form.submit
    print 'ERRORS', form.SECRET_KEY
    print app.config['SECRET_KEY']
    # if form.validate_on_submit():  # invoke here a submitting
    if form.is_submitted():
        print 'SUBMITTED'

    if form.validate():

        print 'if'
        name = form.name.data
        form.name.data = ''
    return render_template('adv_form.html', form=form, name=name)


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


@app.route('/submit', methods=('GET', 'POST'))
def submit():
    form = MyForm()
    if form.validate_on_submit():
        print 'submit'
        return redirect('/success')
    return render_template('submit.html', form=form)

if __name__ == '__main__':
    get_logger()
    logger = logging.getLogger('ecomap')
    app.run()
