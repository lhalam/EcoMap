"""Module contains routes for user page."""
import json
import os

import ecomap.user as ecomap_user

from flask import request, jsonify, Response
from flask_login import login_required, current_user

from ecomap.db import util as db
from ecomap import validator
from ecomap.app import app, auto, logger


@app.route('/api/change_password', methods=['POST'])
@auto.doc()
@login_required
def change_password():
    """Function, used to change user password.

    :rtype: JSON
    :request agrs: `{id: "6", old_pass: "oldpasswd", password: "newpasswd"}`
    :return:

        :statuscode 400: request is invalid or old password not confirmed
        :statuscode 200: password was successfully changed

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
@auto.doc()
@login_required
def get_user_info(user_id):
    """This method returns json object with user data.

    :param user_id: id of user for viewing detailed info
    :rtype: JSON
    :return:
        - If user exists and data provided:
            ``{"avatar": "/uploads/user_profile/userid_6/profile_id6.png",
            "email": "email@email.com", "name": "Firstname", "role": "admin",
            "surname": "Lastname"}``
        - If there is no user with given email:
            ``{status:'There is no user with given email'}``


    :statuscode 401: there is no user with given email
    :statuscode 200: user exists and data provided

    """
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
@auto.doc()
@login_required
def add_profile_photo():
    """Controller provides add and edit function for user's profile photo.

    :content-type: multipart/form-data

    :fparam name: name of image file ('photo.jpg')
    :fparam file: image file in base64. Content-Type: image/png

    :rtype: JSON
    :return: json object with image path if success or 400 error message

        - If request data is invalid:
            ``{'error': 'error with import file'}``
        - If all ok:
            ``{added_file: "/uploads/user_profile/userid_6/profile_id6.png"}``

    :statuscode 400: request is invalid
    :statuscode 200: photo was successfully added

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
@auto.doc()
@login_required
def delete_profile_photo():
    """Controller for handling deleting user's profile photo.

    :request args: `{'user_id': '6'}`
    :rtype: JSON
    :return: json object with success message or message with error status

        - If all ok:
            ``{deleted_avatar: "6", msg: "success"}``

    :statuscode 400: request invalid
    :statuscode 200: successfully deleted

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
