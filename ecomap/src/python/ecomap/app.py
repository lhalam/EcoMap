import logging
import os
from datetime import timedelta

from flask.ext.triangle import Triangle
from flask import Flask, redirect, url_for, session, request
from flask_oauthlib.client import OAuth, OAuthException

from ecomap.utils import get_logger

template_folder = os.path.join(os.environ['PRODROOT'], 'www/templates/')
app = Flask(__name__, template_folder=template_folder)
Triangle(app)

get_logger()
logger = logging.getLogger('flask_app')
app.config['SECRET_KEY'] = 'a7c268ab01141868811c070274413ea3c588733241659fcb'
app.config["REMEMBER_COOKIE_DURATION"] = timedelta(days=14)     # user time lib

FACEBOOK_APP_ID = '399515533592508'
FACEBOOK_APP_SECRET = '554d6845d39693ccf43f93a01f6d1149'
SOCIAL_AUTH_FACEBOOK_SCOPE = ['email']

oauth = OAuth(app)

facebook = oauth.remote_app(
    'facebook',
    consumer_key=FACEBOOK_APP_ID,
    consumer_secret=FACEBOOK_APP_SECRET,
    request_token_params={'return_scopes': 'true', 'scope': ['public_profile', 'email', 'user_likes']},
    base_url='https://graph.facebook.com',
    request_token_url=None,
    access_token_url='/oauth/access_token',
    access_token_method='GET',
    authorize_url='https://www.facebook.com/dialog/oauth'
)
