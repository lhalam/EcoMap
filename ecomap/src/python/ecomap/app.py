"""Head application module."""
import logging
import os
from datetime import timedelta

from flask import Flask
from flask.ext.triangle import Triangle
from flask.ext.autodoc import Autodoc

from ecomap.config import Config
from ecomap.utils import get_logger

_CONFIG = Config().get_config()

TEMPLATE_FOLDER = os.path.join(os.environ['PRODROOT'], 'www/templates/')
app = Flask(__name__, template_folder=TEMPLATE_FOLDER)
Triangle(app)
auto = Autodoc(app)

get_logger()
logger = logging.getLogger('flask_app')
app.config['SECRET_KEY'] = 'a7c268ab01141868811c070274413ea3c588733241659fcb'
app.config["REMEMBER_COOKIE_DURATION"] = timedelta(days=14)     # user time lib
app.config['OAUTH_CREDENTIALS'] = {
    'facebook': {
        'id': _CONFIG['oauth.facebook_id'],
        'secret': _CONFIG['oauth.facebook_secret']
    }
}
