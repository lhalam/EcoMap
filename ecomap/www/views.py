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
from authorize_views import *
from admin_views import *
from user_views import *

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
        g.user = anon.username
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
