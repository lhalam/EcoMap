# coding=utf-8
"""
This module holds all views controls for
ecomap project.
"""
import json
import functools
import time
import facebook

TOKEN = ''
from flask import render_template, request, jsonify, Response, g, abort
from flask import redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user

import ecomap.user as usr

from ecomap import validator
from ecomap.app import app, logger, facebook
from ecomap.db import util as db
# from ecomap.oauth import facebook


from flask import Flask, redirect, url_for, session, request
from flask_oauthlib.client import OAuth, OAuthException


@app.before_request
def load_users():
    """Function to check if user is authenticated, else creates
       Anonymous user.
       Launches before requests.
    """
    if current_user.is_authenticated:
        g.user = current_user
        logger.warning(g.user)
    else:
        anon = usr.Anonymous()
        g.user = anon.username
        logger.warning(g.user)


def is_admin(func):
    """Decorator function to protect routes from non admin users.
       :params: func - function we want to protect from non admin users
       :return: wrapper function
    """
    @functools.wraps(func)
    def wrapped(*args, **kwargs):
        """Wrapper function to give arguments to func.
           :params: *args - list of arguments
                    **kwargs - dictionary of arguments
           :return: function with given arguments
        """
        logger.warning(g.user)
        logger.warning('SIC!')
        logger.warning(g.user.role)
        if g.user.role != 'admin':
            abort(403)
        return func(*args, **kwargs)
    return wrapped


@app.route('/f')
def index_f():
    return redirect(url_for('login_f'))


@app.route('/login_f')
def login_f():
    callback = url_for(
        'facebook_authorized',
        next=request.args.get('next') or request.referrer or None,
        _external=True
    )
    return facebook.authorize(callback=callback)


@app.route('/login/authorized')
def facebook_authorized():
    resp = facebook.authorized_response()
    if resp is None:
        return 'Access denied: reason=%s error=%s' % (
            request.args['error_reason'],
            request.args['error_description']
        )
    if isinstance(resp, OAuthException):
        return 'Access denied: %s' % resp.message

    session['oauth_token'] = (resp['access_token'], '')
    me = facebook.get('/me')
    logger.warning(me)
    logger.warning(dir(me))
    logger.warning(me.data)
    return 'Logged in as id=%s name=%s, %s  redirect=%s' % \
        (me.data['id'], me.data['name'], me.data['email'], request.args.get('next'))


@facebook.tokengetter
def get_facebook_oauth_token():
    return session.get('oauth_token')


@app.route('/api/authorize/facebook', methods=['POST', 'GET'])
def login_with_facebook():

    redirect_uri = url_for('oauth_callback', provider='facebook',
                           _external=True)

    params = {'scope': 'public_profile',
              'response_type': 'code',
              'redirect_uri': redirect_uri}

    logger.info(url_for('oauth_callback', provider='facebook',
                        _external=True))

    url = facebook.get_authorize_url(**params)
    return redirect(url)


@app.route('/api/callback/<provider>', methods=['POST', 'GET'])
def oauth_callback(provider):
    logger.info(request.args['code'])

    redirect_uri = url_for('oauth_callback', provider='facebook',
                           _external=True)

    session = facebook.get_auth_session(data={'code': request.args['code'],
                                        'grant_type': 'authorization_code',
                                              'redirect_uri': redirect_uri})

    logger.info('Got session token.')
    data = session.get('me?fields=id,email,first_name,last_name').json()
    logger.info(data['email'])
    logger.info(data['id'])
    logger.info(data['first_name'])
    logger.info(data['last_name'])
    data['password'] = time.ctime()

    if not usr.get_user_by_email(data['email']):
        usr.facebook_register(data['first_name'],
                              data['last_name'],
                              data['email'],
                              data['password'],
                              'facebook',
                              data['id'])
        msg = 'added %s %s' % (data['first_name'],
                               data['last_name'])
        response = jsonify({'status_message': msg}), 201
    else:
        msg = 'user with this email already exists'
        response = jsonify({'status_message': msg}), 401
    return response





@app.route('/', methods=['GET'])
def index():
    """Controller starts main application page.
    return: renders html template with angular app.
    """
    return render_template('index.html')


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
            user = usr.get_user_by_email(data['email'])
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


@app.route('/api/change_password', methods=['POST'])
@login_required
def change_password():
    """Function, used to change user password
       :return: response - json object.
    """
    response = jsonify(), 401
    data = request.get_json()

    valid = validator.change_password(data)

    if valid['status']:
        user = usr.get_user_by_id(data['id'])
        if user and user.verify_password(data['old_pass']):
            user.change_password(data['password'])
            response = jsonify(), 200
        else:
            response = jsonify(), 400
    else:
        response = Response(json.dumps(valid),
                            mimetype='application/json'), 400
    return response


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
    result = logout_user()
    return jsonify(result=result)


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
            usr.register(data['first_name'],
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
        user = usr.get_user_by_email(data['email'])
        return jsonify(isValid=bool(user))


@app.route('/api/user_detailed_info/<int:user_id>')
def get_user_info(user_id):
    """This method returns json object with user data."""
    if request.method == 'GET':
        user = usr.get_user_by_id(user_id)
        if user:
            return jsonify(name=user.first_name, surname=user.last_name,
                           email=user.email, role=user.role)
        else:
            return jsonify(status='There is no user with given email'), 401


@app.route("/api/resources", methods=['POST'])
@login_required
@is_admin
def resource_post():
    """Function which edits resource name.
    :return: If there is already resource with this name:
                 {'error': 'resource already exists'}, 400
             If request data is invalid:
                 {'status': False, 'error': [list of errors]}, 400
             If all ok:
                 {'added_resource': 'resource_name',
                  'resource_id': 'resource_id'}
    """
    data = request.get_json()

    valid = validator.resource_post(data)

    if valid['status']:
        if db.get_resource_id(data['resource_name']):
            return jsonify(error='Resource already exists'), 400

        db.add_resource(data['resource_name'])
        added_res_id = db.get_resource_id(data['resource_name'])
        response = jsonify(added_resource=data['resource_name'],
                           resource_id=added_res_id[0])
    else:
        response = Response(json.dumps(valid),
                            mimetype='application/json'), 400
    return response


@app.route("/api/resources", methods=['PUT'])
@login_required
@is_admin
def resource_put():
    """Function which edits resource name.
    :return: If there is already resource with this name:
                 {'error': 'this name already exists'}, 400
             If request data is invalid:
                 {'status': False, 'error': [list of errors]}, 400
             If all ok:
                 {'status': 'success', 'edited': 'resource_name'}
    """
    data = request.get_json()

    valid = validator.resource_put(data)

    if valid['status']:
        if db.get_resource_id(data['resource_name']):
            return jsonify(error='this name already exists'), 400

        db.edit_resource_name(data['resource_name'],
                              data['resource_id'])
        response = jsonify(status='success',
                           edited=data['resource_name'])
    else:
        response = Response(json.dumps(valid),
                            mimetype='application/json'), 400
    return response


@app.route("/api/resources", methods=['DELETE'])
@login_required
@is_admin
def resource_delete():
    """Function which deletes resource from database.
       Before delete checks if resource have any permissions.
    :return: If resource have permissions:
                 {'error': 'Cannot delete!'}, 400
             If request data is invalid:
                 {'status': False, 'error': [list of errors]}, 400
             If all ok:
                 {'status': 'success', 'deleted_resource': 'resource_id'}
    """
    data = request.get_json()

    valid = validator.resource_delete(data)

    if valid['status']:
        if not db.check_resource_deletion(data['resource_id']):
            db.delete_resource_by_id(data['resource_id'])
            response = jsonify(status='success',
                               deleted_resource=data['resource_id'])
        else:
            response = jsonify(error='Cannot delete!'), 400
    else:
        response = Response(json.dumps(valid),
                            mimetype='application/json'), 400
    return response


@app.route("/api/resources", methods=['GET'])
@login_required
@is_admin
def resource_get():
    """Function which returns all resources from database.
       :return: {'resource_name': 'resource_id'}
    """
    query = db.get_all_resources()
    parsed_data = {}
    if query:
        parsed_data = {res[1]: res[0] for res in query}
    return jsonify(parsed_data)


@app.route("/api/roles", methods=['POST'])
@login_required
@is_admin
def role_post():
    """Function which adds new role into database.
    :return: If there is already role with this name:
                 {'error': 'role already exists'}, 400
             If request data is invalid:
                 {'status': False, 'error': [list of errors]}, 400
             If all ok:
                 {'added_role': 'role_name',
                  'added_role_id': 'role_id'}
    """
    data = request.get_json()

    valid = validator.role_post(data)

    if valid['status']:
        if db.get_role_id(data['role_name']):
            return jsonify(error='role already exists'), 400

        db.insert_role(data['role_name'])
        added_role_id = db.get_role_id(data['role_name'])

        response = jsonify(added_role=data['role_name'],
                           added_role_id=added_role_id[0])
    else:
        response = Response(json.dumps(valid),
                            mimetype='application/json'), 400
    return response


@app.route("/api/roles", methods=['PUT'])
@login_required
@is_admin
def role_put():
    """Function which edits role name.
    :return: If there is already resource with this name:
                 {'error': 'this name already exists'}, 400
             If request data is invalid:
                 {'status': False, 'error': [list of errors]}, 400
             If all ok:
                 {'status': 'success', 'edited': 'resource_name'}
    """
    data = request.get_json()

    valid = validator.role_put(data)

    if valid['status']:
        if db.get_role_id(data['role_name']):
            return jsonify(error='this name already exists'), 400

        db.edit_role(data['role_name'], data['role_id'])
        response = jsonify(status='success',
                           edited=data['role_name'])
    else:
        response = Response(json.dumps(valid),
                            mimetype='application/json'), 400
    return response


@app.route("/api/roles", methods=['DELETE'])
@login_required
@is_admin
def role_delete():
    """Function which deletes role from database.
    :return: If role has permissions:
                 {'error': 'Cannot delete!'}
             If request data is invalid:
                 {'status': False, error: [list of errors]}, 400
             If all ok:
                 {'status': 'success', 'deleted_role': 'role_id'}
    """
    data = request.get_json()

    valid = validator.role_delete(data)

    if valid['status']:
        if not db.check_role_deletion(data['role_id']):
            db.delete_role_by_id(data['role_id'])
            response = jsonify(msg='success',
                                   deleted_role=data['role_id'])
        else:
            response = jsonify(error='Cannot delete!')
    else:
        response = Response(json.dumps(valid),
                            mimetype='application/json'), 400
    return response


@app.route("/api/roles", methods=['GET'])
@login_required
@is_admin
def role_get():
    """Function which gets all roles from database.
       :return: {'role_name': 'role_id'}
    """
    query = db.get_all_roles()
    parsed_data = {}
    if query:
        parsed_data = {res[1]: res[0] for res in query}
    return jsonify(parsed_data)


@app.route("/api/permissions", methods=['POST'])
@login_required
@is_admin
def permission_post():
    """Function which adds new permission into database.
    :return: If request data is invalid:
                 {'status': False, 'error': [list of errors]}, 400
             If all ok:
                 {'added_permission': 'description',
                  'permission_id': 'permission_id'}
    """

    if request.method == 'POST' and request.get_json():
        data = request.get_json()

        valid = validator.permission_post(data)

        if valid['status']:
            db.insert_permission(data['resource_id'],
                                 data['action'],
                                 data['modifier'],
                                 data['description'])
            added_perm_id = db.get_permission_id(data['resource_id'],
                                                 data['action'],
                                                 data['modifier'])
            response = jsonify(added_permission_for=data['description'],
                               permission_id=added_perm_id[0])
        else:
            response = Response(json.dumps(valid),
                                mimetype='application/json'), 400
        return response


@app.route("/api/permissions", methods=['PUT'])
@login_required
@is_admin
def permission_put():
    """Function which edits permission.
    :return: If request data is invalid:
                 {'status': False, 'error': [list of errors]}, 400
             If all ok:
                 {'status': 'success',
                  'edited_perm_id': 'permission_id'}
    """
    if request.method == 'PUT' and request.get_json():
        data = request.get_json()

        valid = validator.permission_put(data)

        if valid['status']:
            db.edit_permission(data['action'],
                               data['modifier'],
                               data['permission_id'],
                               data['description'])
            response = jsonify(status='success',
                               edited_perm_id=data['permission_id'])
        else:
            response = Response(json.dumps(valid),
                                mimetype='application/json'), 400
        return response


@app.route("/api/permissions", methods=['DELETE'])
@login_required
@is_admin
def permission_delete():
    """Function which edits permission.
    :return: If permission is binded with any role:
                 {'error': 'Cannot delete!'}
             If request data is invalid:
                 {'status': False, 'error': [list of errors]}, 400
             If all ok:
                 {'status': 'success',
                  'edited_perm_id': 'permission_id'}
    """
    if request.method == 'DELETE' and request.get_json():
        data = request.get_json()

        valid = validator.permission_delete(data)

        if valid['status']:
            if not db.check_permission_deletion(data['permission_id']):
                db.delete_permission_by_id(data['permission_id'])
                response = jsonify(status='success',
                                   deleted_permission=data['permission_id'])
            else:
                response = jsonify(error='Cannot delete!')
        else:
            response = Response(json.dumps(valid),
                                mimetype='application/json'), 400
        return response


@app.route("/api/permissions", methods=['GET'])
@login_required
@is_admin
def permission_get():
    """Function which gets all permissions.
    :return: {'permission_id': 'permission_id', 'action': 'action',
              'modifier': 'modifier', 'description': 'description'}
    """
    resource_id = request.args.get('resource_id')
    permission_tuple = db.get_all_permissions_by_resource(resource_id)
    parsed_json = {}
    if permission_tuple:
        for res in permission_tuple:
            parsed_json.update({'permission_id': res[0],
                                'action': res[1],
                                'modifier': res[2],
                                'description': res[3]})
    return Response(json.dumps(parsed_json), mimetype='application/json')


@app.route("/api/role_permissions", methods=['POST'])
@login_required
@is_admin
def role_permission_post():
    """Function which binds permission with role.
    :return: If request data is not valid:
                 {'status': False, 'error': [list of errors]}
             If all ok:
                 {'added_role_permission_for_role': 'role_id'}
    """
    data = request.get_json()

    valid = validator.role_permission_post(data)

    if valid['status']:
        db.add_role_permission(data['role_id'],
                               data['permission_id'])
        response = jsonify(added_role_permission_for_role=data['role_id'])
    else:
        response = Response(json.dumps(valid),
                            mimetype='application/json'), 400
    return response


@app.route("/api/role_permissions", methods=['PUT'])
@login_required
@is_admin
def role_permission_put():
    """Function which sets list of permission to role. Before sets
       removes all permissions from role.
       :return: If request data is not invalid':
                    {'status': False, 'error': [list of errors]}
                If all ok:
                    {'msg': 'edited permission'}
    """
    data = request.get_json()
    logger.info('Role permission put')

    # valid = validator.role_permission_put(data)

    # if valid['status']:
    db.delete_permissions_by_role_id(data['role_id'])
    for perm_id in data['permission_id']:
        db.add_role_permission(data['role_id'], perm_id)
    response = jsonify(msg='edited permission')
    # else:
    #     response = Response(json.dumps(valid),
    #                         mimetype='application/json'), 400
    return response


# WTF?
@app.route("/api/role_permissions", methods=['DELETE'])
@login_required
@is_admin
def role_permission_delete():
    data = request.get_json()

    valid = validator.role_permission_delete(data)

    if valid['status']:
        if not db.check_role_deletion(data['role_id']):
            db.delete_role_by_id(data['role_id'])
            response = jsonify(status='success',
                               deleted_role=data['role_id'])
        else:
            response = jsonify(error='Cannot delete!')
    else:
        response = Response(json.dumps(valid),
                            mimetype='application/json'), 400
    return response


@app.route("/api/role_permissions", methods=['GET'])
@login_required
@is_admin
def role_permission_get():
    """Function which gets all permissions from database and all actual
       permissions for current role.
       :return: {'actual': [list of actual permissions for role],
                 'all_permissions': [list of all permissions]}
    """
    role_id = request.args.get('role_id')
    permissions_of_role = db.get_role_permission(role_id)
    all_permissions = db.get_all_permissions()
    parsed_json = {}
    if all_permissions:
        parsed_json['all_permissions'] = []
        parsed_json['actual'] = []
        for res in all_permissions:
            parsed_json['all_permissions'].append({'resource_id': res[0],
                                                   'action': res[2],
                                                   'modifier': res[3],
                                                   'description': res[4]})

            parsed_json['actual'] = [({'id': x[0], 'action': x[1],
                                       'modifier': x[2],
                                       'description': x[3]}) for x in
                                     permissions_of_role]

    return Response(json.dumps(parsed_json), mimetype='application/json')


@app.route("/api/all_permissions", methods=['GET'])
@login_required
@is_admin
def get_all_permissions():
    """Handler for sending all created permissions to frontend.

    :return: list of json
    """
    all_permissions = db.get_all_permissions()
    perms_list = []
    if all_permissions:
        for perm in all_permissions:
            perms_list.append({
                'permission_id': perm[0],
                'resource_name': perm[1],
                'action': perm[2],
                'modifier': perm[3],
                'description': perm[4]
            })
    return Response(json.dumps(perms_list), mimetype='application/json')


@app.route("/api/user_roles", methods=['GET', 'POST'])
@login_required
@is_admin
def get_all_users():
    """Function, used to get all users.
       :return: list of users with id, first name, last name, email and role
    """
    if request.method == 'POST' and request.get_json():
        data = request.get_json()

        valid = validator.user_role_post(data)

        if valid['status']:
            db.change_user_role(data['role_id'],
                                data['user_id'])
            response = jsonify(msg='success',
                               added_role=data['role_id'])
        else:
            response = Response(json.dumps(valid),
                                mimetype='application/json'), 400
        return response
    users_tuple = db.get_all_users()
    parsed_json = []
    if users_tuple:
        for res in users_tuple:
            parsed_json.append({'user_id': res[0], 'first_name': res[1],
                                'last_name': res[2], 'email': res[3],
                                'role': res[4]})
    return Response(json.dumps(parsed_json), mimetype='application/json')

@app.route("/api/problems", methods=['GET'])
def problems():
    """
    Function, used to get all problems.
    :return: list of problems with id, title, latitude, longtitude,
    problem type, status and date of creation
    """
    problem_tuple = db.get_all_problems()
    parsed_json = []
    if problem_tuple:
        for problem in problem_tuple:
            parsed_json.append({
                'problem_id':problem[0], 'title':problem[1],
                'latitude':problem[2], 'longtitude':problem[3],
                'problem_type_Id':problem[4], 'status':problem[5],
                'date':problem[6]})
    return Response(json.dumps(parsed_json), mimetype='application/json')


if __name__ == '__main__':
    app.run()
