import sys
import os

# this is configuration for virtual env of your project:
# if you using some virtualenv interpreter - uncomment next three lines
# and add your own path to env's 'activate_this.py' file
activate_this = "/home/padalko/python_enviroments/flask_test/bin/activate_this.py"
execfile(activate_this, dict(__file__=activate_this))
sys.path.insert (0, (os.path.join(os.environ['PRODROOT'], 'www')))

from views import app as application

application.secret_key = "topsecret!"

# if using templates for your project, define templates path here:
# also change the path to your own to see some stuff from views.py
application.template_folder='/home/padalko/ss_projects/Lv-164.UI/ecomap/www/templates'

