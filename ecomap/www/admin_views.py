"""Module contains routes, used for admin page."""
import json

from flask import request, jsonify, Response, session
from flask_login import login_required

from ecomap import validator
from ecomap.app import app, logger, auto
from ecomap.db import util as db
from ecomap.permission import permission_control


@app.route("/api/resources", methods=['POST'])
@auto.doc()
@login_required
def resource_post():
    """Function which adds new site resource to site-map in admin panel.

    :rtype: JSON
    :request agrs: `{resource_name: "/res_name"}`
    :return:
        - If there is already resource with this name:
               ``{'error': 'resource already exists'}``
        - If request data is invalid:
              ``{'status': False, 'error': [list of errors]}``
        - If all ok:
              ``{'added_resource': 'resource_name',
              'resource_id': 'resource_id'}``

    :statuscode 400: resource already exists or request is invalid
    :statuscode 200: resource was successfully posted

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
        session['access_control'] = permission_control.reload_dct()
    else:
        response = Response(json.dumps(valid),
                            mimetype='application/json'), 400
    return response


@app.route("/api/resources", methods=['PUT'])
@auto.doc()
@login_required
def resource_put():
    """Function which edits resource name by its id.

    :rtype: JSON
    :request args: `{resource_name: "new_res_name", resource_id: 29}`
    :return:
            - If there is already resource with this name:
                 ``{'error': 'this name already exists'}``
            - If request data is invalid:
                 ``{'status': False, 'error': [list of errors]}``
            - If all ok:
                 ``{'status': 'success', 'edited': 'resource_name'}``

    :statuscode 400: resource already exists or request is invalid
    :statuscode 200: resource was successfully posted

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
        session['access_control'] = permission_control.reload_dct()
    else:
        response = Response(json.dumps(valid),
                            mimetype='application/json'), 400
    return response


@app.route("/api/resources", methods=['DELETE'])
@auto.doc()
@login_required
def resource_delete():
    """Function which deletes resource from database by id.
    Before delete checks if resource have any permissions.

    :rtype: JSON
    :request args: `{resource_id: 29}`
    :return:
        - If resource has assigned permissions:
            ``{'error': 'Cannot delete!'}``
        - If request data is invalid:
            ``{'status': False, 'error': [list of errors]}``
        - If all ok:
            ``{'status': 'success', 'deleted_resource': 'resource_id'}``

    :statuscode 400: if resource has assigned permissions or request invalid
    :statuscode 200: resource was deleted successfully

    """
    data = request.get_json()
    valid = validator.resource_delete(data)

    if valid['status']:
        if not db.check_resource_deletion(data['resource_id']):
            db.delete_resource_by_id(data['resource_id'])
            response = jsonify(status='success',
                               deleted_resource=data['resource_id'])
            session['access_control'] = permission_control.reload_dct()
        else:
            response = jsonify(error='Cannot delete!'), 400
    else:
        response = Response(json.dumps(valid),
                            mimetype='application/json'), 400
    return response


@app.route("/api/resources", methods=['GET'])
@auto.doc()
@login_required
def resource_get():
    """Function which returns resources list from db with pagination options.

    :rtype: JSON
    :query offset: offset number. default is 0
    :query limit: limit number. default is 5
    :return:
        - If resource list is not empty:
            ``[[{"resource_name": "name", "id": 1},
            {"resource_name": "name_2", "id": 2}],
            [{"total_res_count": 2}]]``
        - If there are no resources:
            ``{}``

    :statuscode 200: no errors

    """
    offset = request.args.get('offset') or 0
    per_page = request.args.get('per_page') or 5

    query = db.get_all_resources(offset, per_page)
    count = db.count_resources()
    total_count = {}
    resources = []

    if query:
        for resource in query:
            resources.append({'id': resource[0],
                             'resource_name': resource[1]})
    if count:
        total_count = {'total_res_count': count[0]}

    return Response(json.dumps([resources, [total_count]]),
                    mimetype='application/json')


@app.route("/api/roles", methods=['POST'])
@auto.doc()
@login_required
def role_post():
    """Function which adds new role into database.

    :rtype: JSON
    :request args: `{"role_name":"test"}`
    :return:
        - If there is already role with this name:
            ``{'error': 'role already exists'}``
        - If request data is invalid:
            ``{'status': False, 'error': [list of errors]}``
        - If all ok:
            ``{'added_role': 'role_name',
            'added_role_id': 'role_id'}``

    :statuscode 400: If role with this name exists or request is invalid
    :statuscode 200: If no errors

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
        session['access_control'] = permission_control.reload_dct()
    else:
        response = Response(json.dumps(valid),
                            mimetype='application/json'), 400
    return response


@app.route("/api/roles", methods=['PUT'])
@auto.doc()
@login_required
def role_put():
    """Function which edits role name by it id.

    :rtype: JSON
    :request args: `{role_name: "new_name", role_id: 5}`
    :return:
        - If there is already resource with this name:
            ``{'error': 'this name already exists'}``
        - If request data is invalid:
            ``{'status': False, 'error': [list of errors]}``
        - If all ok:
            ``{'status': 'success', 'edited': 'resource_name'}``

    :statuscode 400: if role with this name exists or request is invalid
    :statuscode 200: if no errors

    """
    data = request.get_json()
    valid = validator.role_put(data)

    if valid['status']:
        if db.get_role_id(data['role_name']):
            return jsonify(error='this name already exists'), 400

        db.edit_role(data['role_name'], data['role_id'])
        response = jsonify(status='success',
                           edited=data['role_name'])
        session['access_control'] = permission_control.reload_dct()
    else:
        response = Response(json.dumps(valid),
                            mimetype='application/json'), 400
    return response


@app.route("/api/roles", methods=['DELETE'])
@auto.doc()
@login_required
def role_delete():
    """Function which deletes role from database by it id.

    :rtype: JSON
    :request args: `{role_id: 5}`
    :return:
        - If role has permissions:
            ``{'error': 'Cannot delete!'}``
        - If request data is invalid:
            ``{'status': False, error: [list of errors]}``
        - If all ok:
            ``{'status': 'success', 'deleted_role': 'role_id'}``

    :statuscode 400: if role has assigned permissions or request invalid
    :statuscode 200: if no errors

    """
    data = request.get_json()

    valid = validator.role_delete(data)

    if valid['status']:
        if not db.check_role_deletion(data['role_id']):
            db.delete_role_by_id(data['role_id'])
            response = jsonify(msg='success',
                                   deleted_role=data['role_id'])
            session['access_control'] = permission_control.reload_dct()
        else:
            response = jsonify(error='Cannot delete!')
    else:
        response = Response(json.dumps(valid),
                            mimetype='application/json'), 400
    return response


@app.route("/api/roles", methods=['GET'])
@auto.doc()
@login_required
def role_get():
    """Function which gets all roles of user from database.

    :rtype: JSON
    :return:
        - If no roles in DB:
            ``{}``
        - If roles exists:
            ``{'role_name': 'role_id',..., 'role_name2': 'role_id'}``

    :statuscode 200: if no errors

    """
    query = db.get_all_roles()
    parsed_data = {}
    if query:
        parsed_data = {res[1]: res[0] for res in query}
    return jsonify(parsed_data)


@app.route("/api/permissions", methods=['POST'])
@auto.doc()
@login_required
def permission_post():
    """Function which adds new permission into database.

    :rtype: JSON
    :request args example: `{action: "DELETE",
        description: "TEST",
        modifier: "None",
        resource_id: "33"}`
    :return:
        - If request data is invalid:
            ``{'status': False, 'error': [list of errors]}``
        - If all ok:
            ``{'added_permission': 'description',
            'permission_id': 'permission_id'}``

    :statuscode 400: invalid request
    :statuscode 200: permission has been successfully added

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
            session['access_control'] = permission_control.reload_dct()
        else:
            response = Response(json.dumps(valid),
                                mimetype='application/json'), 400
        return response


@app.route("/api/permissions", methods=['PUT'])
@auto.doc()
@login_required
def permission_put():
    """Function which edits permission.

    :rtype: JSON
    :request args example: `{action: "POST",
        description: "edited description",
        modifier: "Any",
        resource_id: "33"}`
    :return:
        - If request data is invalid:
            ``{'status': False, 'error': [list of errors]}``
        - If all ok:
            ``{'status': 'success',
            'edited_perm_id': 'permission_id'}``

    :statuscode 400: invalid request
    :statuscode 200: if no errors

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
            session['access_control'] = permission_control.reload_dct()
        else:
            response = Response(json.dumps(valid),
                                mimetype='application/json'), 400
        return response


@app.route("/api/permissions", methods=['DELETE'])
@auto.doc()
@login_required
def permission_delete():
    """Function which deletes permission by it id.

    :rtype: JSON
    :request args example: `{permission_id: 5}`
    :return:
        - If permission was binded to some role:
            ``{'error': 'Cannot delete!'}``
        - If request data is invalid:
            ``{'status': False, 'error': [list of errors]}``
        - If all ok:
            ``{'status': 'success',
            'edited_perm_id': 'permission_id'}``

    :statuscode 400: if role has assigned permissions or request invalid
    :statuscode 200: if no errors

    """
    if request.method == 'DELETE' and request.get_json():
        data = request.get_json()
        valid = validator.permission_delete(data)

        if valid['status']:
            if not db.check_permission_deletion(data['permission_id']):
                db.delete_permission_by_id(data['permission_id'])
                response = jsonify(status='success',
                                   deleted_permission=data['permission_id'])
                session['access_control'] = permission_control.reload_dct()
            else:
                response = jsonify(error='Cannot delete!')
        else:
            response = Response(json.dumps(valid),
                                mimetype='application/json'), 400
        return response


@app.route("/api/permissions", methods=['GET'])
@auto.doc()
@login_required
def permission_get():
    """Function which gets all permissions.

    :rtype: JSON
    :query resource_id: id of site resource(int)

    :return:
        - If resource list is not empty for this id:
            ``{'permission_id': 'permission_id', 'action': 'action',
            'modifier': 'modifier', 'description': 'description'}``
        - If there are no permissions for selected resource_id:
            ``{}``

    :statuscode 200: no errors

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
@auto.doc()
@login_required
def role_permission_post():
    """Function which binds permission with role.

    :rtype: JSON
    :request args example: `{permission_id: 5, role_id: 4}`
    :return:
        - If request data is not valid:
            ``{'status': False, 'error': [list of errors]}``
        - If all ok:
            ``{'added_role_permission_for_role': 'role_id'}``

    :statuscode 400: if role has assigned permissions or request invalid
    :statuscode 200: if no errors

    """
    data = request.get_json()
    valid = validator.role_permission_post(data)

    if valid['status']:
        db.add_role_permission(data['role_id'],
                               data['permission_id'])
        response = jsonify(added_role_permission_for_role=data['role_id'])
        session['access_control'] = permission_control.reload_dct()
    else:
        response = Response(json.dumps(valid),
                            mimetype='application/json'), 400
    return response


@app.route("/api/role_permissions", methods=['PUT'])
@auto.doc()
@login_required
def role_permission_put():
    """Function which sets list of permission to role. Before sets
    removes all permissions from role.

    :rtype: JSON
    :request args example: `{permission_id: 5, role_id: 4}`
    :return:
        - If request data is not invalid':
            ``{'status': False, 'error': [list of errors]}``
        - If all ok:
            ``{'msg': 'edited permission'}``

    """
    data = request.get_json()
    logger.info('Role permission has been changed.')

    db.delete_permissions_by_role_id(data['role_id'])
    for perm_id in data['permission_id']:
        db.add_role_permission(data['role_id'], perm_id)
    response = jsonify(msg='edited permission')
    session['access_control'] = permission_control.reload_dct()
    return response


@app.route("/api/role_permissions", methods=['DELETE'])
@auto.doc()
@login_required
def role_permission_delete():
    """Function to delete permissions by role id.

    :rtype: JSON
    :request args example: `{role_id: 4}`
    :return:
        - If request data is not invalid':
            ``{'status': False, 'error': [list of errors]}``
        - If all ok:
            ``{'msg': 'deleted permission'}``

    """
    data = request.get_json()

    valid = validator.role_permission_delete(data)

    if valid['status']:
        if not db.check_role_deletion(data['role_id']):
            db.delete_role_by_id(data['role_id'])
            response = jsonify(status='success',
                               deleted_role=data['role_id'])
            session['access_control'] = permission_control.reload_dct()
        else:
            response = jsonify(error='Cannot delete!')
    else:
        response = Response(json.dumps(valid),
                            mimetype='application/json'), 400
    return response


@app.route("/api/role_permissions", methods=['GET'])
@auto.doc()
@login_required
def role_permission_get():
    """Function which gets all permissions from database and all actual
    permissions for current role.

    :query role_id: set specific id of user role for showing its actual list
     of permissions

    :return:
        ``{'actual': [list of actual permissions for role],
        'all_permissions': [list of all permissions]}``
    :rtype: JSON

    """
    role_id = request.args.get('role_id')
    permissions_of_role = db.get_role_permission(role_id)
    all_permissions = db.get_all_permission_list()
    parsed_json = {}
    if all_permissions:
        parsed_json['all_permissions'] = []
        parsed_json['actual'] = []
        for res in all_permissions:
            parsed_json['all_permissions'].append({'resource_id': res[0],
                                                   'action': res[2],
                                                   'modifier': res[3],
                                                   'description': res[4]})

            parsed_json['actual'] = [({'permission_id': x[0], 'action': x[1],
                                       'modifier': x[2],
                                       'description': x[3]}) for x in
                                     permissions_of_role]

    return Response(json.dumps(parsed_json), mimetype='application/json')


@app.route("/api/all_permissions", methods=['GET'])
@auto.doc()
@login_required
def get_all_permissions():
    """Function sends all created permissions to frontend. Handles with
    pagination options defined in query arguments.

    :rtype: JSON
    :query offset: pgination offset number. default is 0
    :query limit: pagination limit number. default is 5
    :return:
        - If permission tuple from DB is not empty:
            ``[[{"action": "POST", "permission_id": 6,
            "resource_name": "/api/register",
            "modifier": "Any",
            "description": "register user into app"}],
            [{"total_perm_count": 46}]]``
        - If there are no permissions:
            ``{}``

    :statuscode 200: no errors

    """
    offset = request.args.get('offset') or 0
    per_page = request.args.get('per_page') or 5

    count = db.count_permissions()
    all_permissions = db.get_all_permissions(offset, per_page)
    permissions = []
    total_count = {}

    if all_permissions:
        for perm in all_permissions:
            permissions.append({
                'permission_id': perm[0],
                'resource_name': perm[1],
                'action': perm[2],
                'modifier': perm[3],
                'description': perm[4]})
    if count:
        total_count = {'total_perm_count': count[0]}
    return Response(json.dumps([permissions, [total_count]]),
                    mimetype='application/json')


@app.route("/api/user_roles", methods=['GET', 'POST'])
@auto.doc()
@login_required
def get_all_users():
    """Function, used to get all users.

    :return: list of all users with id, first name, last name, email and role

    ``[{"role": "admin", "first_name": "Admin", "last_name": "Administrator",
    "user_id": 3, "email": "admin@ecomap.com"}
    ...
    {"role": "user", "first_name": "Oleg", "last_name": "Lyashko",
    "user_id": 4, "email": "radical@gmail.com"}``

    :statuscode 200: no errors
    :statuscode 400: invalid request


    """
    if request.method == 'POST' and request.get_json():
        data = request.get_json()

        valid = validator.user_role_put(data)

        if valid['status']:
            db.change_user_role(data['role_id'],
                                data['user_id'])
            response = jsonify(msg='success',
                               added_role=data['role_id'])
            session['access_control'] = permission_control.reload_dct()
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


@app.route('/api/editResource/<int:page_id>', methods=['PUT'])
@auto.doc()
@login_required
def edit_page(page_id):
    """This method makes changes to given page(ex-resource) via
    page_id, passed to it.

    :param page_id: id of specific page to edit.

    :request agrs example: `{'id': 1, 'title': 'title', 'alias': 'tag',
       'description': 'small description of page',
       'content': 'main article content',
       'meta_keywords': 'keyword1, keyword2',
       'meta_description': 'meta-description of content',
       'is_enabled': 1}`

    :return: confirmation object
    :rtype: JSON
    :JSON sample:
       ``{'result': true}``
       or
       ``{'result': false}``

    :statuscode 200: successfully edited
    :statuscode 404: no page by given id

    """
    if request.method == 'PUT' and request.get_json():
        data = request.get_json()
        result = False
        status_code = 404
        if db.get_page_by_id(data['id']):
            db.edit_page(page_id, data['title'], data['alias'],
                         data['description'], data['content'],
                         data['meta_keywords'], data['meta_description'],
                         data['is_enabled'])
            result = True
            status_code = 200
        return jsonify(result=result), status_code


@app.route('/api/addResource', methods=['POST'])
@auto.doc()
@login_required
def add_page():
    """This method adds new page to db.

    :rtype: JSON
    :request agrs: `{'title': 'new page', 'alias': 'tag',
                    'description': 'short description of page',
                    'content': 'main article content',
                    'meta_keywords': 'keyword1, keyword2',
                    'meta_description': 'meta-description of content',
                    'is_enabled': 1}`

    :return:
        - If there is already page with this name:
               ``{'result': 'False', 'msg': 'Page already exists!'}``
        - If request data is invalid:
              ``{'result': 'False', 'msg': 'Couldn't add new page!'}``
        - If all ok:
              ``{'result': 'True', 'msg': 'Succesfully added!'}``

    :statuscode 200: check status in response json object

    """

    result = None
    msg = None
    if request.method == 'POST' and request.get_json():
        data = request.get_json()
        if not db.get_page_by_alias(data['alias']):
            db.add_page(data['title'], data['alias'],
                        data['description'], data['content'],
                        data['meta_keywords'], data['meta_description'],
                        data['is_enabled'])
            if db.get_page_by_alias(data['alias']):
                result = True
                msg = 'Succesfully added!'
            else:
                result = False
                msg = "Couldn't add new page!"
        else:
            result = False
            msg = 'Page already exists!'
    return jsonify(result=result, msg=msg)


@app.route('/api/deleteResource/<page_id>', methods=['DELETE'])
@auto.doc()
@login_required
def delete_page(page_id):
    """This method deletes page by it's id.

    :param page_id: id of specific page to delete.

    :request agrs example: `{'id': 1}`

    :return: confirmation object
    :rtype: JSON
    :JSON sample:
       ``{'result': true, 'msg': 'Page was deleted successfully!'}``
    or
       ``{'result': false, 'msg': 'Couldn't delete the page'}``

    :statuscode 200: successfully edited
    :statuscode 404: no page by given id

    """

    msg = None
    result = None
    if request.method == 'DELETE':
        db.delete_page_by_id(page_id)
        if not db.get_page_by_id(page_id):
            result = True
            msg = 'Page was deleted successfully!'
        else:
            result = False
            msg = 'Couldn\'t delete the page!'
    return jsonify(result=result, msg=msg)


@app.route("/api/user_page", methods=['GET'])
@auto.doc()
@login_required
def get_all_users_info():
    """Function which returns users list from db with pagination options.

    :rtype: JSON
    :query offset: pagination offset number. default is 0
    :query limit: pagination limit number. default is 5
    :return:
        ``[[{"role_name": "admin",
        "first_name": "username",
        "last_name": "UserSurname",
        "id": 1,
        "email": "email@name.ru"},
        ....
        {"role_name": "user",
        "first_name": "Username",
        "last_name": "UserSurname",
        "id": 5,
        "email": "email@gmail.com"}],
        [{"total_users": 2}]]``

    :statuscode 200: no errors

    """
    offset = request.args.get('offset') or 0
    per_page = request.args.get('per_page') or 5

    query = db.get_users_pagination(offset, per_page)
    count = db.count_users()
    total_count = {}
    users = []

    if query:
        for user_data in query:
            users.append({'id': user_data[0], 'first_name': user_data[1],
                          'last_name': user_data[2],
                          'email': user_data[3],
                          'role_name': user_data[4]})
    if count:
        total_count = {'total_users': count[0]}

    return Response(json.dumps([users, [total_count]]),
                    mimetype='application/json')


@app.route('/api/problem_type', methods=['GET'])
@auto.doc()
@login_required
def get_problem_type():
    '''The method retrieves all probleme types.
       :rtype: JSON.
       :return: json object with problem types.
    '''
    problem_type_tuple = db.get_problem_type()
    problem_type_list = []
    if problem_type_tuple:
        for problem in problem_type_tuple:
            problem_type_list.append({'id': problem[0],
                                     'picture': problem[1],
                                      'name': problem[2],
                                      'radius': problem[3]
                                      })
    response = Response(json.dumps(problem_type_list),
                        mimetype='application/json')
    return response


@app.route('/api/problem_type', methods=['DELETE'])
@auto.doc()
@login_required
def delete_problem_type():
    '''The method retrieves all probleme types.
       :rtype: JSON.
       :return: Message if .
    '''
    data = request.get_json()
    db.delete_problem_type(data['problem_type_id'])
    if not db.get_problem_type_by_id(data['problem_type_id']):
        response = jsonify(msg='Success')
    else:
        response = jsonify(error='Cannot delete!')
    return response
