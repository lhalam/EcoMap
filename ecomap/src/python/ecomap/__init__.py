from flask import Flask
from flask.ext.bootstrap import Bootstrap
import sys

app = Flask(__name__)
app.config['APPLICATION_ROOT'] = '/home/padalko/ss_projects/Lv-164.UI/ecomap'
app.config['SECRET_KEY'] = 'topsecret!'
bootstrap = Bootstrap(app)

sys.path.insert(0, '/home/padalko/ss_projects/Lv-164.UI/ecomap/www')

import views