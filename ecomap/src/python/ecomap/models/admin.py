# -*- coding: utf-8 -*-
"""Module contains ProblemType class."""
import os
import re
import time
import magic
import hashlib
import logging

from PIL import Image

from ecomap.db import util as db
from base_view_model import BaseModel

ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg', 'gif']
MARKERS_PATH = '/media/image/markers'
MARKER_WIDTH = 50


class ProblemType(BaseModel):

    '''Class for working with problem types.'''

    def __init__(self):
        self.log = logging.getLogger('admin_model')

    status_code = [200, 401, 402]

    def save(self, image, name, radius):
        '''The method adds new problem type.'''
        if db.get_problem_type_by_name(name):
            response = self.status_code[1]
            self.log.info('Failed to add new problem type')
        else:
            file_name = self.save_file(image)
            if file_name:
                self.insert(file_name, name, radius)
                response = self.status_code[0]
                self.log.info('Added new problem type')
            else:
                self.log.info('Failed to add new problem type')
                response = self.status_code[2]
        return response

    def edit(self, type_id, picture, name, radius):
        '''The method edits new problem type.'''
        old_name = db.get_problem_type_picture(type_id)
        f_path = os.environ['STATICROOT'] + MARKERS_PATH
        file_name = self.save_file(picture)
        if file_name:
            if os.path.exists(os.path.join(f_path, old_name[0])):
                os.remove(os.path.join(f_path, old_name[0]))
            self.insert(file_name, name, radius, type_id)
            response = self.status_code[0]
            self.log.info('Problem type edited')
        else:
            db.self.update_field_in_db(old_name[0],
                                       name, radius, type_id)
            response = self.status_code[0]
            self.log.info('Problem type edited')
        return response

    def delete(self, type_id):
        '''The method deletes problem type.'''
        file_name = db.get_problem_type_picture(type_id)
        f_path = os.environ['STATICROOT'] + MARKERS_PATH
        if not db.get_problems_by_type(type_id):
            if os.path.exists(os.path.join(f_path, file_name[0])):
                os.remove(os.path.join(f_path, file_name[0]))
            self.remove_by_id(type_id)
            if not self.get_by_id(type_id):
                response = self.status_code[0]
                self.log.info('Problem type deleted')
            else:
                response = self.status_code[1]
                self.log.info('Failed to delete problem type')
        else:
            response = self.status_code[2]
            self.log.info('Failed to delete problem type')
        return response

    def save_file(self, marker):
        '''Method to save a file from a form.'''
        with magic.Magic(flags=magic.MAGIC_MIME_TYPE) as check:
            if bool(re.match('image/(\w+)', check.id_filename(marker.filename))):
                f_path = os.environ['STATICROOT'] + MARKERS_PATH
                unique_key = time.time()
                hashed_name = hashlib.md5(str(unique_key))
                basewidth = MARKER_WIDTH
                img = Image.open(marker['file'])
                wpercent = (basewidth/float(img.size[0]))
                hsize = int((float(img.size[1])*float(wpercent)))
                img = img.resize((basewidth, hsize), Image.ANTIALIAS)
                f_name = '%s' % (hashed_name.hexdigest())
                img.save(os.path.join(f_path, f_name))
                response = f_name
            else:
                response = False
        return response

    def get_all(self):
        '''Method gets all problem types.'''
        query = '''SELECT * FROM `problem_type`;'''
        response = db.read_method(query)
        return response

    def get_by_id(self, type_id):
        '''Method selects picture from proble type.'''
        query = ('''SELECT `*` FROM `problem_type`
                        WHERE `id`='{}';''').format(type_id)
        response = db.read_method(query)
        return response

    def remove_by_id(self, problem_type_id):
        '''Method removes problem type.'''
        query = ('''DELETE FROM `problem_type`
                        WHERE id='{}';''').format(problem_type_id)
        db.write_method(query)

    def insert(self, picture, name, radius, type_id='id'):
        '''Method inserts or updates problem types.'''
        query = ('''INSERT  INTO `problem_type` (`id`,`picture`,
                                     `name`, `radius`)
                      VALUES ('{}','{}', '{}', '{}') ON DUPLICATE KEY UPDATE
                      problem_type;''').format(type_id, picture, name,
                                               radius)
        db.write_method(query)
