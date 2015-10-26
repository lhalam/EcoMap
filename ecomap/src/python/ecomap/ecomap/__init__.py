from flask import Flask
from flask.ext.bootstrap import Bootstrap


app = Flask(__name__)
app.config['APPLICATION_ROOT'] = '/home/padalko/ss_projects/Lv-164.UI/ecomap'
app.config['SECRET_KEY'] = 'top secret!'
bootstrap = Bootstrap(app)

import ecomap.views
