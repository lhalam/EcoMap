"""
This module holds all views controls for
ecomap project.
"""
import sys

from flask import render_template, request, jsonify
from flask_login import login_user, logout_user

import ecomap.db.user as usr

from ecomap.app import app


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        data = request.get_json()
        user = usr.User.get(username=data['username'])
        if user and usr.hash_pass(data['password']) == \
           usr.hash_pass(user.password):
            try:
                logined = login_user(user, force=True)
                return jsonify(userid=user.userid, logined=logined)
            except:
                return jsonify(e=str(sys.exc_info()[0]))
    return jsonify(error="Couldn't login with your credenntials!!!", logined=0)


@app.route("/api/logout", methods=["GET", "POST"])
def logout():
    result = logout_user()
    return jsonify(result=result)


# @app.route("/register")
# def register():
#     response = {
#         "id": 1,
#         "name": 'Andrii',
#         "surname": "Piratovskyi",
#         "role": "dev",
#         "iat": 3546464,
#         "token": "sfdandaoifnewf53dsa54g3g87dfsg",
#         "email": "andjeypirat@gmail.com",
#     }
#     return jsonify(response)

if __name__ == "__main__":
    app.run()
    # usr.login_manager.init_app(app)

    # user = usr.User.get(username="admin")
    # print user
    # login_user(user, remember=True)
