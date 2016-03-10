# -*- coding: utf-8 -*-
"""Module contains ProblemType class."""
import os
import time
import hashlib

# from flask import request
from PIL import Image

from ecomap.db import util as db
from base_view_model import BaseModel

ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg', 'gif']
MARKERS_PATH = '/media/image/markers'


class ProblemType(BaseModel):

    '''Class for working with problem types.'''

    # def __init__():
    id = None
    picture = None
    name = None
    radius = None
    status_code = [200, 401, 402]

    def add(self, picture, name, radius):
        self.picture = picture
        self.name = name
        self.radius = radius

    def save(self, file):
        '''The method adds new problem type.'''
        # data = request.form
        if self.get_by_name(self.name):
            response = self.status_code[1]
        else:
            file_name = self.save_file(MARKERS_PATH, file)
            if file_name:
                self.insert_into_db(file_name, self.picture, self.name,
                                    self.radius)
                response = self.status_code[0]
            else:
                response = self.status_code[2]
        return response

    def edit(self, id):
        '''The method edits new problem type.'''
        # data = request.form
        self.id = id
        old_name = self.get_by_picture(self.id)
        f_path = os.environ['STATICROOT'] + MARKERS_PATH
        file_name = self.save_file(MARKERS_PATH, file)
        if file_name:
            if os.path.exists(os.path.join(f_path, old_name[0])):
                os.remove(os.path.join(f_path, old_name[0]))
            self.update_field_in_db(self.id, file_name,
                                    self.name, self.radius)
            response = self.status_code[0]
        else:
            db.self.update_field_in_db(self.id, old_name[0],
                                       self.name, self.radius)
            response = self.status_code[0]
        return response

    def delete(self, id):
        '''The method deletes new problem type.'''
        # data = request.get_json()
        self.id = id
        file_name = self.get_by_picture(self.id)
        f_path = os.environ['STATICROOT'] + MARKERS_PATH
        if not db.get_problems_by_type(self.id):
            if os.path.exists(os.path.join(f_path, file_name[0])):
                os.remove(os.path.join(f_path, file_name[0]))
            self.remove_from_db(self.id)
            if not self.get_by_id(self.id):
                response = self.status_code[0]
            else:
                response = self.status_code[1]
        else:
            response = self.status_code[2]
        return response

    def save_file(self, static_url, file_to_save):
        """Method to save a file from a form."""
        # file_to_save = request.files
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

    def get_all(self):
        '''Method gets all problem types from db.'''
        query = '''SELECT * FROM `problem_type`;'''
        response = db.read_method(query)
        return response

    # def get_problem_type(self, field, filtration, type_id):
    #     '''Method selects picture from proble type.'''
    #     query = ('''SELECT `'{}'` FROM `problem_type`
    #                     WHERE `'{}'`='{}';''').format(field,
    #                                                   filtration, type_id)
    #     response = db.read_method(query)
    #     return response

    def get_by_name(self, name):
        '''Method selects picture from proble type.'''
        query = ('''SELECT `*` FROM `problem_type`
                        WHERE `name`='{}';''').format(name)
        response = db.read_method(query)
        return response

    def get_by_picture(self, type_id):
        '''Method selects picture from proble type.'''
        query = ('''SELECT `picture` FROM `problem_type`
                        WHERE `id`='{}';''').format(type_id)
        response = db.read_method(query)
        return response

    def get_by_id(self, type_id):
        '''Method selects picture from proble type.'''
        query = ('''SELECT `*` FROM `problem_type`
                        WHERE `id`='{}';''').format(type_id)
        response = db.read_method(query)
        return response

    def remove_by_id(self, problem_type_id):
        '''Method removes problem type from db.'''
        query = ('''DELETE FROM `problem_type`
                        WHERE id='{}';''').format(problem_type_id)
        db.write_method(query)

    def insert(self, picture, name, radius):
        ''' '''
        query = ('''INSERT  INTO `problem_type` (`picture`,
                                     `name`, `radius`)
                      VALUES ('{}', '{}', '{}');''').format()
        db.write_method(query)

    def update(self, type_id, picture, name, radius):
        ''' '''
        query = ('''UPDATE `problem_type` SET `picture`='{}',
                                     `name`='{}', `radius`='{}'
                      WHERE `id`='{}';''').format(picture, name,
                                                  radius, type_id)
        db.write_method(query)
