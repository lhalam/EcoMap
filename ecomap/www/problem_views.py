# -*- coding: utf-8 -*-
"""Module contains routes, used for problem table."""
import os
import re
import json
import time
import shutil
import hashlib
import datetime

import PIL

from flask import request, jsonify, Response
from flask_login import current_user, login_required
from PIL import Image

from ecomap import validator
from ecomap.db import util as db
from ecomap.utils import generate_email, send_email
from ecomap.app import app, logger, auto, _CONFIG


ANONYMUS_USER_ID = 2
UPLOADS_PROBLEM_PATH = '/uploads/problems/'
MIN_SIZE = 'min.png'


@app.route('/api/problems')
@app.cache.cached(timeout=_CONFIG['ecomap.problems_cache_timeout'])
def problems():
    """Handler for sending short data about all problem stored in db.
    Used by Google Map instance.

    :rtype: JSON
    :return:
        - If problems list not empty:
            ``[{"status": "Unsolved", "problem_type_Id": 2,
            "title": "problem 1","longitude": 25.9717, "date": 1450735578,
            "latitude": 50.2893, "problem_id": 75},
            {"status": "Unsolved", "problem_type_Id": 3,
            "title": "problem 2", "longitude": 24.7852, "date": 1450738061,
            "latitude": 49.205, "problem_id": 76}]``
        - If problem list is empty:
            ``{}``

    :statuscode 200: no errors

    """
    problem_tuple = db.get_all_problems()
    parsed_json = []
    if problem_tuple:
        for problem in problem_tuple:
            parsed_json.append({
                'problem_id': problem[0], 'title': problem[1],
                'latitude': problem[2], 'longitude': problem[3],
                'is_enabled': problem[4], 'problem_type_Id': problem[5],
                'status': problem[6], 'date': problem[7],
                'radius': problem[8], 'picture': problem[9]})
    return Response(json.dumps(parsed_json), mimetype='application/json')


@app.route('/api/problem_detailed_info/<int:problem_id>', methods=['GET'])
def detailed_problem(problem_id):
    """This method returns object with detailed problem data.

    :rtype: JSON
    :param problem_id: `{problem_id: 82}`
    :return:
            - If problem exists:
                ``[[{"content": "Text with situation", "status": "Unsolved",
                "date": 1450954447, "severity": "1", "title": "problem",
                "latitude": 52.7762, "proposal": "proposal how to solve",
                "problem_type_id": 3, "problem_id": 82, "longitude": 34.2114}],
                [{"activity_type": "Added", "user_id": 5,
                "problem_id": 82, "created_date": 1450954447}],
                [{"url": "/uploads/problems/82/0d0d3ef56a16bd069e.png",
                "user_id": 5, "description": "description to photo"}],
                [{"user_id": 5, "name": "User", "problem_id": 82,
                "content": "Comment", "created_date": 1450954929000,
                "id": 5}]]``
            - If problem not exists:
                ``{"message": " resource not exists"}``

    :statuscode 404: problem not exists
    :statuscode 200: problem displayed

    """
    user_id = current_user.uid
    problem_data = db.get_problem_by_id(problem_id)
    activities_data = db.get_activity_by_problem_id(problem_id)
    photos_data = db.get_problem_photos(problem_id)
    comments_data = db.get_comments_by_problem_id(problem_id)
    subscription_data = db.check_exist_subscriptions(user_id, problem_id)
    photos = []
    activities = {}
    comments = []

    if problem_data:
        problems = {
            'problem_id': problem_data[0], 'title': problem_data[1],
            'content': problem_data[2], 'proposal': problem_data[3],
            'severity': problem_data[4], 'status': problem_data[5],
            'latitude': problem_data[6], 'longitude': problem_data[7],
            'problem_type_id': problem_data[8], 'date': problem_data[9],
            'name': problem_data[10], 'is_enabled': problem_data[11],
            'is_subscripted': subscription_data}
    else:
        return jsonify({'message': ' resource not exists'}), 404

    if activities_data:
        activities = {
            'created_date': activities_data[0],
            'problem_id': activities_data[1],
            'user_id': activities_data[2],
            'activity_type': activities_data[3]}
    if photos_data:
        for photo_data in photos_data:
            photos.append({'url': photo_data[0],
                           'description': photo_data[1],
                           'user_id': photo_data[2]})
    if comments_data:
        for comment in comments_data:
            subcomments_count = db.get_count_of_parent_subcomments(comment[0])
            comments.append({'id': comment[0],
                             'content': comment[1],
                             'problem_id': comment[2],
                             'created_date': comment[3] * 1000,
                             'updated_date': comment[4] * 1000 if comment[4] else None,
                             'user_id': comment[5],
                             'nickname': comment[6],
                             'avatar': comment[7],
                             'sub_count': subcomments_count[0]})

    response = Response(json.dumps([[problems], [activities],
                                    photos, comments]),
                        mimetype='application/json')
    return response


@app.route('/api/problem_post', methods=['POST'])
def post_problem():
    """Function which adds data about created problem into DB.

    :content-type: multipart/form-data

    :fparam title: Title of problem ('problem with rivers')
    :fparam type: id of problem type (2)
    :fparam lat: lat coordinates (49.8256101)
    :fparam longitude: lon coordinates (24.0600542)
    :fparam content: description of problem ('some text')
    :fparam proposal: proposition for solving problem ('text')

    :rtype: JSON
    :return:
            - If request data is invalid:
                    ``{'status': False, 'error': [list of errors]}``
            - If all ok:
                    ``{"added_problem": "problem title", "problem_id": 83}``

    :statuscode 400: request is invalid
    :statuscode 200: problem was successfully posted

    """
    if request.method == 'POST' and request.form:
        data = request.form
        logger.warning(json.dumps(request.form))
        logger.info(data)
        valid = validator.problem_post(data)
        if valid['status']:
            logger.debug('Checks problem post validation. %s', valid)
            user_id = current_user.uid
            posted_date = int(time.time())
            last_id = db.problem_post(data['title'],
                                      data['content'],
                                      data['proposal'],
                                      data['latitude'],
                                      data['longitude'],
                                      data['type'],
                                      posted_date,
                                      user_id)
            if last_id:
                db.problem_activity_post(last_id, posted_date,
                                         user_id, 'Added')
            logger.debug('New problem post was created with id %s', last_id)
            response = jsonify(added_problem=data['title'],
                               problem_id=last_id)
        else:
            response = Response(json.dumps(valid),
                                mimetype='application/json'), 400
        return response


@app.route('/api/usersProblem/<int:user_id>', methods=['GET'])
def get_user_problems(user_id):
    """This method retrieves all user's problem from db and shows it in user
    profile page on `my problems` tab.
    :param  user_id: id of user (int).
    :query filtr: name of column for filtration.
    :query order: 0 or 1. 0 - asc and 1 - desc.
    :query limit: limit number. default is 5.
    :query offset: offset number. default is 0.
    :rtype: JSON.
    :return:
        - If user has problems:
            ``[{'id': 190, 'title': 'name',
            'latitude': 51.419765,
            'longitude': 29.520264,
            'problem_type_id': 1,
            'status': 0,
            'date': "2015-02-24T14:27:22.000Z",
            'severity': '3',
            'is_enabled': 1,
            'name': 'problem with forest'
            },{...}]``
        - If user haven't:
            ``{}``
        :statuscode 200: no errors.
    """
    filtr = request.args.get('filtr') or None
    order = int(request.args.get('order')) or 0
    offset = int(request.args.get('offset')) or 0
    per_page = int(request.args.get('per_page')) or 5
    if filtr:
        order_desc = 'asc' if order else 'desc'
        problem_tuple = db.get_user_problem_by_filter(user_id, order_desc,
                                                      filtr, offset, per_page)
    else:
        problem_tuple = db.get_user_problems(user_id, offset, per_page)
    count = db.count_user_problems(user_id)
    problems_list = [{'id': problem[0],
                      'title': problem[1],
                      'latitude': problem[2],
                      'logitude': problem[3],
                      'problem_type_id': problem[4],
                      'status': problem[5],
                      'date': problem[6] * 1000,
                      'severity': problem[8],
                      'is_enabled': problem[7],
                      'user_id': problem[9],
                      'name': problem[10]}
                     for problem in problem_tuple] if problem_tuple else []
    logger.info(problem_tuple)
    total_count = {'total_problem_count': count[0]} if count else {}
    return Response(json.dumps([problems_list, [total_count]]),
                    mimetype='application/json')


@app.route('/api/all_usersProblem', methods=['GET'])
def get_all_users_problems():
    """This method retrieves all user's problem from db.
    :query filtr: name of column for filtration.
    :query order: 0 or 1. 0 - asc and 1 - desc.
    :query limit: limit number. default is 5.
    :query offset: offset number. default is 0.
    :rtype: JSON.
    :return: list of user's problem represented with next objects:
        ``[{"id": 190,
        "title": "name",
        "latitude": 51.419765,
        "longitude": 29.520264,
        "problem_type_id": 1,
        "status": 0,
        "date": "2015-02-24T14:27:22.000Z",
        "severity": '3',
        "is_enabled": 1,
        'last_name': 'name',
        'first_name': 'surname',
        'nickname': 'nick',
        'name': 'problem with forests'}]``

    """
    filtr = request.args.get('filtr')
    order = int(request.args.get('order')) or 0
    offset = request.args.get('offset') or 0
    per_page = request.args.get('per_page') or 5
    if filtr:
        order_desc = 'asc' if order else 'desc'
        problem_tuple = db.get_user_by_filter(order_desc, filtr, offset,
                                              per_page)
    else:
        problem_tuple = db.get_all_users_problems(offset, per_page)
    count = db.count_problems()
    problems_list = [{'id': problem[0],
                      'title': problem[1],
                      'latitude': problem[2],
                      'longitude': problem[3],
                      'user_id': problem[4],
                      'problem_type_id': problem[5],
                      'status': problem[6],
                      'date': problem[7] * 1000,
                      'severity': problem[9],
                      'is_enabled': problem[8],
                      'last_name': problem[10],
                      'first_name': problem[11],
                      'nickname': problem[12],
                      'name': problem[13]}
                     for problem in problem_tuple] if problem_tuple else []
    total_count = {'total_problem_count': count[0]} if count else {}
    return Response(json.dumps([problems_list, [total_count]]),
                    mimetype='application/json')


@app.route('/api/photo/<int:problem_id>', methods=['POST'])
def problem_photo(problem_id):
    """Controller for handling adding problem photos.

    **param** problem_id - id of problem instance for uploading new photos.

    :content-type: multipart/form-data

    :fparam file: image file in base64. Content-Type: image/png
    :fparam name: image name (`'image.jpg'`)
    :fparam description: description of image (`'some text'`)

    :return: json object with success message or message with error status.

        - if success:
            ``{"added_file": "/uploads/problems/77/df4c22114eb24442e8b6.png"}``

    :statuscode 400: error with attaching image or request is invalid
    :statuscode 200: successfully added

    """
    response = jsonify(), 400
    extension = '.png'
    static_url = '/uploads/problems/%s/' % problem_id
    f_path = os.environ['STATICROOT'] + static_url
    user_id = current_user.uid
    now = time.time()*100000
    unique_key = (int(now)+user_id)
    hashed_name = hashlib.md5(str(unique_key))
    f_name = '%s%s' % (hashed_name.hexdigest(), extension)

    if request.method == 'POST':
        problem_img = request.files['file']
        photo_descr = request.form['description']

        if problem_img and validator.validate_image_file(problem_img):
            if not os.path.exists(f_path):
                os.makedirs(os.path.dirname('%s%s' % (f_path, f_name)))
            problem_img.save(os.path.join(f_path, f_name))
            img_path = '%s%s' % (static_url, f_name)

            basewidth = 100
            img = Image.open(os.path.join(f_path, f_name))
            wpercent = (basewidth/float(img.size[0]))
            hsize = int((float(img.size[1])*float(wpercent)))
            img = img.resize((basewidth, hsize), PIL.Image.ANTIALIAS)
            f_name = '%s%s%s' % (hashed_name.hexdigest(), '.min', extension)
            img.save(os.path.join(f_path, f_name))

            db.add_problem_photo(problem_id, img_path, photo_descr, user_id)
            response = json.dumps({'added_file': img_path})
        else:
            response = jsonify(error='error with import file'), 400
    return response


@app.route('/api/change_comment', methods=['POST'])
def change_comment_by_id():
    """This method update comment content.
    :rtype: JSON
    :param id: comment_id `{id: 2}`
    :param content: comment content

    :statuscode 400: error updating comment
    :statuscode 200: comment added successfully

    """
    response = jsonify(), 400
    data = request.get_json()
    updated_date = int(time.time())
    if data:
        valid = validator.change_comment(data)
        if valid['status']:
            db.change_comment_by_id(data['id'], data['content'], updated_date)
            response = jsonify({'updated_date': updated_date * 1000}), 200
    return response


@app.route('/api/delete_comment', methods=['DELETE'])
def delete_comment_by_id():
    """Function deletes comment from DB.
    :type: JSON
    :return: response
    """
    comment_id = int(request.args.get('comment_id'))
    db.delete_comment_by_id(comment_id)
    logger.debug('Comment and all subcomments (if any) was deleted with id %s',
                 comment_id)
    response = jsonify(message='Comment successfully added.'), 200
    return response


@app.route('/api/problem/add_comment', methods=['POST'])
@login_required
def post_comment():
    """Adds new comment to problem.

    :rtype: JSON
    :request args: `{content: "comment", problem_id: "77"}`
    :return:
        - if success:
            ``{"message": "Comment successfully added."}``
        - if some error:
            ``{error: "type of validation error"}``

    :statuscode 400: error with adding comment or request is invalid
    :statuscode 200: successfully added

    """
    data = request.get_json()
    valid = validator.check_post_comment(data)

    if valid['status']:
        created_date = int(time.time())
        user_id = ANONYMUS_USER_ID if data.get('anonim') else current_user.uid
        db.add_comment(user_id,
                       data['problem_id'],
                       data['parent_id'],
                       data['content'],
                       created_date)
        db.problem_activity_post(data['problem_id'],
                                 created_date,
                                 user_id,
                                 'Updated')
        response = jsonify(message='Comment successfully added.'), 200
    else:
        response = Response(json.dumps(valid),
                            mimetype='application/json'), 400

    return response


@app.route('/api/problem_comments/<int:problem_id>', methods=['GET'])
def get_comments(problem_id):
    """Return all problem comments

        :rtype: JSON
        :param problem_id: id of problem (int)
        :return:
            - If problem has comments:
                ``[{content: "some comment",
                created_date: 1451001050000,
                id: 29,
                name: "user name",
                problem_id: 77,
                user_id: 6,
                } ,{...}]``
            - If user hasn't:
                ``{}``

        :statuscode 200: no errors

    """

    comments_data = db.get_comments_by_problem_id(problem_id)
    comments = []

    if comments_data:
        for comment in comments_data:
            subcomments_count = db.get_count_of_parent_subcomments(comment[0])
            comments.append({'id': comment[0],
                             'content': comment[1],
                             'problem_id': comment[2],
                             'created_date': comment[3] * 1000,
                             'updated_date': comment[4] * 1000 if comment[4] else None,
                             'user_id': comment[5],
                             'nickname': comment[6],
                             'avatar': comment[7],
                             'sub_count': subcomments_count[0]})
    response = Response(json.dumps(comments),
                        mimetype='application/json')
    return response


@app.route('/api/problem_subcomments/<int:parent_id>', methods=['GET'])
def get_subcomments(parent_id):
    """Return all comment subcomments

        :rtype: JSON
        :param parent_id: id of parent comment (int)
        :return:
            - If problem has comments:
                ``[{content: "some comment",
                created_date: 1451001050000,
                id: 29,
                name: "user name",
                problem_id: 22,
                parent_id: 77,
                user_id: 6,
                } ,{...}]``
            - If user hasn't:
                ``{}``

        :statuscode 200: no errors

    """

    comments_data = db.get_subcomments_by_parent_id(parent_id)
    sub_count = db.get_count_of_parent_subcomments(parent_id)
    comments = []

    if comments_data:
        for comment in comments_data:
            comments.append({'id': comment[0],
                             'content': comment[1],
                             'problem_id': comment[2],
                             'parent_id': comment[3],
                             'created_date': comment[4] * 1000,
                             'updated_date': comment[5] * 1000 if comment[5] else None,
                             'user_id': comment[6],
                             'nickname': comment[7],
                             'avatar': comment[8],
                             'first_name': comment[9],
                             'last_name': comment[10]})
    response = Response(json.dumps([comments, sub_count[0]]),
                        mimetype='application/json')
    return response


@app.route('/api/usersSubscriptions/<int:user_id>', methods=['GET'])
def get_user_subscriptions(user_id):
    """Function retrieves all user's subscriptions from db and shows it in user
    profile page on `my subscriptions` tab.
    :param id: id of subscription (int)
    :param title: title of problem (str)
    :param problem_type_id: id of problem type (int)
    :param status: status of problem (solved or unsolved)
    :param date: date when problem was creared
    :param date_subscription: date when user subscribed to a problem
    :param name: name of problem type
    :type: JSON
    """
    offset = int(request.args.get('offset')) or 0
    per_page = int(request.args.get('per_page')) or 5
    subscription_tuple = db.get_subscriptions(user_id, offset, per_page)
    count = db.count_user_subscriptions(user_id)
    subscriptions_list = []
    total_count = {}
    logger.info(subscription_tuple)
    for subscription in subscription_tuple:
        subscriptions_list.append({'id': subscription[0],
                                   'title': subscription[1],
                                   'problem_type_id': subscription[2],
                                   'status': subscription[3],
                                   'date': subscription[4] * 1000,
                                   'date_subscription': subscription[5] * 1000,
                                   'name': subscription[6]})
    if count:
        total_count = {'total_problem_count': count[0]}
    return Response(json.dumps([subscriptions_list, [total_count]]),
                    mimetype='application/json')


@app.route('/api/usersSubscriptions', methods=['GET'])
def get_all_subscriptions():
    """Function retrieves all user's subscriptions from db and shows it in
    admin profile page on `my subscriptions` tab.
    :query per_page: limit number. default is 5.
    :query offset: offset number. default is 0.
    :param id: id of subscription (int).
    :param title: title of problem (str).
    :param problem_type_id: id of problem type (int).
    :param status: status of problem (solved or unsolved).
    :param date: date when problem was creared.
    :param date_subscription: date when user subscribed to a problem.
    :param name: name of problem type.
    :last_name: user last name.
    :first_name: user first name.
    :nickname: user nickname.
    :type: JSON.
    """
    offset = int(request.args.get('offset')) or 0
    per_page = int(request.args.get('per_page')) or 5
    subscription_tuple = db.get_all_subscriptions(offset, per_page)
    count = db.count_all_subscriptions()
    subscriptions_list = [{'id': subscription[0],
                           'title': subscription[1],
                           'problem_type_id': subscription[2],
                           'status': subscription[3],
                           'date': subscription[4] * 1000,
                           'date_subscription': subscription[5] * 1000,
                           'name': subscription[6],
                           'last_name': subscription[7],
                           'first_name': subscription[8],
                           'nickname': subscription[9]}
                          for subscription in subscription_tuple]
    logger.info(subscription_tuple)
    total_count = {'total_problem_count': count[0]} if count else {}
    return Response(json.dumps([subscriptions_list, [total_count]]),
                    mimetype='application/json')


@app.route('/api/countSubscriptions', methods=['GET'])
def get_count_subscriptions():
    """Function retrieves all user's subscriptions from db and shows them in
    `top 10 of the most popular subscriptions` tab.
    :param count: count of subscriptions to every problem (int)
    :param title: title of problem (str)
    :type: JSON
    """
    subscription_tuple = db.count_subscriptions_by_problem_id()
    subscriptions_list = []
    total_count = {}
    logger.info(subscription_tuple)
    for subscription in subscription_tuple:
        subscriptions_list.append({'count': subscription[0],
                                   'id': subscription[1],
                                   'title': subscription[2]})
    sorted_json = sorted(subscriptions_list,
                     key=lambda k: (k['count']),
                     reverse=True)[:10]
    return Response(json.dumps([sorted_json]),
                    mimetype='application/json')


@app.route('/api/subscription_post', methods=['POST'])
def subscription_post():
    """Function adds data about subscription into DB.
    :param problem_id: id of problem (int)
    :param user_id: id of user (int)
    :param subscr date: date when user subscribed to a problem
    :return: response
    :type: JSON
    """
    if request.method == 'POST':
        data = request.get_json()
        logger.warning(request.get_json())
        logger.info(data)
        user_id = current_user.uid
        subscr_date = int(time.time())
        last_id = db.subscription_post(data['problem_id'],
                                       user_id,
                                       subscr_date)
        logger.debug('New subscription post was created with id %s', last_id)
        response = jsonify(subscription_id=last_id)
        return response


@app.route('/api/subscription_delete', methods=['DELETE'])
def subscription_delete():
    """Function deletes data of subscription from DB.
    :type: JSON
    :return: response
    """
    if request.method == 'DELETE':
        logger.info(request.args.get('problem_id'))
        problem_id = int(request.args.get('problem_id'))
        user_id = current_user.uid
        logger.info(problem_id)
        last_id = db.subscription_delete(user_id, problem_id)
        logger.debug('Subscription post was deleted with id %s', last_id)
        response = jsonify(subscription_id=last_id)
        return response


@app.route('/api/search_usersProblem', methods=['GET'])
def get_search_users_problems():
    """This method retrieves all user's problem with special nickname from db.
    :query per_page: limit number. default is 5.
    :query offset: offset number. default is 0.
    :rtype: JSON.
    :return: list of user's problem represented with next objects:
        ``[{"id": 190,
        "title": "name",
        "status": 0,
        "date": "2015-02-24T14:27:22.000Z",
        "severity": '3',
        "is_enabled": 1,
        'last_name': 'name',
        'first_name': 'surname',
        'nickname': 'nick'}]``
    """
    filtr = request.args.get('filtr')
    order = int(request.args.get('order')) or 0
    nickname = request.args.get('nickname').encode('utf-8')
    offset = int(request.args.get('offset')) or 0
    per_page = int(request.args.get('per_page')) or 5
    order_desc = 'desc' if order else 'asc'
    if filtr:
        problem_tuple = db.get_filter_user_by_nickname(nickname, filtr,
                                                       order_desc, offset,
                                                       per_page)
    else:
        problem_tuple = db.get_user_by_nickname(nickname, offset, per_page)
    count = db.count_user_by_nickname(nickname)
    problems_list = [{'id': problem[0],
                      'title': problem[1],
                      'status': problem[2],
                      'date': problem[3] * 1000,
                      'is_enabled': problem[4],
                      'severity': problem[5],
                      'nickname': problem[6],
                      'user_id': problem[7],
                      'last_name': problem[8],
                      'first_name': problem[9],
                      'name': problem[10]}
                     for problem in problem_tuple] if problem_tuple else []
    total_count = {'total_problem_count': count[0]} if count else {}
    return Response(json.dumps([problems_list, [total_count]]),
                    mimetype='application/json')


@app.route('/api/all_users_comments', methods=['GET'])
@login_required
def all_users_comments():
    """Function gets all comments from DB.
    :type: JSON
    :query per_page: limit number. default is 5.
    :query offset: offset number. default is 0.
    :rtype: JSON.
    :return: list of user's comments and total_count:
    ``[{"id": 2,
        "content": "Awesome comment.",
        "problem_id": 12,
        "problem_title": "Forest Problem",
        "created_date": "2015-02-24T14:27:22.000Z",
        "nickname": 'Pomidor',
        "first_name": 'Ivan',
        'last_name': 'Kozak',
        'sub_count': 15}]``
    """
    offset = request.args.get('offset') or 0
    per_page = request.args.get('per_page') or 5
    comments_data = db.get_all_users_comments(offset, per_page)
    count = db.get_count_comments()
    comments = []
    total_count = {}
    if comments_data:
        problems_id = [comment[2] for comment in comments_data]
        problems_title = db.get_problems_title(problems_id)
        for comment in comments_data:
            subcomments_count = db.get_count_of_parent_subcomments(comment[0])
            comments.append({'id': comment[0],
                             'content': comment[1],
                             'problem_id': comment[2],
                             'problem_title': problems_title.get(comment[2]),
                             'created_date': comment[3] * 1000,
                             'user_id' : comment[4],
                             'nickname': comment[5],
                             'first_name': comment[6],
                             'last_name': comment[7],
                             'sub_count': subcomments_count[0]})
    if count:
        total_count = {'total_comments_count': count[0]}
    response = Response(json.dumps([comments, [total_count]]),
                        mimetype='application/json')
    return response


@app.route('/api/nickname_subscriptions', methods=['GET'])
def get_user_subscriptions_nickname():
    """Function retrieves all user's subscriptions by nickname from db and
    shows it using search field on `my subscriptios` tab.
    :query per_page: limit number. default is 5.
    :query offset: offset number. default is 0.
    :param id: id of subscription (int).
    :param title: title of problem (str).
    :param problem_type_id: id of problem type (int).
    :param status: status of problem (solved or unsolved).
    :param date: date when problem was creared.
    :param date_subscription: date when user subscribed to a problem.
    :param name: name of problem type.
    :last_name: user last name.
    :first_name: user first name.
    :nickname: user nickname.
    :type: JSON
    """
    nickname = request.args.get('nickname').encode('utf-8')
    offset = request.args.get('offset') or 0
    per_page = request.args.get('per_page') or 5
    subscription_tuple = db.get_subscriptions_by_nickname(nickname,
                                                          offset,
                                                          per_page)
    count = db.count_subscriptions_by_nickname(nickname)
    subscriptions_list = [{'id': subscription[0],
                           'title': subscription[1],
                           'problem_type_id': subscription[2],
                           'status': subscription[3],
                           'date': subscription[4] * 1000,
                           'date_subscription': subscription[5] * 1000,
                           'name': subscription[6],
                           'last_name': subscription[7],
                           'first_name': subscription[8],
                           'nickname': subscription[9]}
                          for subscription in subscription_tuple]
    logger.info(subscription_tuple)
    total_count = {'total_problem_count': count[0]} if count else {}
    return Response(json.dumps([subscriptions_list, [total_count]]),
                    mimetype='application/json')


@app.route('/api/search_users_comments', methods=['GET'])
def search_users_comments():
    """This method retrieves all user's comments with special nickname from db.
    :query per_page: limit number. default is 5.
    :query offset: offset number. default is 0.
    :rtype: JSON.
    :return: list of user's problem represented with next objects:
    ``[{"id": 2,
        "content": "Awesome comment.",
        "problem_id": 12,
        "problem_title": "Forest Problem",
        "created_date": "2015-02-24T14:27:22.000Z",
        "nickname": 'Pomidor',
        "first_name": 'Ivan',
        'last_name': 'Kozak',
        'sub_count': 15}]``
    """
    nickname = request.args.get('nickname').encode('utf-8')
    offset = int(request.args.get('offset')) or 0
    per_page = int(request.args.get('per_page')) or 5
    comments_count = db.get_count_comments_by_nickname(nickname)
    comment_tuple = db.get_comments_by_nickname(nickname, offset, per_page)
    comments = []
    if comment_tuple:
        problems_id = [comment[2] for comment in comment_tuple]
        problems_title = db.get_problems_title(problems_id)
        for comment in comment_tuple:
            subcomments_count = db.get_count_of_parent_subcomments(comment[0])
            comments.append({'id': comment[0],
                             'content': comment[1],
                             'problem_id': comment[2],
                             'problem_title': problems_title.get(comment[2]),
                             'created_date': comment[3] * 1000,
                             'user_id' : comment[4],
                             'nickname': comment[5],
                             'first_name': comment[6],
                             'last_name': comment[7],
                             'sub_count': subcomments_count[0]})
    if comments_count:
        total_count = {'total_comments_count': comments_count[0]}
    return Response(json.dumps([comments, [total_count]]),
                    mimetype='application/json')


@app.route('/api/problem_type_filtration', methods=['GET'])
def get_problem_type_for_filtration():
    '''The method retrieves all probleme types.
       :rtype: JSON.
       :return: json object with problem types.
       :JSON sample:
       ``[{"id": 1,
        "name": "first problem type"},
        ....
        {"id": 7,
        "name": "sevens problem type"]``.
    '''
    problem_type_tuple = db.get_problem_type_for_filtration()
    problem_type_list = []
    if problem_type_tuple:
        for problem in problem_type_tuple:
            problem_type_list.append({'id': problem[0],
                                      'picture': problem[1],
                                      'name': problem[2]
                                      })
    response = Response(json.dumps(problem_type_list),
                        mimetype='application/json')
    return response


@app.route('/api/problems_radius/<int:type_id>')
@login_required
def problems_radius(type_id):
    """Handler for sending short data for about probles for
         radius functionality.
    :rtype: JSON
    :return:
        - If problems list not empty:
            ``[{"status": "Unsolved", "problem_type_Id": 2,
            "title": "problem 1","longitude": 25.9717, "date": 1450735578,
            "latitude": 50.2893, "problem_id": 75}]``
        - If problem list is empty:
            ``{}``

    :statuscode 200: no errors

    """
    problem_tuple = db.get_problems_by_type(type_id)
    parsed_json = []
    if problem_tuple:
        for problem in problem_tuple:
            parsed_json.append({
                'problem_id': problem[0], 'title': problem[1],
                'latitude': problem[2], 'longitude': problem[3],
                'problem_type_Id': problem[4], 'name': problem[9],
                'radius': problem[10]})
    return Response(json.dumps(parsed_json), mimetype='application/json')


@app.route('/api/statisticPieChar', methods=['GET'])
def statistic_problems():
    """This method returns statisctic for some period from db.
    Statistic include type of problem and its count for this period.
    :period: int which define time period. default is 0. Can have such values:
    (0 - period of all time, 1 - only for one day, 2 - for a week,
    3 -for a month, 4 - for a year).
    :rtype: JSON.
    :return: list of statisctic ecomap's problem with next objects:
    ``[{"type": "Forest Problem",
        "count": 12}]``
    """
    period = int(request.args.get('date')) or 0
    count = db.count_problem_types()[0]
    if period:
        date_format = ('', '%Y-%m-%d', '%U', '%Y-%m', '%Y')[period]
        posted_date = datetime.datetime.now().strftime(date_format)
        statics = [{'type': db.count_type(problem_types, date_format,
                                          posted_date)[1],
                    'count': db.count_type(problem_types, date_format,
                                           posted_date)[0]}
                   for problem_types in range(1, count+1)]
    else:
        statics = [{'type': db.count_all_type(problem_types)[1],
                    'count': db.count_all_type(problem_types)[0]}
                   for problem_types in range(1, count+1)]
    return Response(json.dumps(statics), mimetype='application/json')


@app.route('/api/problems_severity_stats')
def problems_severity_stats():
    """This method returns top 10 important problems.
    :rtype: JSON
    :return:
        - If problems list not empty:
            ``[{"id": "1", "date": 1450735578,
            "title": "problem 1","severity": 1}]``
        - If problem list is empty:
            ``{}``

    :statuscode 200: no errors

    """
    problem_tuple = db.get_all_problems_severity_for_stats()
    parsed_json = []
    if problem_tuple:
        for problem in problem_tuple:
            parsed_json.append({'id': problem[0], 'date': problem[4],
                                'title': problem[5],
                                'severity': problem[6]})
    sorted_json = sorted(parsed_json,
                         key=lambda k: (k['severity'], k['date']),
                         reverse=True)[:10]
    return Response(json.dumps(sorted_json), mimetype='application/json')


@app.route('/api/statistic_all', methods=['GET'])
def statistic_all():
    """This method returns statisctic for all problems, subscriptions,
    comments, photos from db.
    :rtype: JSON.
    :return: list of all statisctics with next objects:
    statistics[0] - count of all problems, statistics[1] - count of all
    subscriptions, statistics[2] - count of all comments,
    tatistics[3] - count of all photos
    """
    statistics = [db.count_problems()[0], db.count_all_subscriptions()[0],
                  db.count_comment()[0], db.count_photo()[0]]
    return Response(json.dumps(statistics), mimetype='application/json')

@app.route('/api/problems_comments_stats', methods=['GET'])
def problems_comments_stats():
    """This method returns top 10 discussed problems.
    :rtype: JSON.
    :return: list of top 10 discussed problems with next objects:
    ``[{'problems_id': 4,
        'problem_title': Big problem,
        'comments_count': 34}]``
    """
    problems_comments = db.get_problems_comments_stats()
    parsed_json = []
    if problems_comments:
        for problem in problems_comments:
            parsed_json.append({'id': problem[0],
                                'title': problem[1],
                                'comments_count': problem[2]})
    return Response(json.dumps(parsed_json), mimetype='application/json')


@app.route('/api/search_byFilter_usersProblem', methods=['GET'])
def get_search_problems_by_filter():
    """This method retrieves all user's problem by special filter name from db.
    :query filtr: name of column for filtration.
    :query order: 0 or 1. 0 - asc and 1 - desc.
    :query per_page: limit number. default is 5.
    :query offset: offset number. default is 0.
    :rtype: JSON.
    :return: list of user's problem represented with next objects:
        ``[{"id": 190,
        "title": "name",
        "status": 0,
        "date": "2015-02-24T14:27:22.000Z",
        "severity": '3',
        "is_enabled": 1,
        'last_name': 'name',
        'first_name': 'surname',
        'nickname': 'nick',
        'name': 'forests_problem'}]``
    """
    filtr = request.args.get('filtr')
    order = int(request.args.get('order')) or 0
    offset = int(request.args.get('offset')) or 0
    per_page = int(request.args.get('per_page')) or 5
    order_desc = 'desc' if order else 'asc'
    count = db.count_problems()
    problem_tuple = db.get_user_by_filter(order_desc, filtr, offset, per_page)
    problems_list = [{'id': problem[0],
                      'title': problem[1],
                      'status': problem[2],
                      'date': problem[3] * 1000,
                      'is_enabled': problem[4],
                      'severity': problem[5],
                      'nickname': problem[6],
                      'last_name': problem[7],
                      'first_name': problem[8],
                      'name': problem[9]}
                     for problem in problem_tuple] if problem_tuple else []
    total_count = {'total_problem_count': count[0]} if count else {}
    return Response(json.dumps([problems_list, [total_count]]),
                    mimetype='application/json')


@app.route('/api/problem_delete', methods=['DELETE', 'PUT'])
@auto.doc()
@login_required
def delete_problem():
    """The method deletes problem by id.
       :rtype: JSON.
       :request args: `{problem_id: 5}`.
       :return: confirmation object.
       :JSON sample:
       ``{'msg': 'Problem type was deleted successfully!'}``
       or
       ``{'msg': 'Cannot delete'}``.

       :statuscode 400: if request is invalid.
       :statuscode 200: if no errors.
    """
    data = request.get_json()
    valid = validator.problem_delete(data)
    if valid['status']:
        if request.method == 'DELETE':
            folder_to_del = UPLOADS_PROBLEM_PATH + str(data['problem_id'])
            f_path = os.environ['STATICROOT'] + folder_to_del
            if os.path.exists(f_path):
                shutil.rmtree(f_path, ignore_errors=True)
            db.delete_problem_by_id(data['problem_id'])
            email_tuple = db.get_user_by_id(data['user_id'])
            message = generate_email('delete_problem',
                                     _CONFIG['email.from_address'],
                                     email_tuple[4], (email_tuple[1],
                                                      email_tuple[2],
                                                      data['problem_title'],
                                                      request.url_root))
            send_email(_CONFIG['email.server_name'],
                       _CONFIG['email.user_name'],
                       _CONFIG['email.server_password'],
                       _CONFIG['email.from_address'],
                       email_tuple[4],
                       message)
            response = jsonify(msg='Дані видалено успішно!'), 200
        elif request.method == 'PUT':
            db.change_problem_to_anon(data['problem_id'])
            response = jsonify(msg='Дані привязані на анонімного юзера!'), 200
    else:
        response = jsonify(msg='Некоректні дані!'), 400
    return response


@app.route('/api/problem_confirmation', methods=['PUT'])
@auto.doc()
@login_required
def problem_confirmation():
    """The method deletes problem by id.
       :rtype: JSON.
       :request args: `{problem_id: 5,
                                    severity: '3',
                                    status: 'Solved',
                                    is_enabled: 0}`.
       :return: confirmation object.
       :JSON sample:
       ``{'msg': 'Problem type was deleted successfully!'}``
       or
       ``{'msg': 'Cannot delete'}``.

       :statuscode 400: if request is invalid.
       :statuscode 200: if no errors.
    """
    data = request.get_json()
    valid = validator.problem_confirmation(data)
    if valid['status']:
        update_time = int(time.time())
        db.problem_confirmation(data['problem_id'], data['severity'],
                                data['status'], data['is_enabled'],
                                update_time)
        user_id = db.get_user_id_problem_by_id[5]
        email_tuple = db.get_user_by_id(user_id)
        message = generate_email('update_problem',
                                 _CONFIG['email.from_address'],
                                 email_tuple[4], (email_tuple[1],
                                                  email_tuple[2],
                                                  data['problem_title'],
                                                  data['content'],
                                                  request.url_root))
        send_email(_CONFIG['email.server_name'],
                   _CONFIG['email.user_name'],
                   _CONFIG['email.server_password'],
                   _CONFIG['email.from_address'],
                   email_tuple[4],
                   message)
        response = jsonify(msg='Дані успішно змінено!'), 200
    else:
        response = jsonify(msg='Некоректні дані!'), 400
    return response


@app.route('/api/problem_edit', methods=['PUT'])
@auto.doc()
@login_required
def edit_problem():
    """The method deletes problem by id.
       :rtype: JSON.
       :request args: `{problem_id: 5,
                                    title: name,
                                    content: 'message',
                                    proposal: 'message 2'}`.
       :return: confirmation object.
       :JSON sample:
       ``{'msg': 'Problem type was deleted successfully!'}``
       or
       ``{'msg': 'Cannot delete'}``.

       :statuscode 400: if request is invalid.
       :statuscode 200: if no errors.
    """
    data = request.get_json()
    # valid = validator.problem_put(data)
    # if valid['status']:
    update_time = int(time.time())
    db.edit_problem(data['problem_id'], data['title'],
                    data['content'], data['proposal'],
                    data['latitude'], data['longitude'],
                    data['type'], update_time)
    response = jsonify(msg='Дані успішно змінено!'), 200
    # else:
    #     response = jsonify(msg='Некоректні дані!'), 400
    return response


# @app.route('/api/photo_delete', methods=['DELETE'])
# @auto.doc()
# @login_required
def delete_photo():
    """The method deletes min photo and photos by photo id.
       :rtype: JSON.
       :request args: `{photo_id: 5}`.
       :return: confirmation object.
       :JSON sample:
       ``{'msg': 'Problem type was deleted successfully!'}``
       or
       ``{'msg': 'Cannot delete'}``.

       :statuscode 400: if request is invalid.
       :statuscode 200: if no errors.
    """
    data = request.get_json()
    uploads_path = 'uploads/problems/%s/' % data['photo_id']
    photo_origin = str(db.get_problem_photo_by_id(data['photo_id']))
    # min photo path
    f_min_path = os.environ['STATICROOT'] + uploads_path
    # photo path
    f_path = os.environ['STATICROOT'] + photo_origin
    photo_min = re.search('\w+[\.]', photo_origin).group() + MIN_SIZE
    if os.path.exists(f_path):
        os.remove(f_path)
        db.delete_photo_by_id(data['photo_id'])
        if os.path.exists(os.path.join(f_min_path, photo_min)):
            os.remove(os.path.join(f_min_path, photo_min))
        response = jsonify(msg='Дані успішно видалено!'), 200
    else:
        response = jsonify(msg='Такого файлу не існує!'), 200
    return response
