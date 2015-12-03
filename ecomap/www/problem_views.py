"""Module contains routes, used for problem table."""
import json
import time
import os

from flask import request, jsonify, Response
from flask_login import current_user

from ecomap import validator
from ecomap.app import app, logger
from ecomap.db import util as db


@app.route('/api/problems')
def problems():
    """
    Function, used to get all problems.
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
    """
    This method returns json object with detailed problem data.
    :params problem_id - id of selected problem
    :return json with detailed info about problem
    """
    problem_tuple = db.get_problem_by_id(problem_id)
    activity_tuple = db.get_activity_by_problem_id(problem_id)
    photos = db.get_problem_photos(problem_id)
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
            'latitude': problem_tuple[6], 'longitude': problem_tuple[7],
            'problem_type_id': problem_tuple[8], 'date': problem_tuple[9]
        })

    if activity_tuple:
        activity_info.append({
            'created_date': activity_tuple[0], 'problem_id': activity_tuple[1],
            'user_id': activity_tuple[2], 'activity_type': activity_tuple[3]
        })
    if photos:
        for photo_data in photos:
            logger.warning(photos)
            photo_info.append({
                'url': photo_data[0], 'description': photo_data[1],
                'user_id': photo_data[2]
            })
    return Response(json.dumps(parsed_json), mimetype='application/json')


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
            logger.debug('Checks if valid.')
            logger.debug(valid)
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
            logger.debug(last_id)
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


@app.route('/api/photo/<int:problem_id>', methods=['POST'])
def problem_photo(problem_id):
    """ Connected with problem_post. Creating for uploading photos
        with problem.
        :return: json with success if photo have been uploaded
    """
    response = jsonify(), 400

    extension = '.png'
    static_url = 'uploads/problems/problem_%s/' % problem_id
    f_path = os.environ['STATICROOT'] + static_url
    user_id = current_user.uid

    if request.method == 'POST':
        problem_img = request.files['file']
        user_f_name = request.form['name']
        f_name = user_f_name[:-4] + '_problem_%s' % problem_id + extension
        photo_descr = request.form['description']
        if problem_img and validator.validate_image_file(problem_img):
            if not os.path.exists(f_path):
                os.makedirs(os.path.dirname(f_path + f_name))
            problem_img.save(os.path.join(f_path, f_name))
            img_path = static_url + f_name
            db.add_problem_photo(problem_id, img_path, photo_descr, user_id)
            response = json.dumps({'added_file': img_path})
        else:
            response = jsonify(error='error with import file'), 400
    return response
