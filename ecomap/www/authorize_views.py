"""Module contains routes for user authorization,
   registering and logout.
"""
import json
import requests

from flask import request, jsonify, Response
from flask_login import login_user, logout_user, login_required

from urlparse import parse_qsl

import ecomap.user as ecomap_user

from ecomap import validator
from ecomap.app import app, logger
from ecomap.db import util as db


@app.route('/api/logout', methods=['POST', 'GET'])
@login_required
def logout():
    """Method for user's log out.

    :return:
        - if logging out was successful:
            json {result:True}
        - in case of problems:
            json {result:False}
    """
    return jsonify(result=logout_user())


@app.route('/api/register', methods=['POST'])
def register():
    """Method for registration new user in db.
    Method checks if user is not exists and handle
    registration processes.

    :return:
        - if one of the field is incorrect or empty:
            json {'error':'Unauthorized'}
            Status 401 - Unauthorized
        - if user already exists
            Status 400 - Bad Request
            json {'status': 'user with this email already exists'}
        - if registration was successful:
            json {'status': added user <username>}
            Status 200 - OK
    """
    response = jsonify(msg='unauthorized'), 400
    if request.method == 'POST' and request.get_json():
        data = request.get_json()
        valid = validator.user_registration(data)

        if valid['status']:
            ecomap_user.register(data['first_name'],
                                 data['last_name'],
                                 data['email'],
                                 data['password'])
            msg = 'added %s %s' % (data['first_name'],
                                   data['last_name'])
            response = jsonify({'status_message': msg}), 201
        else:
            response = Response(json.dumps(valid),
                                mimetype='application/json'), 400
    return response


@app.route('/api/email_exist', methods=['POST'])
def email_exist():
    """Function for AJAX call from frontend.
    Validates unique email identifier before registering a new user
    :return: json with status 200 or 400
    """
    if request.method == 'POST' and request.get_json():
        data = request.get_json()
        user = ecomap_user.get_user_by_email(data['email'])
        return jsonify(isValid=bool(user))


@app.route('/api/login', methods=['POST'])
def login():
    """Login processes handler.
    Log user in or shows error messages.

    :return:
        - if log in succeed:
            json with user data from db.
            Status 200 - OK
        - if user with entered email isn't exists
            or password was invalid:
            json with error message
            {'error':'message'}
            Status 401 - Unauthorized
        - if login data has invalid format:
            Status 400 - Bad Request
    """
    response = jsonify(), 401
    if request.method == 'POST' and request.get_json():
        data = request.get_json()
        valid = validator.user_login(data)

        if valid['status']:
            user = ecomap_user.get_user_by_email(data['email'])
            if user and user.verify_password(data['password']):
                login_user(user, remember=True)
                response = jsonify(id=user.uid,
                                   name=user.first_name,
                                   surname=user.last_name,
                                   role=user.role, iat="???",
                                   token=user.get_auth_token(),
                                   email=user.email)
            if not user:
                logger.warning('if not user')
                response = jsonify(error='There is no user with given email.',
                                   logined=0, ), 401
            elif not user.verify_password(data['password']):
                logger.warning('if not user verify')
                response = jsonify(error='Invalid password, try again.',
                                   logined=0), 401
        else:
            response = Response(json.dumps(valid),
                                mimetype='application/json'), 400
    return response


@app.route('/api/authorize/<provider>', methods=['POST', 'GET'])
def oauth_login(provider):
    """Provides facebook authorization.
       Retrieves user info from facebook, check if there is
       user with retrieved from facebook user id,
       if yes:
           skips to next step
       if not:
           checks if there is user with retrieved email
           if yes:
               adds oauth credentials to this user
           if not:
               creates new user
       After all function loggins user and return it's params
    """

    access_token_url = 'https://graph.facebook.com/oauth/access_token'
    graph_api_url = 'https://graph.facebook.com/v2.5/me?fields=email,'\
                    'first_name,last_name,id,picture.type(large)'

    params = {
        'client_id': request.json['clientId'],
        'redirect_uri': request.json['redirectUri'],
        'client_secret': app.config['OAUTH_CREDENTIALS']['facebook']['secret'],
        'code': request.json['code']
    }

    resource = requests.get(access_token_url, params=params)
    access_token = dict(parse_qsl(resource.text))
    resource = requests.get(graph_api_url, params=access_token)
    profile = json.loads(resource.text)
    logger.info(profile['picture']['data']['url'])

    user = ecomap_user.facebook_register(profile['first_name'],
                                         profile['last_name'],
                                         profile['email'],
                                         provider,
                                         profile['id'])

    db.insert_user_avatar(user.uid, profile['picture']['data']['url'])

    login_user(user, remember=True)

    response = jsonify(id=user.uid,
                       name=user.first_name,
                       surname=user.last_name,
                       role=user.role, iat="???",
                       token=user.get_auth_token(),
                       email=user.email)

    return response


@app.route('/api/restore_password', methods=['POST'])
def restore_password():
    """Function to restore forgotten password."""
    json = request.get_json()
    email = json['email']
    user = ecomap_user.get_user_by_email(email)
    if user:
        ecomap_user.restore_password(user)
        response = jsonify(message='Email was sended.'), 200
    else:
        response = jsonify(error='There is not such email.'), 401
    return response


@app.route('/api/restore_password_page/<string:hashed>')
def restore_password_page(hashed):
    """Renders page to restore password."""
    pass
