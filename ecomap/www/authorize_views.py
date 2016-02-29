"""Module contains routes for user authorization,
   registering and logout.
"""
import json
import requests
import time

from flask import request, jsonify, Response, render_template
from flask_login import login_user, logout_user, login_required

from urlparse import parse_qsl

import ecomap.user as ecomap_user

from ecomap import validator
from ecomap.app import app, logger, auto
from ecomap.db import util as db
from ecomap.config import Config

_CONFIG = Config().get_config()

COOKIE_MAX_AGE = app.config['REMEMBER_COOKIE_DURATION']

@app.route('/api/logout', methods=['POST', 'GET'])
@auto.doc()
@login_required
def logout():
    """Method for user's log out.
    :rtype: JSON
    :return:
        - if logging out was successful:
            ``{result:True}``
        - in case of problems:
            ``{result:False}``

    """
    return jsonify(result=logout_user())


@app.route('/api/register', methods=['POST'])
@auto.doc()
def register():
    """Method for registration new user in db.
    Method checks if user is not exists and handle
    registration processes.
    :rtype: JSON
    :request args: `{'first_name': 'Ivan',
                     'last_name': 'Sirko',
                     'nickname': 'Bulka',
                     'email': 'email@test.com',
                     'password': 'passw'}`
    :return:
        - if one of the field is incorrect or empty:
            ``{'error':'Unauthorized'}``
        - if user already exists
            ``{'status': 'user with this email already exists'}``
        - if registration was successful:
            ``{'status': added user <username>}``

    :statuscode 401: form is invalid or empty
    :statuscode 400: user already exists
    :statuscode 200: registration successful

    """
    response = jsonify(msg='unauthorized'), 400
    if request.method == 'POST' and request.get_json():
        data = request.get_json()
        valid = validator.user_registration(data)

        if valid['status']:
            ecomap_user.register(data['first_name'],
                                 data['last_name'],
                                 data['nickname'],
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
@auto.doc()
def email_exist():
    """Function for AJAX call from frontend.
    Validates unique email identifier before registering a new user
    :return: json with status 200 or 400
    """
    if request.method == 'POST' and request.get_json():
        data = request.get_json()
        user = ecomap_user.get_user_by_email(data['email'])
        return jsonify(isValid=bool(user))


@app.route('/api/nickname_exist', methods=['POST'])
@auto.doc()
def nickname_exist():
    """Function for AJAX call from frontend.
    Validates unique nickname identifier before registering a new user
    :return: json with status 200 or 400
    """
    if request.method == 'POST' and request.get_json():
        data = request.get_json()
        user = db.get_user_by_nick_name(data['nickname'])
        return jsonify(isValid=bool(user))


@app.route('/api/login', methods=['POST'])
@auto.doc()
def login():
    """Login processes handler.
    Log user in or shows error messages.

    :rtype: JSON
    :request args: `{'email': 'username@mail.com',
                     'password': 'userpaswd'}`
    :return:
        - if credentials are ok and log in successful:
            ``{"email": "username@mail.com",
            "iat": "???",
            "id": 6,
            "name": "oleg",
            "role": "admin",
            "surname": "lyashko",
            "token": "hashed_auth_token"}``
        - if user with entered email isn't exists or password was invalid:
            ``{'error':'message'}``

    :statuscode 401: user doesn't exist or password is invalid
    :statuscode 400: login data has invalid format:
    :statuscode 200: credentials are ok

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

                response.set_cookie('id',
                                    bytes(user.uid),
                                    max_age=COOKIE_MAX_AGE)
                response.set_cookie('name',
                                    bytes(user.first_name),
                                    max_age=COOKIE_MAX_AGE)
                response.set_cookie('surname',
                                    bytes(user.last_name),
                                    max_age=COOKIE_MAX_AGE)
                response.set_cookie('role',
                                    bytes(user.role),
                                    max_age=COOKIE_MAX_AGE)
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
@auto.doc()
def oauth_login(provider):
    """Provides facebook authorization.
    Retrieves user info from facebook, check if there is
    user with retrieved from facebook user id,
    :param provider: Oauth provider (Facebook by default)

       - if yes:
           skips to next step
       - if not:
           checks if there is user with retrieved email
           - if yes:
               adds oauth credentials to this user
           - if not:
               creates new user
       After all function logging in user into app and return it's params

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
    nickname = profile['last_name'] + str(time.time())
    logger.info(profile['picture']['data']['url'])
    user = ecomap_user.facebook_register(profile['first_name'],
                                         profile['last_name'],
                                         nickname,
                                         profile['email'],
                                         provider,
                                         profile['id'])

    db.insert_user_avatar(user.uid, profile['picture']['data']['url'])

    login_user(user, remember=True)

    response = jsonify(iat="???",
                       token=user.get_auth_token(),
                       email=user.email)

    response.set_cookie('id',
                        bytes(user.uid),
                        max_age=COOKIE_MAX_AGE)
    response.set_cookie('name',
                        bytes(user.first_name),
                        max_age=COOKIE_MAX_AGE)
    response.set_cookie('surname',
                        bytes(user.last_name),
                        max_age=COOKIE_MAX_AGE)
    response.set_cookie('role',
                        bytes(user.role),
                        max_age=COOKIE_MAX_AGE)

    return response


@app.route('/api/restore_password', methods=['POST'])
@auto.doc()
def restore_password_request():
    """Function to restore forgotten password.

    :rtype: JSON
    :request args: `{'email': 'username@mail.com'}`
    :return:
        - if credentials are ok and checking successful:
            ``{message='Email was sended.'}``
        - if user's email isn't exists:
            ``{'error':'There is not such email.'}``

    :statuscode 401: no email
    :statuscode 200: email sended

    """
    json = request.get_json()
    email = json['email']
    user = ecomap_user.get_user_by_email(email)
    if user:
        ecomap_user.restore_password(user)
        response = jsonify(message='Email was sended.'), 200
    else:
        response = jsonify(error='There is not such email.'), 401
    return response


@app.route('/api/restore_password_page/<string:hashed>', methods=['GET'])
@auto.doc()
def restore_password_page(hashed):
    """Renders page template to restore password.
    :param hashed: unique hash to identify user via sending it to email.

    :return redirect to main page with rendered template.

    """
    valid = validator.hash_check(hashed)
    page = render_template('index.html')

    if valid:
        creation_time = db.check_hash_in_db(hashed)
        if creation_time:
            elapsed = time.time() - creation_time[0]
            if elapsed <= _CONFIG['hash_options.lifetime']:
                page = render_template('password_restoring_pass.html')

    return page


@app.route('/api/restore_password', methods=['PUT'])
@auto.doc()
def restore_password():
    """Updates user password.


    """
    data = request.get_json()
    valid = validator.change_password(data)

    if valid:
        user_id = db.get_user_id_by_hash(data['hash_sum'])
        if user_id:
            password = ecomap_user.hash_pass(data['password'])
            db.restore_password(user_id[0], password)
            response = jsonify(message='Password restored.')
        else:
            response = jsonify(message='got error.'), 400
    else:
        response = Response(json.dumps(valid),
                            mimetype='application/json'), 400
    return response


@app.route('/api/delete_user_request', methods=['DELETE'])
@auto.doc()
def find_to_delete():
    """Function to send email with delete link"""
    data = request.get_json()
    search_id = data['user_id']
    user = ecomap_user.get_user_by_id(search_id)
    if search_id == ecomap_user.User.get_id(user):
        ecomap_user.delete_user(user)
        response = jsonify(message='Email was sended.'), 200
    else:
        response = jsonify(error="You can't do that"), 400
    return response


@app.route('/api/delete_user_page/<string:hashed>', methods=['GET'])
@auto.doc()
def delete_user_page(hashed):
    """Renders page to confirmation of deleting user"""
    valid = validator.hash_check(hashed)
    page = render_template('index.html')

    if valid:
        creation_time = db.check_hash_in_db(hashed)
        if creation_time:
            elapsed = time.time() - creation_time[0]
            if elapsed <= _CONFIG['hash_options.lifetime']:
                page = render_template('index.html')
    return page


@app.route('/api/user_delete', methods=['DELETE'])
def delete_user():
    """Controller for handling deletion of user profile by
    profile owner.
    :return: json object with success message or message with error
    """
    data = request.get_json()
    valid = validator.hash_check(data['hash_sum'])
    if valid['status']:
        user_id = db.get_user_id_by_hash(data['hash_sum'])
        logger.warning(user_id)
        tuple_of_problems = db.get_problem_id_for_del(user_id[0])
        problem_list = []
        for tuple_with_problem_id in tuple_of_problems:
            problem_list.append(tuple_with_problem_id[0])
        if db.get_user_comments_count:
            db.change_comments_to_anon(user_id[0])
        if problem_list:
            for problem_id in problem_list:
                db.change_problem_to_anon(problem_id)
                db.change_activity_to_anon(problem_id)
            db.delete_user(user_id[0])
            logger.info('User with id %s has been deleted' % user_id[0])
            response = jsonify(msg='success', deleted_user=user_id[0])
        else:
            db.delete_user(user_id[0])
            logger.info('User with id %s has been deleted' % user_id[0])
            response = jsonify(msg='success', deleted_user=user_id[0])
    else:
        response = Response(json.dumps(valid),
                            mimetype='application/json'), 400
    return response
