import logging
import sys
import os

activate_this = "/home/padalko/python_enviroments/flask_test/bin/activate_this.py"
execfile(activate_this, dict(__file__=activate_this))

os.environ['PRODROOT'] = "/home/padalko/ss_projects/Lv-164.UI/ecomap"
os.environ['PYSRCROOT'] = "/home/padalko/ss_projects/Lv-164.UI/ecomap/src/python"
os.environ['CONFROOT'] = "/home/padalko/ss_projects/Lv-164.UI/ecomap/etc"
os.environ['PYTHONPATH'] = "/home/padalko/ss_projects/Lv-164.UI/ecomap/src/python"


sys.path.insert (0,'/home/padalko/ss_projects/Lv-164.UI/ecomap/src/python/ecomap')
os.chdir('/home/padalko/ss_projects/Lv-164.UI/ecomap/src/python/ecomap')

from utils import get_logger
get_logger()

from ecomap_flask import app as application

application.secret_key = "topsecret!"
application.template_folder='/home/padalko/ss_projects/Lv-164.UI/ecomap/www/templates'
application.config['APPLICATION_ROOT'] = '/home/padalko/ss_projects/Lv-164.UI/ecomap'

