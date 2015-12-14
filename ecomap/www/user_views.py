"""Module contains routes for user page."""
import json
import os

import ecomap.user as ecomap_user

from flask import request, jsonify, Response
from flask_login import login_required, current_user

from ecomap.db import util as db
from ecomap import validator
from ecomap.app import app, logger


@app.route('/api/change_password', methods=['POST'])
@login_required
def change_password():
    """Function, used to change user password
       :return: response - json object.
    """
    response = jsonify(), 400
    if request.method == 'POST' and request.get_json():
        data = request.get_json()

        valid = validator.change_password(data)

        if valid['status']:
            user = ecomap_user.get_user_by_id(data['id'])
            if user and user.verify_password(data['old_pass']):
                user.change_password(data['password'])
                response = jsonify(), 200
            else:
                response = jsonify(), 400
        else:
            response = Response(json.dumps(valid),
                                mimetype='application/json'), 400
    return response


@app.route('/api/user_detailed_info/<int:user_id>')
def get_user_info(user_id):
    """This method returns json object with user data."""
    if request.method == 'GET':
        user = ecomap_user.get_user_by_id(user_id)
        if user:
            return jsonify(name=user.first_name,
                           surname=user.last_name,
                           email=user.email,
                           role=user.role,
                           avatar=user.avatar)
        else:
            return jsonify(status='There is no user with given email'), 401


@app.route('/api/user_avatar', methods=['POST'])
@login_required
def add_profile_photo():
    """Controller provides add and edit function for user's profile photo.
    :return: json object with image path if success or 400 error message
    """
    response = jsonify(), 400
    extension = '.png'
    f_name = 'profile_id%s' % current_user.uid + extension
    static_url = '/uploads/user_profile/userid_%d/' % current_user.uid
    f_path = os.environ['STATICROOT'] + static_url
    if request.method == 'POST':
        img_file = request.files['file']

        if img_file and validator.validate_image_file(img_file):
            if not os.path.exists(f_path):
                os.makedirs(os.path.dirname('%s%s' % (f_path, f_name)))
            img_file.save(os.path.join(f_path, f_name))
            img_path = '%s%s' % (static_url, f_name)
            db.insert_user_avatar(current_user.uid, img_path)
            response = json.dumps({'added_file': img_path})
        else:
            response = jsonify(error='error with import file'), 400
    return response


@app.route('/api/user_avatar', methods=['DELETE'])
@login_required
def delete_profile_photo():
    """Controller for handling deleting user's profile photo.
    :return: json object with success message or message with error status
    """
    response = jsonify(), 400
    extension = '.png'
    f_name = 'profile_id%s' % current_user.uid + extension
    static_url = '/uploads/user_profile/userid_%d/' % current_user.uid
    f_path = os.environ['STATICROOT'] + static_url

    if request.method == 'DELETE' and request.get_json():
        data = request.get_json()
        valid = validator.user_photo_deletion(data)

        if valid['status']:
            if os.path.exists(f_path):
                os.remove('%s%s' % (f_path, f_name))
            db.delete_user_avatar(data['user_id'])
            response = jsonify(msg='success', deleted_avatar=data['user_id'])
        else:
            response = Response(json.dumps(valid),
                                mimetype='application/json'), 400
    return response


@app.route('/api/user_delete', methods=['DELETE'])
def delete_user():
    """Controller for handling deletion of user profile by
    profile owner.
    :return: json object with success message or message with error
    """
    data = request.get_json()
    valid = validator.user_deletion(data)
    if valid['status']:
        tuple_of_problems = db.get_problem_id_for_del(data['user_id'])
        problem_list = []
        for tuple_with_problem_id in tuple_of_problems:
            for problem_id in tuple_with_problem_id:
                    problem_list.append(problem_id)
        if problem_list:
            anon_tuple = db.select_anonim()
            anon_id = anon_tuple[0]

            for problem_id in problem_list:
                db.change_problem_to_anon(anon_id,problem_id)
                db.change_activity_to_anon(anon_id,problem_id)
            db.delete_user(data['user_id'])
            logger.info('User with id %s has been deleted' % data['user_id'])
            response = jsonify(msg='success', deleted_user=data['user_id'])
        else:
            db.delete_user(data['user_id'])
            logger.info('User with id %s has been deleted' % data['user_id'])
            response = jsonify(msg='success', deleted_user = data['user_id'])
    else:
        response = Response(json.dumps(valid),
                            mimetype='application/json'), 400
    return response

