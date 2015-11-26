# coding=utf-8
"""
This module holds all views controls for
ecomap project.
"""

from flask import render_template, request, jsonify, g
from flask_login import current_user

import ecomap.user as usr

from ecomap.app import app, logger
from authorize_views import *
from admin_views import *
from user_views import *


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
        logger.warning(g.user)


@app.route('/', methods=['GET'])
def index():
    """Controller starts main application page.
    return: renders html template with angular app.
    """
    return render_template('index.html')


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
                           email=user.email, role=user.role)
        else:
            return jsonify(status='There is no user with given email'), 401


if __name__ == '__main__':
    app.run()
