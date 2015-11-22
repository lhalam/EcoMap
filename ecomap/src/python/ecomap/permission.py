import ecomap.utils
import db.util as util
import logging

from ecomap.app import logger
# logger = logging.getLogger('ololo')


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


class Permission(object):
    __metaclass__ = ecomap.utils.Singleton

    def __init__(self):
        self.dct = None
        self.logger = logging.getLogger('perm_control_class')

    def create_dct(self):
        parsed_data = {}
        logger.warning('<<<<<<<<<<<<<<<<<<<<GOTO DB>>>>>>>>>>>>>>>>>>>>')
        all_perms_list = util.select_all()
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

p_instance = Permission()
# pddd = p_instance.get_dct()
# p_inst2 = Permission()
# logger.warning(p_instance is p_inst2)
# dct = permissions.create_dct()


def get_perms():
    parsed_data = {}
    all_perms_list = util.select_all()
    if all_perms_list:
        parsed_data = [x for x in all_perms_list]
        # logger.warning(parsed_data)
    return make_json(parsed_data)

