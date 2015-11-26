# coding=utf-8
"""
This module holds all views controls for
ecomap project.
"""
import json
import os

from flask import render_template, request, jsonify, Response, g, abort
from flask_login import login_user, logout_user, login_required, current_user

import ecomap.user as usr

from ecomap.app import app, logger
from ecomap.db import util as db
from ecomap import validator
from ecomap.permission import permission_control, check_permissions
from ecomap.pagination import paginate, Pagination

@app.before_request
def load_users():
    """Function to check if user is authenticated, else creates
       Anonymous user.
       Launches before requests.
    """
    if current_user.is_authenticated:
        g.user = current_user
        logger.info(g.user)
    else:
        anon = usr.Anonymous()
        g.user = anon
        logger.info(g.user.role)
        logger.info(current_user)


# @app.before_request
def check_access():
    """Global decorator for each view.
    Checks permissions to access app resources by each user's request.
    Gets dynamic user info(user role, url, request method)from request context.
    :return: nested function returns true or 403
    """
    access_info = permission_control.get_dct()

    route = '/' + '/'.join(request.url.split('/')[3:])
    logger.debug('CHECK REQUEST: (url = %s [ %s ], user ID %s as %s )'
                 % (route, request.method, current_user.uid, current_user.role))
    check_permissions(current_user.role, route,
                      request.method, access_info)
    logger.debug(check_permissions(current_user.role, route,
                                   request.method, access_info))


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
    response = jsonify(), 401
    if request.method == 'POST' and request.get_json():
        data = request.get_json()

        valid = validator.validate_user_login(data)

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
    if request.method == 'POST':
        data = request.get_json()

        valid = validator.validate_change_password(data)

        if valid['status']:
            user = usr.get_user_by_id(data['id'])
            if user and user.verify_password(data['old_pass']):
                user.change_password(data['new_pass'])
                response = jsonify(), 200
            response = jsonify(), 400
        else:
            response = Response(json.dumps(valid),
                                mimetype='application/json'), 400
    return response


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
    response = jsonify(msg='unauthorized'), 400
    if request.method == 'POST' and request.get_json():
        data = request.get_json()

        valid = validator.validate_user_registration(data)

        if valid['status']:
            if not usr.get_user_by_email(data['email']):
                usr.register(data['firstName'], data['lastName'],
                             data['email'], data['password'])
                msg = 'added %s %s' % (data['firstName'], data['lastName'])
                response = jsonify({'status_message': msg}), 201
            else:
                msg = 'user with this email already exists'
                response = jsonify({'status_message': msg}), 401
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
                           email=user.email, role=user.role, avatar=user.avatar)
        else:
            return jsonify(status='There is no user with given email'), 401


@app.route('/api/user_avatar', methods=['POST', 'DELETE'])
@login_required
def profile_photo():
    """Controller for handling editing user's profile photo.
    :return:
    """
    response = {}
    if request.method == 'POST':
        img_file = request.files['file']
        extension = '.png'
        f_name = 'profile_id%s' % current_user.uid + extension
        static_url = '/uploads/user_profile/userid_%d/' % current_user.uid
        f_path = os.environ['STATICROOT'] + static_url

        if img_file and validator.validate_image_file(img_file):
            if not os.path.exists(f_path):
                os.makedirs(os.path.dirname(f_path + f_name))
            img_file.save(os.path.join(f_path, f_name))
            img_path = static_url + f_name
            db.insert_user_avatar(current_user.uid, img_path)
            return json.dumps({'added_file': img_path})
        return jsonify(error='error with import file'), 400

    if request.method == 'DELETE' and request.get_json():
        data = request.get_json()

        # valid = validator.validate_photo_delete(data)

        # if valid['status']:
        # if os.path.exists(f_path):
        #     os.remove(f_path + f_name)
        db.delete_user_avatar(data['user_id'])
        response = jsonify(msg='success', deleted_avatar=data['user_id'])
        # else:
        #     response = Response(json.dumps(valid),
        #                         mimetype='application/json'), 400
        return response
    return jsonify(response)


@app.route("/api/resources", methods=['GET', 'POST', 'PUT', 'DELETE'])
@login_required
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

        valid = validator.validate_resource_post(data)

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

    if request.method == 'PUT' and request.get_json():
        data = request.get_json()

        valid = validator.validate_resource_put(data)

        if valid['status']:
            if db.get_resource_id(data['new_resource_name']):
                return jsonify(error='this name already exists'), 400

            db.edit_resource_name(data['new_resource_name'],
                                  data['resource_id'])
            response = jsonify(status='success',
                               edited=data['new_resource_name'])
        else:
            response = Response(json.dumps(valid),
                                mimetype='application/json'), 400
        return response

    if request.method == 'DELETE' and request.get_json():
        del_data = request.get_json()

        valid = validator.validate_resource_delete(del_data)

        if valid['status']:
            if not db.check_resource_deletion(del_data['resource_id']):
                db.delete_resource_by_id(del_data['resource_id'])
                response = jsonify(msg='success',
                                   deleted_resource=del_data['resource_id'])
            else:
                response = jsonify(error='Cannot delete!')
        else:
            response = Response(json.dumps(valid),
                                mimetype='application/json'), 400
        return response

    query = db.get_all_resources()
    parsed_data = {}
    if query:
        parsed_data = {res[1]: res[0] for res in query}
    return jsonify(parsed_data)


@app.route("/api/roles", methods=['GET', 'POST', 'PUT', 'DELETE'])
@login_required
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

        valid = validator.validate_role_post(data)

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

    if request.method == 'PUT' and request.get_json():
        edit_data = request.get_json()

        valid = validator.validate_role_put(edit_data)

        if valid['status']:
            if db.get_role_id(edit_data['new_role_name']):
                return jsonify(error='this name already exists'), 400

            db.edit_role(edit_data['new_role_name'], edit_data['role_id'])
            response = jsonify(msg='success',
                               edited=edit_data['new_role_name'])
        else:
            response = Response(json.dumps(valid),
                                mimetype='application/json'), 400
        return response

    if request.method == 'DELETE' and request.get_json():
        del_data = request.get_json()

        valid = validator.validate_role_delete(del_data)

        if valid['status']:
            if not db.check_role_deletion(del_data['role_id']):
                db.delete_role_by_id(del_data['role_id'])
                response = jsonify(msg='success',
                                   deleted_role=del_data['role_id'])
            else:
                response = jsonify(error='Cannot delete!')
        else:
            response = Response(json.dumps(valid),
                                mimetype='application/json'), 400
        return response

    query = db.get_all_roles()
    parsed_data = {}
    if query:
        parsed_data = {res[1]: res[0] for res in query}
    return jsonify(parsed_data)


@app.route("/api/permissions", methods=['GET', 'PUT', 'POST', 'DELETE'])
@login_required
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

        valid = validator.validate_permission_post(data)

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

    if request.method == 'PUT' and request.get_json():
        edit_data = request.get_json()

        valid = validator.validate_permission_put(edit_data)

        if valid['status']:
            db.edit_permission(edit_data['new_action'],
                               edit_data['new_modifier'],
                               edit_data['permission_id'],
                               edit_data['new_description'])
            response = jsonify(msg='success',
                               edited_perm_id=edit_data['permission_id'])
        else:
            response = Response(json.dumps(valid),
                                mimetype='application/json'), 400
        return response

    if request.method == 'DELETE' and request.get_json():
        data = request.get_json()

        valid = validator.validate_permission_delete(data)

        if valid['status']:
            if not db.check_permission_deletion(data['permission_id']):
                db.delete_permission_by_id(data['permission_id'])
                response = jsonify(msg='success',
                                   deleted_permission=data['permission_id'])
            else:
                response = jsonify(error='Cannot delete!')
        else:
            response = Response(json.dumps(valid),
                                mimetype='application/json'), 400
        return response

    resource_id = request.args.get('resource_id')
    permission_tuple = db.get_all_permissions_by_resource(resource_id)
    parsed_json = {}
    if permission_tuple:
        for res in permission_tuple:
            parsed_json.update({'permission_id': res[0], 'action': res[1],
                                'modifier': res[2], 'description': res[3]})
    return Response(json.dumps(parsed_json), mimetype='application/json')


@app.route("/api/role_permissions", methods=['GET', 'PUT', 'POST'])
@login_required
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

        valid = validator.validate_role_permission_post(data)

        if valid['status']:
            db.add_role_permission(data['role_id'],
                                   data['permission_id'])
            response = jsonify(added_role_permission_for=data['role_id'])
        else:
            response = Response(json.dumps(valid),
                                mimetype='application/json'), 400
        return response

    if request.method == 'PUT' and request.get_json():
        edit_data = request.get_json()

        valid = validator.validate_role_permission_put(edit_data)

        if valid['status']:
            db.delete_permissions_by_role_id(edit_data['role_id'])
            for perm_id in edit_data['permission_id']:
                db.add_role_permission(edit_data['role_id'], perm_id)
            response = jsonify(msg='edited permission')
        else:
            response = Response(json.dumps(valid),
                                mimetype='application/json'), 400
        return response

    if request.method == 'DELETE' and request.get_json():
        del_data = request.get_json()

        valid = validator.validate_role_permission_delete(del_data)

        if valid['status']:
            if not db.check_role_deletion(del_data['role_id']):
                db.delete_role_by_id(del_data['role_id'])
                response = jsonify(status='success',
                                   deleted_role=del_data['role_id'])
            else:
                response = jsonify(error='Cannot delete!')
        else:
            response = Response(json.dumps(valid),
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
def edit_page(page_id):
    """This method makes changes to given page(ex-resource).

        :returns confirmation.
    """
    if request.method == 'PUT':
        data = request.get_json()
        status_code = None
        result = None
        if db.get_page_by_id(data['id']):
            db.edit_page(page_id, data['title'], data['alias'],
                         data['description'], data['content'],
                         data['meta_keywords'], data['meta_description'],
                         data['is_enabled'])
            result = True
            status_code = 200
        else:
            result = False
            status_code = 404
        return jsonify(result=result), status_code


@app.route('/api/addResource', methods=['POST'])
@login_required
def add_page():
    """This method adds new page to db."""
    result = None
    msg = None
    if request.method == 'POST':
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
@login_required
def delete_page(page_id):
    """This method deletes page by it's id."""
    msg = None
    result = None
    if request.method == 'DELETE':
        db.delete_page_by_id(page_id)
        if not db.get_page_by_id(page_id):
            result = True
            msg = 'Page was deleted successfully!'
        else:
            result = False
            msg = "Couldn't delete the page!"
    return jsonify(result=result, msg=msg)


@app.route("/api/user_roles", methods=['GET', 'POST'])
@login_required
def get_all_users():
    """Function, used to get all users.
       :return: list of users with id, first name, last name, email and role
    """
    if request.method == 'POST' and request.get_json():
        data = request.get_json()

        valid = validator.validate_user_role_post(data)

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
                'problem_id': problem[0], 'title': problem[1],
                'latitude': problem[2], 'longtitude': problem[3],
                'problem_type_Id': problem[4], 'status': problem[5],
                'date': problem[6]})
    return Response(json.dumps(parsed_json), mimetype='application/json')


@app.route('/api/problem_detailed_info/<int:problem_id>', methods=['GET'])
def detailed_problem(problem_id):
    """
    This method returns json object with detailed problem data.
    :params problem_id - id of selected problem
    :return json with detailed info about problem
    """
    problem_tuple = db.get_problem_by_id(problem_id)
    activity_tuple = db.get_activity_by_problem_id(problem_id)
    parsed_json = []
    problem_info = []
    activity_info = []
    photo_info = []
    parsed_json.append(problem_info)
    parsed_json.append(activity_info)
    parsed_json.append(photo_info)
    if problem_tuple:
        problem_info.append({
            'problem_id': problem_tuple[0], 'title': problem_tuple[1],
            'content': problem_tuple[2], 'proposal': problem_tuple[3],
            'severity': problem_tuple[4], 'status': problem_tuple[5],
            'latitude': problem_tuple[6], 'longtitude': problem_tuple[7],
            'problem_type_id': problem_tuple[8]
            })

    if activity_tuple:
        activity_info.append({
            'created_date': activity_tuple[0], ' problem_id': activity_tuple[1],
            'user_id': activity_tuple[2], 'activity_type': activity_tuple[3]
            })

    return Response(json.dumps(parsed_json), mimetype='application/json')


@app.route("/api/user_page", methods=['GET'])
# @paginate('users')
def pagination():
    """
    """
    offset = int(request.args.get('offset'))
    per_page = int(request.args.get('per_page'))
    query = db.get_users_pagination(offset, per_page)
    parsed_json = []
    if query:
        for user_data in query:
            parsed_json.append({'id': user_data[0], 'first_name': user_data[1],
                                'last_name': user_data[2],
                                'email': user_data[3],
                                'role_name': user_data[4]})
    return Response(json.dumps(parsed_json), mimetype='application/json')


PER_PAGE = 5


@app.route('/users/', defaults={'page': 1})
@app.route('/users/page/<int:page>')
def show_users(page):
    count = db.count_users()[0]
    users = db.pagination_test(page, PER_PAGE, count)
    logger.warning('**************************')
    if not users and page != 1:
        abort(404)
    pagination_ = Pagination(page, PER_PAGE, count, users)

    logger.warning(pagination_.per_page)
    # logger.warning(pagination_.prev)
    logger.warning(pagination_.prev_num)
    logger.warning(pagination_.total)
    # logger.warning(pagination_.query)
    logger.warning(pagination_.next_num)
    logger.warning(pagination_.page)
    logger.warning(pagination_.pages)
    logger.warning(pagination_.has_prev)
    logger.warning(pagination_.items)
    logger.warning(pagination_.iter_pages)
    # logger.warning(pagination_.next)
    return Response(json.dumps(({'total_pages': pagination_.pages,
                                 'page': pagination_.page,
                                 'total': pagination_.total,
                                 'per_page': pagination_.per_page,
                                 'data': pagination_.items}),
                               indent=1), mimetype='application/json')


@app.route("/api/users_p", methods=['GET', 'POST'])
@login_required
# @paginate('users')
def get_all_users_p():
    """Function, used to get all users.
    """
    users_tuple = db.get_all_users()
    parsed_json = []
    if users_tuple:
        for res in users_tuple:
            parsed_json.append({'user_id': res[0], 'first_name': res[1],
                                'last_name': res[2], 'email': res[3],
                                'role': res[4]})
    return Response(json.dumps(parsed_json), mimetype='application/json')



if __name__ == '__main__':
    app.run()
