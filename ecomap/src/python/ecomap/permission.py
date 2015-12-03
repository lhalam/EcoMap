# coding=utf-8
"""
Module providing complex and secure access control for all application's
resources by checking user role permissions predefined by admin.
Permission data stores in db. This module checks data from user's request
and compares it with dynamic permission App JSON object.

"""
import ecomap.utils
import ecomap.db.util as db

from flask import abort
from flask_login import current_user

from ecomap.app import logger


def make_json(sql_list):
    """Function providing transform data given from db into JSON object.
    :param sql_list: tuple of tuples from db.
    :return: json
    """
    dct = {}
    for (role, resource, method, perm) in sql_list:
        if role not in dct:
            dct[role] = {}
        if resource not in dct[role]:
            dct[role][resource] = {}
        if method not in dct[role][resource]:
            dct[role][resource].update({method: perm})
    return dct


def get_id_problem_owner(problem_id):
    """Method for checking custom dynamic url pattern.
    Returns id of problem owner
    :param problem_id - problem id
    :return: id of problem owner
    """
    user_owner_id = db.get_problem_owner(problem_id)
    return int(user_owner_id[0])


def get_current_user_id(user_id):
    """returns id of current user
    :param user_id - user id to check
    :return: id of problem owner
    """
    return current_user.uid if int(user_id) == int(current_user.uid) else False

RULEST_DICT = {':idUser': get_current_user_id,
               ':idProblem': get_id_problem_owner}

MODIFIERS = ['None', 'Own', 'Any']

MSG = {'forbidden': 'forbidden',
       '404': 'access is forbidden or resource not exists',
       'unknown_role': 'no role',
       'own': 'YOU HAVE ACCESS ONLY TO YOUR OWN %s',
       'warning': 'make this permission modifier = ANY!',
       'ok': 'ok'}


def check_static_route(dct, access, role, resource, method):
    """Method for checking access to static resources urls from user request.
    :param dct: dictionary with all permission rules given from db.
    :param access: result dictionary contains access control status and errors.
    :param role: role of user given from each request.
    :param resource: resource url requested by user to check.
    :param method: request method of resource url.
    :return: access - dictionary with checking status and results.
    """
    permissions = dct[role][resource]
    for i in permissions:
        if method in permissions:
            if permissions[method] == MODIFIERS[2]:
                access['status'] = MSG['ok']
            elif permissions[method] == MODIFIERS[1]:
                access['warning'] = MSG['warning']
            elif permissions[method] == MODIFIERS[0]:
                access['error'] = MSG['forbidden']
        else:
            access['error'] = MSG['forbidden']
    return access


def check_dynamic_route(dct, access, role, route, resource, method):
    """Method for checking access to dynamic resources urls from user request.
    Compares user's request params with access rules given from database.
    :param dct: dictionary with all permission rules given from db.
    :param access: result dictionary contains access control status and errors.
    :param role: role of user given from each request.
    :param resource: resource url requested by user to check.
    :param method: request method of resource url.
    :param route: resource url extracted from db to compare with user request url.
    :return: access - dictionary with checking status and results.
    """
    if ':' in str(route):
        pattern = route.split('/')[-1]
        dynamic_res_host = '/'.join(route.split('/')[:-1])
        request_res_arg = resource.split('/')[-1]
        request_res_host = '/'.join(resource.split('/')[:-1])

        if request_res_host == dynamic_res_host \
                and pattern in RULEST_DICT:
            owner_id = RULEST_DICT[pattern](request_res_arg)
            perms = dct[role][route]
            if method in perms:
                if perms[method] == MODIFIERS[2]:
                    access['status'] = MSG['ok']
                if perms[method] == MODIFIERS[1]:
                    if current_user.uid == owner_id:
                        access['status'] = MSG['ok']
                    else:
                        access['error'] = MSG['own'] % request_res_host
            else:
                access['error'] = 'else 404'

        elif '?' in resource and pattern in RULEST_DICT:
            access['status'] = MSG['ok']
        else:
            if not access['status'] == MSG['ok']:
                access['error'] = None
        return access


def check_permissions(role, resource, method, dct):
    """Main module's function. Handles permission control.
    Makes checking dynamic data from each request context with static
    permission rules created by administrator.
    :param role: current user role in request context
    :param resource: request url in absolute format with dynamic args.
    :param method: request method from context.
    :param dct: permission data from app db
    formatted into json-like object
    :return: True if access is allowed or status 403
    and error message otherwise
    """
    access = {'status': None, 'error': None}
    if role in dct:
        role_perms = dct[role]
        for route in role_perms:
            if resource in role_perms:
                check_static_route(dct, access, role, resource, method)
            else:
                check_dynamic_route(dct, access, role, route, resource, method)
    else:
        access['error'] = MSG['unknown_role']
    if not access['status'] == MSG['ok']:
        access['error'] = access['error'] or MSG['404']
    return access


class Permission(object):
    """
    Singleton class for store actual info about permissions.
    """
    __metaclass__ = ecomap.utils.Singleton

    def __init__(self):
        """init instance variables
        :return:
        """
        self.permissions_dict = None

    def create_dct(self):
        """Creates initial instance of permission rules.
        Call sql query and transform it into a json-like object.
        :return:
        """
        parsed_data = {}
        logger.info('<<<Permission Control Initialization>>>')
        all_perms_list = db.get_permission_control_data()
        if all_perms_list:
            parsed_data = [x for x in all_perms_list]
        self.permissions_dict = make_json(parsed_data)
        return self.permissions_dict

    def get_dct(self):
        """Implement singleton logic by creating data if it
        already not exist.
        :return:
        """
        if self.permissions_dict is None:
            self.permissions_dict = self.create_dct()
        return self.permissions_dict

    def reload_dct(self):
        """Providing reloading function
         which updates rules dictionary if needed.
        :return: new json-like object
        """
        self.permissions_dict = self.create_dct()
        return self.permissions_dict


permission_control = Permission()
