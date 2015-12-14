"""Module contains routes, used for problem table."""
import json
import hashlib
import time
import os

from flask import request, jsonify, Response
from flask_login import current_user

from ecomap import validator
from ecomap.app import app, logger
from ecomap.db import util as db


@app.route('/api/problems')
def problems():
    """Handler for sending short data about all problem stored in db.
    Used by Google Map instance
    :return: list of problems with id, title, latitude, longitude,
    problem type, status and date of creation
    """
    problem_tuple = db.get_all_problems()
    parsed_json = []
    if problem_tuple:
        for problem in problem_tuple:
            parsed_json.append({
                'problem_id': problem[0], 'title': problem[1],
                'latitude': problem[2], 'longitude': problem[3],
                'problem_type_Id': problem[4], 'status': problem[5],
                'date': problem[6]})
    return Response(json.dumps(parsed_json), mimetype='application/json')


@app.route('/api/problem_detailed_info/<int:problem_id>', methods=['GET'])
def detailed_problem(problem_id):
    """This method returns json object with detailed problem data.
    :params problem_id - id of selected problem
    :return json with detailed info about problem
    """
    problem_data = db.get_problem_by_id(problem_id)
    activities_data = db.get_activity_by_problem_id(problem_id)
    photos_data = db.get_problem_photos(problem_id)
    photos = []
    activities = {}

    if problem_data:
        problems = {
            'problem_id': problem_data[0], 'title': problem_data[1],
            'content': problem_data[2], 'proposal': problem_data[3],
            'severity': problem_data[4], 'status': problem_data[5],
            'latitude': problem_data[6], 'longitude': problem_data[7],
            'problem_type_id': problem_data[8], 'date': problem_data[9]}
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
            photos.append({
                'url': photo_data[0],
                'description': photo_data[1],
                'user_id': photo_data[2]})

    response = Response(json.dumps([[problems], [activities], photos]),
                        mimetype='application/json')
    return response


@app.route('/api/problem_post', methods=['POST'])
def post_problem():
    """Function which adds data from problem form to DB.
    :return: If request data is invalid:
    {'status': False, 'error': [list of errors]}, 400
    If all ok:
    {'added_problem': 'problem_title'
    'problem_id': 'problem_id'}
    """
    if request.method == 'POST' and request.form:
        data = request.form
        logger.warning(json.dumps(request.form))
        logger.info(data)
        valid = validator.problem_post(data)
        if valid['status']:
            logger.debug('Checks problem post validation. %s', valid)
            user_id = current_user.uid
            now = time.time()
            posted_date = int(now)
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
                                         user_id)
            logger.debug('New problem post was created with id %s', last_id)
            response = jsonify(added_problem=data['title'],
                               problem_id=last_id)
        else:
            response = Response(json.dumps(valid),
                                mimetype='application/json'), 400
        return response


@app.route('/api/usersProblem/<int:user_id>', methods=['GET'])
def get_user_problems(user_id):
    """This method retrieves all user's problem from db.
        :returns list of user's problem represented with next objects:
        {"id": 190,
         "title": "name",
         "latitude": 51.419765,
         "longitude": 29.520264,
         "problem_type_id": 1,
         "status": 0,
         "date": "2015-02-24T14:27:22.000Z",
         "severity": '3',
         "is_enabled": 1
        }
    """
    problems_list = []
    problem_tuple = db.get_user_problems(user_id)
    logger.info(problem_tuple)
    for problem in problem_tuple:
        problems_list.append({'id': problem[0],
                              'title': problem[1],
                              'latitude': problem[2],
                              'logitude': problem[3],
                              'problem_type_id': problem[4],
                              'status': problem[5],
                              'date': problem[6] * 1000,
                              'severity': problem[8],
                              'is_enabled': problem[7]})
    return Response(json.dumps(problems_list), mimetype='application/json')


@app.route('/api/all_usersProblem', methods=['GET'])
def get_all_users_problems():
    """This method retrieves all user's problem from db.
        :returns list of user's problem represented with next objects:
        [
            {"id": 190,
             "title": "name",
             "latitude": 51.419765,
             "longitude": 29.520264,
             "problem_type_id": 1,
             "status": 0,
             "date": "2015-02-24T14:27:22.000Z",
             "severity": '3',
             "is_enabled": 1
            },
        ]
    """
    problems_list = []
    problem_tuple = db.get_all_users_problems()
    for problem in problem_tuple:
        problems_list.append({'id': problem[0],
                              'title': problem[1],
                              'latitude': problem[2],
                              'logitude': problem[3],
                              'problem_type_id': problem[4],
                              'status': problem[5],
                              'date': problem[6] * 1000,
                              'severity': problem[8],
                              'is_enabled': problem[7]})
    return Response(json.dumps(problems_list), mimetype='application/json')


@app.route('/api/photo/<int:problem_id>', methods=['POST'])
def problem_photo(problem_id):
    """Controller for handling adding problem photos.
    :param problem_id - id of problem instance for uploading new photos.
    :return: json object with success message or message with error status.
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
            db.add_problem_photo(problem_id, img_path, photo_descr, user_id)
            response = json.dumps({'added_file': img_path})
        else:
            response = jsonify(error='error with import file'), 400
    return response


@app.route('/api/problem/add_comment', methods=['POST'])
def post_comment():
    """Adds new comment to problem."""
    data = request.get_json()
    valid = True

    if valid:
        created_date = int(time.time())
        db.add_comment(data['user_id'],
                       data['problem_id'],
                       data['content'],
                       created_date)
        db.problem_activity_post(data['problem_id'],
                                 created_date,
                                 data['user_id'],
                                 'Updated')
        response = jsonify(message='Comment successfully added.')
    else:
        response = Response(json.dumps(valid),
                            mimetype='application/json'), 400
    return response
