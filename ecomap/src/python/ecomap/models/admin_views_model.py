# -*- coding: utf-8 -*-
"""Module contains base class for views and subclasses."""
import os
import json
import time
import hashlib

from flask import request, Response
from PIL import Image

from ecomap.db import util as db
from base_view_model import BaseModel

ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg', 'gif']
MARKERS_PATH = '/media/image/markers'


class ProblemType(BaseModel):

    '''Class for working with problem types.'''

    fields = {'*': '*',
              'id': 'id',
              'picture': 'picture',
              'name': 'name',
              'radius': 'radius'}
    table = 'problem_type'
    status_code = [200, 401, 402]

    def get_all(self):
        '''The method retrieves all probleme types.'''
        problem_type_tuple = self.get_all_from_db()
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

    def add(self):
        '''The method adds new problem type.'''
        data = request.form
        if self.get_problem_type(self.fields['*'], self.fields['name'],
                                 data['problem_type_name']):
            response = self.status_code[1]
        else:
            file_name = self.save_file(MARKERS_PATH)
            if file_name:
                self.insert_into_db(file_name, data['problem_type_name'],
                                    data['problem_type_radius'])
                response = self.status_code[0]
            else:
                response = self.status_code[2]
        return response

    def edit(self):
        '''The method edits new problem type.'''
        data = request.form
        old_name = self.get_problem_type(self.fields['picture'],
                                         self.fields['id'],
                                         data['problem_type_id'])
        f_path = os.environ['STATICROOT'] + MARKERS_PATH
        file_name = self.save_file(MARKERS_PATH)
        if file_name:
            if os.path.exists(os.path.join(f_path, old_name[0])):
                os.remove(os.path.join(f_path, old_name[0]))
            self.update_field_in_db(data['problem_type_id'], file_name,
                                    data['problem_type_name'],
                                    data['problem_type_radius'],
                                    self.fields['id'])
            response = self.status_code[0]
        else:
            db.self.update_field_in_db(data['problem_type_id'], old_name[0],
                                       data['problem_type_name'],
                                       data['problem_type_radius'],
                                       self.fields['id'])
            response = self.status_code[0]
        return response

    def delete(self):
        '''The method deletes new problem type.'''
        data = request.get_json()
        file_name = self.get_problem_type(self.fields['picture'],
                                          self.fields['id'],
                                          data['problem_type_id'])
        f_path = os.environ['STATICROOT'] + MARKERS_PATH
        if not db.get_problems_by_type(data['problem_type_id']):
            if os.path.exists(os.path.join(f_path, file_name[0])):
                os.remove(os.path.join(f_path, file_name[0]))
            self.remove_from_db(data['problem_type_id'])
            if not self.get_problem_type(self.fields[0], self.table,
                                         self.fields[1],
                                         data['problem_type_id']):
                response = self.status_code[0]
            else:
                response = self.status_code[1]
        else:
            response = self.status_code[2]
        return response

    def save_file(self, static_url):
        """Method to save a file from a form."""
        file_to_save = request.files
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

    def get_all_from_db(self):
        '''Method gets all problem types from db.'''
        query = '''SELECT * FROM `problem_type`;'''
        response = db.read_method(query)
        return response

    def get_problem_type(self, field, filtration, type_id):
        '''Method selects picture from proble type.'''
        query = ('''SELECT `'{}'` FROM `problem_type`
                        WHERE `'{}'`='{}';''').format(field,
                                                      filtration, type_id)
        response = db.read_method(query)
        return response

    def remove_from_db(self, problem_type_id):
        '''Method removes problem type from db.'''
        query = ('''DELETE FROM `problem_type`
                        WHERE id='{}';''').format(problem_type_id)
        db.write_method(query)

    def insert_into_db(self, picture, name, radius):
        ''' '''
        query = ('''INSERT  INTO `problem_type` (`picture`,
                                     `name`, `radius`)
                      VALUES ('{}', '{}', '{}');''').format()
        db.write_method(query)

    def update_field_in_db(self, type_id, picture, name, radius, filtration):
        ''' '''
        query = ('''UPDATE `problem_type` SET `picture`='{}',
                                     `name`='{}', `radius`='{}'
                      WHERE `'{}'`='{}';''').format(picture, name,
                                                    radius, filtration,
                                                    type_id)
        db.write_method(query)
