import sys
import os

os.environ['PRODROOT'] = os.path.dirname(os.path.dirname(
    os.path.abspath(__file__)))
os.environ['CONFROOT'] = os.environ['PRODROOT'] + '/etc'
os.environ['PYSRCROOT'] = os.environ['PRODROOT'] + '/src/python'

activate_this = "/home/frutkic/venv/ecomap/bin/activate_this.py"
execfile(activate_this, dict(__file__=activate_this))

os.environ['PRODROOT'] = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.environ['CONFROOT'] = os.environ['PRODROOT'] + '/etc'
os.environ['PYSRCROOT'] = os.environ['PRODROOT'] + '/src/python'

sys.path.insert(0, os.environ['PRODROOT'] + '/www')
sys.path.insert(1, os.environ['PYSRCROOT'])


from views import app as application
