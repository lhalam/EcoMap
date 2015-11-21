# coding=utf-8
"""
This module holds all views controls for
ecomap project.
"""
import json
import functools

from flask import render_template, request, jsonify, Response, g, abort
from flask_login import login_user, logout_user, login_required, current_user

import ecomap.user as usr

from ecomap.app import app, logger
from ecomap.db import util as db
from ecomap import validator as v


@app.before_request
def load_users():
    if current_user.is_authenticated:
        g.user = current_user
        logger.warning(g.user)
    else:
        anon = usr.Anonymous()
        g.user = anon.username
        logger.warning(g.user)


def is_admin(f):
    @functools.wraps(f)
    def wrapped(*args, **kwargs):
        logger.warning(g.user)
        logger.warning('SIC!')
        logger.warning(g.user.role)
        if g.user.role != 'admin':
            abort(403)
        return f(*args, **kwargs)
    return wrapped


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

    return:
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
    # todo change debug error messages
    response = jsonify(), 401
    if request.method == 'POST' and request.get_json():
        data = request.get_json()

        valid = v.main_validator([[data, 'password', 6, 100, v.validate_key,
                                   v.validate_empty, v.validate_string,
                                   v.validate_length],
                                  [data, 'email', 1, 100, v.validate_key,
                                   v.validate_empty, v.validate_string,
                                   v.validate_length, v.validate_email]])

        if not valid:
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
            response = Response(json.dumps({'error': valid}),
                                mimetype='application/json')
    return response


@app.route('/api/change_password', methods=['POST'])
@login_required
def change_password():
    if request.method == 'POST':
        data = request.get_json()

        valid = v.main_validator([[data, 'id', 1, 100, v.validate_key,
                                   v.validate_empty],
                                  [data, 'old_pass', 1, 100, v.validate_key,
                                   v.validate_empty, v.validate_string,
                                   v.validate_length],
                                  [data, 'new_pass', 1, 100, v.validate_key,
                                   v.validate_empty, v.validate_string,
                                   v.validate_length]])

        if not valid:
            user = usr.get_user_by_id(data['id'])
            if user and user.verify_password(data['old_pass']):
                user.change_password(data['new_pass'])
                return jsonify(), 200
            return jsonify(), 400
        return Response(json.dumps({'error': valid}),
                        mimetype='application/json')


@app.route('/api/logout', methods=['POST', 'GET'])
@login_required
def logout():
    """Method for user's log out.

    return:
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

    return:
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
    # TODO get back login logic to server
    # todo ?pass confirm on server logic
    response = jsonify(msg='unauthorized'), 400
    if request.method == 'POST' and request.get_json():
        data = request.get_json()

        valid = v.main_validator([[data, 'email', 2, 100, v.validate_key,
                                   v.validate_empty, v.validate_string,
                                   v.validate_length, v.validate_email],
                                  [data, 'firstName', 2, 100, v.validate_key,
                                   v.validate_empty, v.validate_string,
                                   v.validate_length],
                                  [data, 'lastName', 2, 100, v.validate_key,
                                   v.validate_empty, v.validate_string,
                                   v.validate_length],
                                  [data, 'password', 2, 100, v.validate_key,
                                   v.validate_empty, v.validate_string,
                                   v.validate_length],
                                  [data, 'pass_confirm', 2, 100,
                                   v.validate_key, v.validate_empty,
                                   v.validate_string, v.validate_length]])

        if not valid:
            if not usr.get_user_by_email(data['email']):
                usr.register(data['firstName'], data['lastName'],
                             data['email'], data['password'])
                msg = 'added %s %s' % (data['firstName'], data['lastName'])
                response = jsonify({'status_message': msg}), 201
            else:
                msg = 'user with this email already exists'
                response = jsonify({'status_message': msg}), 401
        else:
            response = Response(json.dumps({'error': valid}),
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


@app.route("/api/resources", methods=['GET', 'POST', 'PUT', 'DELETE'])
@login_required
@is_admin
def resources():
    """Get list of site resources needed for administration
    and server permission control.
    method PUT:
    'resource_name' = changes to name of the resource.
    'resource_id' = key to search name of the resource in db.
    method POST:
    'resource_name' = adds a new resource with this name.
    method DELETE:
    'resource_name' = that has to be Deleted.
    'resource_id' = key to search name of resource in db to delete.

       :return:
            - list of jsons
            - if no such resource in DB
                return empty json
    """
    if request.method == 'POST' and request.get_json():
        data = request.get_json()

        valid = v.main_validator([[data, 'resource_name', 2, 100,
                                  v.validate_key, v.validate_empty]])

        if not valid:
            if db.get_resource_id(data['resource_name']):
                return jsonify(error='Resource already exists'), 400

            db.add_resource(data['resource_name'])
            added_res_id = db.get_resource_id(data['resource_name'])
            response = jsonify(added_resource=data['resource_name'],
                               resource_id=added_res_id[0])
        else:
            response = Response(json.dumps({'error': valid}),
                                mimetype='application/json'), 400
        return response

    # todo change unique handler to ajax?
    if request.method == 'PUT' and request.get_json():
        data = request.get_json()

        valid = v.main_validator([[data, 'new_resource_name', 2, 100,
                                   v.validate_key, v.validate_empty,
                                   v.validate_string, v.validate_length],
                                  [data, 'resource_id', 1, 100, v.validate_key,
                                   v.validate_empty]])

        if not valid:
            if db.get_resource_id(data['resource_name']):
                return jsonify(error='this name already exists'), 400

            db.edit_resource_name(data['new_resource_name'],
                                  data['resource_id'])
            response = jsonify(status='success',
                               edited=data['new_resource_name'])
        else:
            response = Response(json.dumps({'error': valid}),
                                mimetype='application/json'), 400
        return response

    if request.method == 'DELETE' and request.get_json():
        del_data = request.get_json()

        valid = v.main_validator([[del_data, 'resource_id', 1, 100,
                                   v.validate_key, v.validate_empty]])

        if not valid:
            if not db.check_resource_deletion(del_data['resource_id']):
                db.delete_resource_by_id(del_data['resource_id'])
                response = jsonify(msg='success',
                                   deleted_resource=del_data['resource_id'])
            else:
                response = jsonify(error='Cannot delete!')
        else:
            response = Response(json.dumps({'error': valid}),
                                mimetype='application/json'), 400
        return response

    query = db.get_all_resources()
    parsed_data = {}
    if query:
        parsed_data = {res[1]: res[0] for res in query}
    return jsonify(parsed_data)


@app.route("/api/roles", methods=['GET', 'POST', 'PUT', 'DELETE'])
@login_required
@is_admin
def roles():
    """NEW!
    get list of roles for server permission control.
    action GET:
    'role_name' = name of role in db.
    action POST:
    'role_name' = name of the role.
    action PUT:
    'role_name' = changes to name of the role
    'role_id' = key to search name of the role in db
    action DELETE:
    'role_name' = that has to be Deleted
    'role_id' = key to search name of resource in db to delete
       :return:
            - list of jsons(dicts)
            - if no resource in DB
                return empty dict
    """
    if request.method == 'POST' and request.get_json():
        data = request.get_json()

        valid = v.main_validator([[data, 'role_name', 2, 100,
                                  v.validate_key, v.validate_empty,
                                  v.validate_string, v.validate_length]])

        if not valid:
            if db.get_role_id(data['role_name']):
                return jsonify(error='role already exists'), 400

            db.insert_role(data['role_name'])
            added_role_id = db.get_role_id(data['role_name'])

            response = jsonify(added_role=data['role_name'],
                               added_role_id=added_role_id[0])
        else:
            response = Response(json.dumps({'error': valid}),
                                mimetype='application/json'), 400
        return response

    if request.method == 'PUT' and request.get_json():
        edit_data = request.get_json()

        valid = v.main_validator([[edit_data, 'new_role_name', 2, 100,
                                   v.validate_key, v.validate_empty,
                                   v.validate_string, v.validate_length],
                                  [edit_data, 'role_id', 2, 100,
                                   v.validate_key, v.validate_empty,
                                   v.validate_string, v.validate_length]])

        if not valid:
            if db.get_role_id(edit_data['role_name']):
                return jsonify(error='this name already exists'), 400

            db.edit_role(edit_data['new_role_name'], edit_data['role_id'])
            response = jsonify(msg='success',
                               edited=edit_data['new_role_name'])
        else:
            response = Response(json.dumps({'error': valid}),
                                mimetype='application/json'), 400
        return response

    if request.method == 'DELETE' and request.get_json():
        del_data = request.get_json()

        valid = v.main_validator([[del_data, 'role_id', 1, 100, v.validate_key,
                                  v.validate_empty]])

        if not valid:
            if not db.check_role_deletion(del_data['role_id']):
                db.delete_role_by_id(del_data['role_id'])
                response = jsonify(msg='success',
                                   deleted_role=del_data['role_id'])
            else:
                response = jsonify(error='Cannot delete!')
        else:
            response = Response(json.dumps({'error': valid}),
                                mimetype='application/json'), 400
        return response

    query = db.get_all_roles()
    parsed_data = {}
    if query:
        parsed_data = {res[1]: res[0] for res in query}
    return jsonify(parsed_data)


@app.route("/api/permissions", methods=['GET', 'PUT', 'POST', 'DELETE'])
@login_required
@is_admin
def permissions():
    """Controller used for mange getting and adding actions of
    server permission options.

       :return:
            - list of lists with permission data
                [id,action,modifier,resource)
            - if no resource in DB
                return empty json
    """

    if request.method == 'POST' and request.get_json():
        data = request.get_json()

        valid = v.main_validator([[data, 'resource_id', 1, 100,
                                   v.validate_key, v.validate_empty],
                                  [data, 'action', 3, 7, v.validate_key,
                                   v.validate_empty, v.validate_string,
                                   v.validate_length],
                                  [data, 'modifier', 3, 5, v.validate_key,
                                   v.validate_empty, v.validate_string,
                                   v.validate_length],
                                  [data, 'description', 1, 256, v.validate_key,
                                   v.validate_empty, v.validate_string,
                                   v.validate_length]])

        if not valid:
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
            response = Response(json.dumps({'error': valid}),
                                mimetype='application/json'), 400
        return response

    if request.method == 'PUT' and request.get_json():
        edit_data = request.get_json()

        valid = v.main_validator([[edit_data, 'new_action', 3, 7,
                                   v.validate_key, v.validate_empty,
                                   v.validate_string, v.validate_length],
                                  [edit_data, 'new_modifier', 3, 5,
                                   v.validate_key, v.validate_empty,
                                   v.validate_string, v.validate_length],
                                  [edit_data, 'new_description', 1, 256,
                                   v.validate_key, v.validate_empty,
                                   v.validate_string, v.validate_length],
                                  [edit_data, 'permission_id', 1, 100,
                                   v.validate_key, v.validate_empty]])

        if not valid:
            db.edit_permission(edit_data['new_action'],
                               edit_data['new_modifier'],
                               edit_data['permission_id'],
                               edit_data['new_description'])
            response = jsonify(msg='success',
                               edited_perm_id=edit_data['permission_id'])
        else:
            response = Response(json.dumps({'error': valid}),
                                mimetype='application/json'), 400
        return response

    if request.method == 'DELETE' and request.get_json():
        data = request.get_json()

        valid = v.main_validator([[data, 'permission_id', 1, 100,
                                   v.validate_key, v.validate_empty]])

        if not valid:
            if not db.check_permission_deletion(data['permission_id']):
                db.delete_permission_by_id(data['permission_id'])
                response = jsonify(msg='success',
                                   deleted_permission=data['permission_id'])
            else:
                response = jsonify(error='Cannot delete!')
        else:
            response = Response(json.dumps({'error': valid}),
                                mimetype='application/json'), 400
        return response

    resource_id = request.args.get('resource_id')
    permission_tuple = db.get_all_permissions_from_resource(resource_id)
    parsed_json = {}
    if permission_tuple:
        for res in permission_tuple:
            parsed_json.update({'permission_id': res[0], 'action': res[1],
                                'modifier': res[2], 'description': res[3]})
    return Response(json.dumps(parsed_json), mimetype='application/json')


@app.route("/api/role_permissions", methods=['GET', 'PUT', 'POST'])
@login_required
@is_admin
def get_role_permission():
    """
    Handler for assigning permissions to role.
    method GET:
        - returns JSON with all permissions of role
            and with actual selected permissions.
    method POST:

    """
    if request.method == 'POST' and request.get_json():
        data = request.get_json()

        valid = v.main_validator([[data, 'role_id', 1, 100, v.validate_key,
                                   v.validate_empty],
                                  [data, 'permission_id', 1, 100,
                                   v.validate_key, v.validate_empty]])

        if not valid:
            db.add_role_permission(data['role_id'],
                                   data['permission_id'])
            response = jsonify(added_role_permission_for=data['role_id'])
        else:
            response = Response(json.dumps({'error': valid}),
                                mimetype='application/json'), 400
        return response

    if request.method == 'PUT' and request.get_json():
        edit_data = request.get_json()

        valid = v.main_validator([[edit_data, 'role_id', 1, 100,
                                   v.validate_key, v.validate_empty],
                                  [edit_data, 'permission_id', 1, 100,
                                   v.validate_key, v.validate_empty]])

        if not valid:
            db.delete_permissions_by_role_id(edit_data['role_id'])
            for id in edit_data['permission_id']:
                db.add_role_permission(edit_data['role_id'], id)
            response = jsonify(msg='edited permission')
        else:
            response = Response(json.dumps({'error': valid}),
                                mimetype='application/json'), 400
        return response

    if request.method == 'DELETE' and request.get_json():
        del_data = request.get_json()

        valid = v.main_validator([[del_data, 'role_id', 1, 100, v.validate_key,
                                   v.validate_empty]])

        if not valid:
            if not db.check_role_deletion(del_data['role_id']):
                db.delete_role_by_id(del_data['role_id'])
                response = jsonify(status='success',
                                   deleted_role=del_data['role_id'])
            else:
                response = jsonify(error='Cannot delete!')
        else:
            response = Response(json.dumps({'error': valid}),
                                mimetype='application/json'), 400
        return response

    role_id = request.args.get('role_id')
    permissions_of_role = db.get_role_permission(role_id)
    all_permissions = db.get_all_permissions()
    parsed_json = {}
    if all_permissions:
        parsed_json['all_permissions'] = []
        parsed_json['actual'] = []
        for res in all_permissions:
            parsed_json['all_permissions'].append({'id': res[0],
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


@app.route('/api/getTitles', methods=['GET'])
def get_titles():
    """This method returns short info about all defined static pages.

      :returns list of dicts with title, id, alias and is_enabled
      values.
    """
    if request.method == 'GET':
        pages = db.get_pages_titles()
        result = []
        if pages:
            for page in pages:
                result.append({'id': page[0],
                               'title': page[1],
                               'alias': page[2],
                               'is_enabled': page[3]})
        return Response(json.dumps(result), mimetype="application/json")


@app.route('/api/resources/<alias>', methods=['GET'])
def get_faq(alias):
    """This method retrieves exact faq page(ex-resource) via
       alias, passed to it.

        :params - alias - url path to exact page.

        :returns object with all page's attributes within a list.
    """
    if request.method == 'GET':
        page = db.get_page_by_alias(alias)
        status_code = None
        result = None
        if page:
            result = [{'id': page[0],
                       'title': page[1],
                       'alias': page[2],
                       'description': page[3],
                       'content': page[4],
                       'meta_keywords': page[5],
                       'meta_description': page[6],
                       'is_enabled': page[7]}]
            status_code = 200
        else:
            result = []
            status_code = 404
        return Response(json.dumps(result), mimetype="application/json",
                        status=status_code)


@app.route('/api/editResource/<int:page_id>', methods=['PUT'])
@login_required
@is_admin
def edit_page(page_id):
    """This method makes changes to given page(ex-resource).

        :returns confirmation.
    """
    if request.method == 'PUT':
        data = request.get_json()
        status_code = None
        result = None
        if db.get_page_by_alias(data['alias']):
            db.edit_page(page_id, data['title'], data['alias'],
                         data['description'], data['content'],
                         data['meta_keywords'], data['meta_description'],
                         data['is_enabled'])
            result = True
            status_code = 200
        else:
            result = False
            status_code = 404
        return jsonify(result), status_code


if __name__ == '__main__':
    app.run()
