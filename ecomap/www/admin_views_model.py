# -*- coding: utf-8 -*-
"""Module contains base class for views and subclasses."""
import os
import json
import time
import hashlib

# from PIL import Image
from flask import request, jsonify, Response
from PIL import Image

from ecomap.db import util as db
from ecomap import validator

ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg', 'gif']
MARKERS_PATH = '/media/image/markers'


class BaseModel(object):

    """Base class for working with models."""

    def __init__(self, request):
        self.request = request

    def get(self):
        '''Method to retrieves data.'''
        pass

    def post(self):
        '''Method to add data.'''
        pass

    def update(self):
        '''Method to edit data.'''
        pass

    def delete(self):
        '''Method to delete data.'''
        pass

    def save_file(self, static_url):
        """Method to save a file from a form."""
        file_to_save = self.request.files
        if file_to_save:
            extension = file_to_save['file'].filename.rsplit('.', 1)[1].lower()
            if extension in ALLOWED_EXTENSIONS:
                f_path = os.environ['STATICROOT'] + static_url
                unique_key = time.time()
                hashed_name = hashlib.md5(str(unique_key))
                original_file = '%s.%s' % (hashed_name.hexdigest(), extension)
                file_to_save['file'].save(os.path.join(f_path, original_file))
                basewidth = 50
                img = Image.open(os.path.join(f_path, original_file))
                wpercent = (basewidth/float(img.size[0]))
                hsize = int((float(img.size[1])*float(wpercent)))
                img = img.resize((basewidth, hsize), Image.ANTIALIAS)
                f_name = '%s%s.%s' % (hashed_name.hexdigest(), '.min',
                                      extension)
                img.save(os.path.join(f_path, f_name))
                os.remove(os.path.join(f_path, original_file))
                response = f_name
            else:
                response = False
        else:
            response = False

        return response

    def validation(self):
        '''Method to validate data.'''
        pass


class ProblemType(BaseModel):

    '''Class for working with problem types.'''

    def get(self):
        '''The method retrieves all probleme types.'''
        problem_type_tuple = db.get_problem_type()
        problem_type_list = []
        if problem_type_tuple:
            for problem in problem_type_tuple:
                problem_type_list.append({'id': problem[0],
                                          'picture': problem[1],
                                          'name': problem[2],
                                          'radius': problem[3]})
        response = Response(json.dumps(problem_type_list),
                            mimetype='application/json')
        return response

    def post(self):
        '''The method adds new problem type.'''
        data = self.request.form
        if self.validation(data):
            if db.get_problem_type_by_name(data['problem_type_name']):
                response = jsonify(msg='Дане ім’я вже зарезервоване!'), 400
            else:
                file_name = self.save_file(MARKERS_PATH)
                if file_name:
                    db.add_problem_type(file_name, data['problem_type_name'],
                                        data['problem_type_radius'])
                    response = jsonify(msg='Тип проблеми успішно додано!'), 200
                else:
                    response = jsonify(msg='Проблема при додаванні фото.'
                                       'Спробуйте пізніше!'), 400
        else:
            response = jsonify(msg='Так як дані невірні!'), 400
        return response

    def update(self):
        '''The method edits new problem type.'''
        data = self.request.form
        if self.validation(data):
            old_name = db.get_problem_type_picture(data['problem_type_id'])
            f_path = os.environ['STATICROOT'] + MARKERS_PATH
            file_name = self.save_file(MARKERS_PATH)
            if file_name:
                if os.path.exists(os.path.join(f_path, old_name[0])):
                    os.remove(os.path.join(f_path, old_name[0]))
                db.update_problem_type(data['problem_type_id'], file_name,
                                       data['problem_type_name'],
                                       data['problem_type_radius'])
                response = jsonify(msg='Тип проблеми успішно оноволено!'), 200
            else:
                db.update_problem_type(data['problem_type_id'], old_name[0],
                                       data['problem_type_name'],
                                       data['problem_type_radius'])
                response = jsonify(msg='Тип проблеми оновлено!'), 200
        else:
            response = jsonify(msg='Так як дані невірні!'), 400
        return response

    def delete(self):
        '''The method deletes new problem type.'''
        data = self.request.get_json()
        if self.validation(data):
            file_name = db.get_problem_type_picture(data['problem_type_id'])
            f_path = os.environ['STATICROOT'] + MARKERS_PATH
            if os.path.exists(os.path.join(f_path, file_name[0])):
                os.remove(os.path.join(f_path, file_name[0]))
            db.delete_problem_type(data['problem_type_id'])
            if not db.get_problem_type_by_id(data['problem_type_id']):
                response = jsonify(msg='Дані видалено успішно!'), 200
            else:
                response = jsonify(msg='Дані не видалено!'), 400
        else:
            response = jsonify(msg='Некоректні дані!'), 400
        return response

    def validation(self, data):
        '''Validation for problem type.'''
        if self.request.method == 'DELETE':
            valid = validator.problem_type_delete(data)
            if valid['status']:
                response = True
            else:
                response = False
        if self.request.method == 'POST':
            valid = validator.problem_type_post(data)
            if valid['status']:
                response = True
            else:
                response = False
        if self.request.method == 'PUT':
            valid = validator.problem_type_put(data)
            if valid['status']:
                response = True
            else:
                response = False
        return response
