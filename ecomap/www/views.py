from flask import Flask, render_template, request
from flask.ext.bootstrap import Bootstrap
from flask.ext.wtf import Form
import sys
from wtforms import StringField, SubmitField
from wtforms.validators import Required, Length, DataRequired
from ecomap import app

sys.path.insert(0, '/home/padalko/ss_projects/Lv-164.UI/ecomap/src/python/ecomap')
from pool_final import pool_obj


class NameForm(Form):
    name = StringField('What is your name?', validators=[Required(),
                                                         Length(1, 16)])
    submit = SubmitField('Submit')


@app.route('/')
def index(name='start', name2='def_page'):
    return render_template('base.html', name=name, secname=name2)


@app.route('/page1')
def page1():
    name = '%username'
    name2 = 'pool_obj._db_name'
    return render_template('page1.html', name=name, secname=name2)


@app.route('/page2')
def page2(name=None, name2 = "Default"):
    name = '%username'
    name2 = 'os.environ'
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
    name = None
    form = NameForm()
    print 'form', form
    print 'formdata', form.data
    print 'formname', form.name
    print 'formsubmit', form.submit
    if form.validate_on_submit():  # invoke here a submitting
        name = form.name.data
        print 'if'
        form.name.data = ''
    return render_template('adv_form.html', form=form, name=name)


@app.errorhandler(404)
def not_found(e):
    return render_template('404.html')


@app.route('/db')
def db(name=None):
    with pool_obj.manager as conn:
        q1 = conn.cursor()
        q1 = q1.execute('show tables;')
        q2 = q1.fetchall()

    name = str(q2)
    return render_template('hi.html', name=name)


