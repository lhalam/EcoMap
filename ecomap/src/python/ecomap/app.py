"""Head application module."""
import os
import logging
import logging.config
from datetime import timedelta

from flask import Flask
from flask.ext.triangle import Triangle
from flask.ext.autodoc import Autodoc
from ecomap.config import Config

# from flask import Flask, session
from flask.ext.session import Session, MemcachedSessionInterface
# from flask.ext.memcache_session import Session
from werkzeug.contrib.cache import MemcachedCache

cache = MemcachedCache(['127.0.0.1:11211'])


_CONFIG = Config().get_config()

TEMPLATE_FOLDER = os.path.join(os.environ['PRODROOT'], 'www/templates/')
app = Flask(__name__, template_folder=TEMPLATE_FOLDER)
Triangle(app)
auto = Autodoc(app)

logging.config.fileConfig(os.path.join(os.environ['CONFROOT'], '_log.conf'))
logger = logging.getLogger('flask_app')
app.config['SECRET_KEY'] = 'a7c268ab01141868811c070274413ea3c588733241659fcb'
app.config["REMEMBER_COOKIE_DURATION"] = timedelta(days=14)     # user time lib

app.config["SESSION_TYPE"] = 'memcached'
app.session_interface = MemcachedSessionInterface(cache,'session1:')


app.config['OAUTH_CREDENTIALS'] = {
    'facebook': {
        'id': _CONFIG['oauth.facebook_id'],
        'secret': _CONFIG['oauth.facebook_secret']
    }
}

# Session(app)
# sess = Session()
# sess.init_app(app)

