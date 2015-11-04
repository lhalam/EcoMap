import md5

from datetime import timedelta
from flask import Flask, render_template, request, jsonify
from flask_login import LoginManager
from itsdangerous import URLSafeTimedSerializer

from ecomap.db import util

import logging

app = Flask(__name__, template_folder='.')
app.debug = True
app.secret_key = 'top_secret'
app.config["REMEMBER_COOKIE_DURATION"] = timedelta(days=14)

login_serializer = URLSafeTimedSerializer(app.secret_key)

login_manager = LoginManager()


def hash_pass(password):
    """Return md5 hash of password + salt"""
    salted_password = password + app.secret_key
    return md5.new(salted_password).hexdigest()


@login_manager.user_loader
def load_user(user_email):
    """Flask-Login user_loader callback
    The user_loader function asks this function to get a User Object or return
    None based on the user_email.
    params:
        user_email - users email
    """
    return util.get_user(user_email)


@login_manager.token_loader
def load_token(token):
    """Flask-Login token_loader callback.
    The token_loader function asks this function to take the token that was
    stored on the users computer process it to check if its valid and then
    return a User object if its valid or None if its not valid.
    """
    max_age = app.config["REMEMBER_COOKIE_DURATION"].total_seconds()
    data = login_serializer.loads(token, max_age=max_age)
    user = util.get_user(data[0])

    if user and data[1] == user.password:
        return user
    return None


@app.route('/')
def func():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    json = request.get_json()
    user = util.get_user(json['email'])
    if user and hash_pass(json['password']) == user[3]:
        logging.getLogger('view').info('Got response from db: %s', user[3])
        return jsonify(first_name=user[0], last_name=user[1],
                       email=user[2], password=user[3])
    return 'wrong email or password'


@app.route('/register', methods=['GET', 'POST'])
def register():
    json = request.get_json()
    json['password'] = hash_pass(json['password'])
    user = util.get_user(json['email'])
    if user:
        return 'alredy exists'
    util.create_user(json['first_name'], json['last_name'], json['email'],
                     json['password'])
    return request.json['password']

if __name__ == '__main__':
    app.run()
