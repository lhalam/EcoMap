"""
This module holds all views controls for
ecomap project.
"""
# import sys

from flask import render_template, request, jsonify
from flask_login import login_user, logout_user, login_required

import ecomap.user as usr

from ecomap.app import app, logger


@app.route("/", methods=['GET'])
def index():
    """Controller starts main application page.

    return: renders html template.
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
    if request.method == "POST" and request.get_json():
        data = request.get_json()
        try:
            user = usr.get_user_by_email(data['email'])
        except KeyError:
            return jsonify(error="Bad Request", logined=0), 400
        if user and user.verify_password(data['password']):
            login_user(user, remember=True)
            return jsonify(id=user.uid,
                           name=user.first_name,
                           surname=user.last_name,
                           role='???', iat="???",
                           token=user.get_auth_token(),
                           email=user.email)
        if not user:
            return jsonify(error="There is no user with given email.",
                           logined=0), 401
        if not user.verify_password(data['password']):
            return jsonify(error="Invalid password, try again.",
                           logined=0), 401


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
    if request.method == 'POST' and request.get_json():
        data = request.get_json()
        arguments = ['firstName', 'lastName', 'email',
                     'password', 'pass_confirm']
        try:
            if [v for k, v in request.get_json().iteritems() if
                    not v or k not in arguments]:
                return jsonify(error="Unauthorized,"
                                     " some fields are empty"), 401
            first_name = data['firstName']
            last_name = data['lastName']
            email = data['email']
            password = data['password']
        except KeyError:
            return jsonify(error="Unauthorized, missing fields"), 401
        if not usr.get_user_by_email(email):
            usr.register(first_name, last_name, email, password)
            status = 'added %s %s', (first_name, last_name)
        else:
            status = 'user with this email already exists'
            return jsonify({'status': status}), 400
        return jsonify({'status': status})

if __name__ == "__main__":
    app.run()

    app.logger = logger
    # usr.login_manager.init_app(app)

    # user = usr.User.get(username="admin")
    # print user
    # login_user(user, remember=True)
