import sys
import os

# from werkzeug.debug import DebuggedApplication

# !!this is configuration for virtual env of your project:
# if you using some virtualenv interpreter - uncomment next three lines
# and add your own path to env's 'activate_this.py' file

# activate_this = "/home/padalko/python_enviroments/flask_test/bin/activate_this.py"
# execfile(activate_this, dict(__file__=activate_this))

sys.path.insert(0, (os.path.join(os.environ['PRODROOT'], 'www')))

from views import app as application

# application = DebuggedApplication(application, True)
