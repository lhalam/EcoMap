"""Head application module."""
import os
import logging
import logging.config
from datetime import timedelta

from flask import Flask
from flask.ext.session import Session
from flask.ext.autodoc import Autodoc
from flask.ext.triangle import Triangle
from werkzeug.contrib.cache import MemcachedCache

from ecomap.config import Config

_CONFIG = Config().get_config()

TEMPLATE_FOLDER = os.path.join(os.environ['PRODROOT'], 'www/templates/')
app = Flask(__name__, template_folder=TEMPLATE_FOLDER)
Triangle(app)
auto = Autodoc(app)

logging.config.fileConfig(os.path.join(os.environ['CONFROOT'], '_log.conf'))
logger = logging.getLogger('flask_app')
app.config['SECRET_KEY'] = 'a7c268ab01141868811c070274413ea3c588733241659fcb'
app.config["REMEMBER_COOKIE_DURATION"] = timedelta(days=14)     # user time lib
app.config['SECRET_KEY'] = _CONFIG['ecomap.secret_key']
app.config['SESSION_TYPE']='memcached'
app.config['SESSION_MEMCACHED'] = MemcachedCache(_CONFIG['ecomap.memcached_servers'])
app.config["REMEMBER_COOKIE_DURATION"] = timedelta(days=14)
app.config['OAUTH_CREDENTIALS'] = {
    'facebook': {
        'id': _CONFIG['oauth.facebook_id'],
        'secret': _CONFIG['oauth.facebook_secret']
    }
}

Session(app)
