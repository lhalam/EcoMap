"""Module contains routes for user page."""
import json
import os

import ecomap.user as ecomap_user

from flask import request, jsonify, Response
from flask_login import login_required, current_user

from ecomap.db import util as db
from ecomap import validator
from ecomap.app import app


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
                os.makedirs(os.path.dirname(f_path + f_name))
            img_file.save(os.path.join(f_path, f_name))
            img_path = static_url + f_name
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
                os.remove(f_path + f_name)
            db.delete_user_avatar(data['user_id'])
            response = jsonify(msg='success', deleted_avatar=data['user_id'])
        else:
            response = Response(json.dumps(valid),
                                mimetype='application/json'), 400
    return response
