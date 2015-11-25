import json

from flask import request, jsonify, Response
from flask_login import login_required

import ecomap.user as usr

from ecomap import validator
from ecomap.app import app
from authorize_views import *
from admin_views import *


@app.route('/api/change_password', methods=['POST'])
@login_required
def change_password():
    """Function, used to change user password
       :return: response - json object.
    """
    response = jsonify(), 401
    data = request.get_json()

    valid = validator.change_password(data)

    if valid['status']:
        user = usr.get_user_by_id(data['id'])
        if user and user.verify_password(data['old_pass']):
            user.change_password(data['password'])
            response = jsonify(), 200
        else:
            response = jsonify(), 400
    else:
        response = Response(json.dumps(valid),
                            mimetype='application/json'), 400
    return response
