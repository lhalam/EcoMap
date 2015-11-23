import os
from utils import Singleton
# import db.util as util


def make_json(sql_list):
    dct = {}
    for (role, resource, method, perm) in sql_list:
        if role not in dct:
            dct[role] = {}
        if resource not in dct[role]:
            dct[role][resource] = {}
        if method not in dct[role][resource]:
            dct[role][resource].update({method: perm})
    return dct


sql_tuple = [['user', '/', 'GET', 'any'],
             ['admin', '/', 'GET', 'any'],
             ['admin', '/', 'PUT', 'any'],
             ['admin', '/api', 'GET', 'any'],
             ['admin', '/api', 'PUT', 'any'],
             ['admin', '/api', 'POST', 'any'],
             ['admin', '/api', 'DELETE', 'any'],
             ['moder', '/api', 'DELETE', 'any'],
             ['user', '/api', 'DELETE', 'None'],
             ['user', '/api', 'PUT', 'Own'],
             ['moder', '/new', 'DELETE', 'any'],
             ['moder', '/', 'GET', 'any'],
             ['moder', '/api', 'PUT', 'any'],
             ['user', '/api', 'GET', 'any']]


class Permission(object):
    __metaclass__ = Singleton

    def __init__(self):
        self.dct = None

    def create_dct(self):
        parsed_data = {}
        print '******NEW*****GO TO DB FOR PERM DICT******************'
        all_perms_list = sql_tuple
        if all_perms_list:
            parsed_data = [x for x in all_perms_list]
            # logger.warning(parsed_data)
        self.dct = make_json(parsed_data)
        return self.dct

    def get_dct(self):
        if self.dct is None:
            self.dct = self.create_dct()
        return self.dct

    def reload_dct(self):
        self.dct = self.create_dct()
        return self.dct

p1 = Permission()
# print p1
p2 = Permission()
# print p2
print p1 is p2

# print p1.get_dct()
# print p1.get_dct()
# print p2.get_dct()
# print p2.dct
# print p2.reload_dct()