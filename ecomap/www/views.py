# coding=utf-8
"""
This module holds all views controls for
ecomap project.
"""
import json

from flask import render_template, request, jsonify, Response
from flask_login import login_user, logout_user, login_required

import ecomap.user as usr

from ecomap.app import app, logger
from ecomap.db import util as db
from ecomap.db.db_pool import DBPoolError
from ecomap.utils import Validators as v, validate


@app.route("/", methods=['GET'])
def index():
    """Controller starts main application page.

    return: renders html template with angular app.
    """
    return render_template("index.html")


@app.route("/api/login", methods=["POST"])
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
    if request.method == "POST" and request.get_json():
        data = request.get_json()

        validation = validate(data, validators=(
            {'password': [v.is_string, v.max_l(30),
                          v.min_l(6), v.required, v.no_spaces]},
            {'email': [v.required, v.no_spaces, v.max_l(30),
                       v.email_pattern]}))
        if not validation['errors']:

            user = usr.get_user_by_email(data['email'])
            if user and user.verify_password(data['password']):
                login_user(user, remember=True)
                response = jsonify(id=user.uid,
                                   name=user.first_name,
                                   surname=user.last_name,
                                   role='???', iat="???",
                                   token=user.get_auth_token(),
                                   email=user.email)
            if not user:
                logger.warning('if not user')
                response = jsonify(error="There is no user with given email.",
                                   logined=0, ), 401
            elif not user.verify_password(data['password']):
                logger.warning('if not user verify')
                response = jsonify(error="Invalid password, try again.",
                                   logined=0), 401

        else:
            response = Response(json.dumps(validation['errors']),
                                mimetype='application/json')
    return response


@app.route("/api/change_password", methods=["POST"])
@login_required
def change_password():
    if request.method == 'POST':
        data = request.get_json()
        validation = validate(data, validators=(
            {'id': [v.required]},
            {'old_pass': [v.required, v.min_l(6)]},
            {'new_pass': [v.required, v.min_l(6), v.no_spaces]}))
        if not validation['errors']:

            user = usr.get_user_by_id(data['id'])
            if user and user.verify_password(data['old_pass']):
                user.change_password(data['new_pass'])
                return jsonify(), 200
        return jsonify(validation['errors']), 401


@app.route("/api/logout", methods=["POST", 'GET'])
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


@app.route("/api/register", methods=["POST"])
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
        validation = validate(data, validators=(
            {'firstName': [v.is_string, v.max_l(30),
                           v.min_l, v.required, v.no_spaces]},
            {'email': [v.required, v.no_spaces, v.max_l(30),
                       v.email_pattern]},
            {'lastName': [v.is_string, v.max_l(30),
                          v.min_l, v.required, v.no_spaces]},
            {'password': [v.is_string, v.max_l(30),
                          v.min_l(6), v.required, v.no_spaces]},
            {'pass_confirm': [v.is_string, v.max_l(30),
                              v.min_l(6), v.required, v.no_spaces]}))
        if not validation['errors']:

            if not usr.get_user_by_email(data['email']):
                usr.register(data['firstName'], data['lastName'],
                             data['email'], data['password'])
                msg = 'added %s %s' % (data['firstName'], data['lastName'])
                response = jsonify({'status_message': msg}), 201
            else:
                msg = 'user with this email already exists'
                response = jsonify({'status_message': msg}), 401
        else:
            response = Response(json.dumps(validation['errors']),
                                mimetype='application/json'), 400
    return response


@app.route("/api/email_exist", methods=['POST'])
def email_exist():
    """Function for AJAX call from frontend.
    Validates unique email identifier before registering a new user

    :return: json with status 200 or 400
    """
    if request.method == "POST" and request.get_json():
        data = request.get_json()
        user = usr.get_user_by_email(data['email'])
        return jsonify(isValid=bool(user))


@app.route("/api/user_detailed_info/<int:user_id>")
def get_user_info(user_id):
    """This method returns json object with user data."""
    if request.method == 'GET':
        user = usr.get_user_by_id(user_id)
        if user:
            return jsonify(name=user.first_name, surname=user.last_name,
                           email=user.email, role="user")
        else:
            return jsonify(status="There is no user with given email"), 401


@app.route("/api/problems", methods=['GET'])
def get_problems():
    """
    Get all moderated problems in
     brief (id, title, coordinates, type and status);

    return: list of jsons
    """
    data = [
        {
            'id': 1,
            'title': 'xxxx',
            'Title': "Xxxxxxx",
            'Latitude': 45.350166,
            'Longtitude': 29.001091,
            'ProblemTypes_Id': 4,
            'Status': 1,
            'Date': '2014-02-18T07:15:51.000Z'
        },
    ]
    return Response(json.dumps(data), mimetype='application/json')


@app.route("/api/problems/<int:id>", methods=['GET'])
def get_problems_by_id(id):
    """Get detailed problem description.
    (all information from tables 'Problems', 'Activities', 'Photos')
    by it's id;
    """

    data = [
        [
            {
                "Id": 5,
                "Title": "Загрязнение Днепра",
                "Content": "В городе Берислав нет "
                           "очистных сооружений.",
                "Proposal": "",
                "Severity": 3,
                "Moderation": 1,
                "Votes": 13,
                "Latitude": 46.8326,
                "Longtitude": 33.416462,
                "Status": 0,
                "ProblemTypes_Id": 4
            }
        ],
        [],
        [
            {
                "Id": 5,
                "Content": "{\"Content\":\"Проблему "
                           "додано анонімно\",\"userName\""
                           ":\"(Анонім)\"}",
                "Date": "2014-02-27T15:24:53.000Z",
                "ActivityTypes_Id": 1,
                "Users_Id": 2,
                "Problems_Id": 5
            }
        ]
    ] if id == 1 else {'data': 'select ID=1'}
    return Response(json.dumps(data), mimetype='application/json')


@app.route("/api/users/<int:idUser>", methods=['GET'])
def get_user_by_id(idUser):
    """
    get user's name and surname by id;
    :return
        - JSON with user's name and surname or
            empty JSON if there is no
            user with selected id
    """

    data = dict(json=[
        {
            "Name": "admin",
            "Surname": None
        }
    ], length=1) if idUser == 1 else {}

    return jsonify(data)


@app.route("/api/usersProblem/<int:id>", methods=['GET'])
def get_users_problems(id):
    """
    Get all user's problems in brief
    (id, title, coordinates, type and status) by user's id;
    :return
        - returns array of user's problems and empty array
        if there is no user with such id
    """

    data = [
        dict(Id=190,
             Title="назва3333",
             Latitude=51.419765,
             Longtitude=29.520264,
             ProblemTypes_Id=1,
             Status=0,
             Date="2015-02-24T14:27:22.000Z")
    ] if id == 1 else []

    return Response(json.dumps(data), mimetype='application/json')


@app.route("/api/activities/<int:idUser>", methods=['GET'])
def get_user_activities(idUser):
    """
    get all user's activity
    (id, type, description and id of related problem);
    :return: json
    """
    data = dict(
        id=1,
        type='activitytype',
        description='description',
        problem_id=2
    ) if idUser == 1 else {}
    return jsonify(data)


@app.route("/api/problempost", methods=['POST'])
def post_problem():
    """
    post new detailed environment problem to the server
    Request Content-Type: multipart/form-data;

    Request parameters:
    title   optional
    content optional
    proposal    optional
    latitude    optional
    longitude   optional
    type    1-6, required
    userId  optional
    userName    optional
    userSurname optional

       :return: json Content-type: application/json;charset=UTF-8
    """
    if request.method == 'POST' and request.form:
        input_data = request.form
        try:
            input_data['type']
        except KeyError:
            logger.warning('no required parameter')
            return jsonify(err="ER_BAD_NULL_ERROR"), 500
        try:
            int(input_data['userId'])
        except ValueError:
            logger.warning('user id not a int')
            return jsonify(Response='500 Internal Server Error'), 500
        except KeyError:
            pass
        output = {
            "json": {
                'test': input_data['type'],
                "fieldCount": 0,
                "affectedRows": 1,
                "insertId": 191,
                "serverStatus": 2,
                "warningCount": 0,
                "message": u"\u0000",
                "protocol41": True,
                "changedRows": 0
            }
        }
        return jsonify(output)


@app.route("/api/resources", methods=['GET', 'POST', 'PUT', 'DELETE'])
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
    if request.method == "POST" and request.get_json():
        data = request.get_json()
        validation = validate(data, validators=(
            {'resource_name': [v.required]}))
        if not validation['errors']:
            try:
                db.add_resource(data['resource_name'])
                added_res_id = db.get_resource_id(data['resource_name'])
            except DBPoolError:
                return jsonify(error="Resource already exists"), 400

            response = jsonify(added_resource=data['resource_name'],
                               resource_id=added_res_id[0])
        else:
            response = Response(json.dumps(validation['errors']),
                                mimetype='application/json'), 400
        return response

    # todo change unique handler to ajax?
    if request.method == "PUT" and request.get_json():
        data = request.get_json()
        validation = validate(data, validators=(
            {'new_resource_name': [v.required]},
            {'resource_id': [v.required]}))
        if not validation['errors']:
            try:
                db.edit_resource_name(data['new_resource_name'],
                                      data['resource_id'])
            except DBPoolError:
                return jsonify(error="this name already exists"), 400

            response = jsonify(status="success",
                               edited=data['new_resource_name'])
        else:
            response = Response(json.dumps(validation['errors']),
                                mimetype='application/json'), 400
        return response

    if request.method == "DELETE" and request.get_json():
        del_data = request.get_json()
        validation = validate(del_data, validators=(
            {'resource_id': [v.required]}))
        if not validation['errors']:
            if not db.check_resource_deletion(del_data['resource_id']):
                db.delete_resource_by_id(del_data['resource_id'])
                response = jsonify(msg="success",
                                   deleted_resource=del_data['resource_id'])
            else:
                response = jsonify(error="Cannot delete!")
        else:
            response = Response(json.dumps(validation['errors']),
                                mimetype='application/json'), 400
        return response

    query = db.get_all_resources()
    parsed_data = {}
    if query:
        parsed_data = {res[1]: res[0] for res in query}
    return jsonify(parsed_data)


@app.route("/api/roles", methods=['GET', 'POST', 'PUT', 'DELETE'])
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
    # todo ajax validation?
    if request.method == "POST" and request.get_json():
        data = request.get_json()
        validation = validate(data, validators=(
            {'role_name': [v.required, v.min_l(2)]}
        ))
        if not validation['errors']:
            try:
                db.insert_role(data['role_name'])
                added_role_id = db.get_role_id(data['role_name'])
            except DBPoolError:
                return jsonify(error="role already exists"), 400

            response = jsonify(added_role=data['role_name'],
                               added_role_id=added_role_id[0])
        else:
            response = Response(json.dumps(validation['errors']),
                                mimetype='application/json'), 400
        return response

        # try:
        #     db.insert_role(data['role_name'])
        # except KeyError:
        #     return jsonify(error="Bad Request[key_error]"), 400
        # # todo change to uniqueIndentifyError or Exception
        # except DBPoolError:
        #     return jsonify(error="Already exists"), 400
        # try:
        #     added_role_id = db.get_role_id(data['role_name'])
        # except KeyError:
        #     return jsonify(error="Bad Request[key_error_add]"), 400
        # return jsonify(added_role=data['role_name'],
        #                added_role_id=added_role_id[0])

    # edit role by id
    if request.method == "PUT" and request.get_json():
        edit_data = request.get_json()
        validation = validate(edit_data, validators=(
            {'new_role_name': [v.required]},
            {'role_id': [v.required]}))
        if not validation['errors']:
            try:
                db.edit_role(edit_data['new_role_name'], edit_data['role_id'])
            except DBPoolError:
                return jsonify(error="this name already exists"), 400
            response = jsonify(msg="success",
                               edited=edit_data['new_role_name'])
        else:
            response = Response(json.dumps(validation['errors']),
                                mimetype='application/json'), 400
        return response

    if request.method == "DELETE" and request.get_json():
        del_data = request.get_json()
        validation = validate(del_data, validators=(
            {'role_id': [v.required]}))
        if not validation['errors']:
            if not db.check_role_deletion(del_data['role_id']):
                db.delete_role_by_id(del_data['role_id'])
                response = jsonify(msg="success",
                                   deleted_role=del_data['role_id'])
            else:
                response = jsonify(error="Cannot delete!")
        else:
            response = Response(json.dumps(validation['errors']),
                                mimetype='application/json'), 400
        return response

    query = db.get_all_roles()
    parsed_data = {}
    if query:
        parsed_data = {res[1]: res[0] for res in query}
    return jsonify(parsed_data)


@app.route("/api/permissions", methods=['GET', 'PUT', 'POST', 'DELETE'])
def permissions():
    """Controller used for mange getting and adding actions of
    server permission options.

       :return:
            - list of lists with permission data
                [id,action,modifier,resource)
            - if no resource in DB
                return empty json
    """

    if request.method == "POST" and request.get_json():
        data = request.get_json()
        validation = validate(data, validators=(
            {'resource_id': [v.required]},
            {'action': [v.required]},
            {'modifier': [v.required]},
            {'description': [v.required]}))

        if not validation['errors']:
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
            response = Response(json.dumps(validation['errors']),
                                mimetype='application/json'), 400
        return response

    # todo add unique handler!
    if request.method == "PUT" and request.get_json():
        edit_data = request.get_json()
        validation = validate(edit_data, validators=(
            {'new_action': [v.required]},
            {'new_modifier': [v.required]},
            {'permission_id': [v.required]},
            {'new_description': [v.required]}))

        if not validation['errors']:
            db.edit_permission(edit_data['new_action'],
                               edit_data['new_modifier'],
                               edit_data['permission_id'],
                               edit_data['new_description'])
            response = jsonify(msg="success",
                               edited_perm_id=edit_data['permission_id'])
        else:
            response = Response(json.dumps(validation['errors']),
                                mimetype='application/json'), 400
        return response

    if request.method == "DELETE" and request.get_json():
        data = request.get_json()
        validation = validate(data, validators=(
            {'permission_id': [v.required]}))
        if not validation['errors']:
            if not db.check_permission_deletion(data['permission_id']):
                db.delete_permission_by_id(data['permission_id'])
                response = jsonify(msg="success",
                                   deleted_permission=data['permission_id'])
            else:
                response = jsonify(error="Cannot delete!")
        else:
            response = Response(json.dumps(validation['errors']),
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
def get_role_permission():
    """
    Handler for assigning permissions to role.
    method GET:
        - returns JSON with all permissions of role
            and with actual selected permissions.
    method POST:

    """
    if request.method == "POST" and request.get_json():
        data = request.get_json()
        validation = validate(data, validators=(
            {'role_id': [v.required]},
            {'permission_id': [v.required]}))
        if not validation['errors']:
            db.add_role_permission(data['role_id'],
                                   data['permission_id'])
            response = jsonify(added_role_permission_for=data['role_id'])
        else:
            response = Response(json.dumps(validation['errors']),
                                mimetype='application/json'), 400
        return response

    if request.method == "PUT" and request.get_json():
        edit_data = request.get_json()
        validation = validate(edit_data, validators=(
            {'role_id': [v.required]},
            {'permission_id': [v.required]}))
        if not validation['errors']:
            db.delete_permissions_by_role_id(edit_data['role_id'])
            for id in edit_data['permission_id']:
                db.add_role_permission(edit_data['role_id'], id)
            response = jsonify(msg="edited permission")
        else:
            response = Response(json.dumps(validation['errors']),
                                mimetype='application/json'), 400
        return response

    if request.method == 'DELETE' and request.get_json():
        del_data = request.get_json()
        validation = validate(del_data, validators=(
            {'role_id': [v.required]}))
        if not validation['errors']:
            if not db.check_role_deletion(del_data['role_id']):
                db.delete_role_by_id(del_data['role_id'])
                response = jsonify(status="success",
                           deleted_role=del_data['role_id'])
            else:
                response = jsonify(error="Cannot delete!")
        else:
            response = Response(json.dumps(validation['errors']),
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


if __name__ == "__main__":
    app.run()
    app.logger = logger
