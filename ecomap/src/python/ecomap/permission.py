"""
Module providing complex and secure access control for all application's
resources by checking user role permissions predifined by admin.
Permission data stores in db. This module checks data from user's request
and compares it with dynamic permission App JSON object.

"""
import ecomap.utils
import db.util as db

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
    return user_owner_id


def get_current_user_id(user_id):
    """returns id of current user
    :param user_id - user id to check
    :return: id of problem owner
    """
    return current_user.uid if int(user_id) == int(current_user.uid) else False


rules_dct = {':idUser': get_current_user_id,
             ':idProblem': get_id_problem_owner}


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
    perm = {'status': None, 'error': None}
    if role in dct:
        xpath = dct[role]
        for perm_res in xpath:
            if resource in dct[role]:
                for permissions in dct[role][resource]:
                    if method in dct[role][resource]:
                        if dct[role][resource][method] == 'Any':
                            perm['status'] = 'ok'
                        elif dct[role][resource][method] == 'Own':
                            perm['warning'] = 'static resource error'
                        elif dct[role][resource][method] == 'None':
                            perm['error'] = 'METHOD FORBIDDEN BY ADMIN'
                    else:
                        perm['error'] = 'METHOD FORBIDDEN'
            else:
                if ':' in perm_res:  # checking dynamic path
                    pattern = perm_res.split('/')[-1]
                    dynamic_res_host = '/'.join(perm_res.split('/')[:-1])
                    request_res_arg = resource.split('/')[-1]
                    request_res_host = '/'.join(resource.split('/')[:-1])
                    if request_res_host == dynamic_res_host \
                            and pattern in rules_dct:
                        owner_id = rules_dct[pattern](request_res_arg)
                        if dct[role][perm_res][method] == 'Any':
                            perm['status'] = 'ok'
                            return True
                        if dct[role][perm_res][method] == 'Own' \
                                and current_user.uid == owner_id:
                            perm['status'] = 'ok own'
                            return True
                        else:
                            perm['error'] = 'YOU CAN ACCESS ONLY YOUR' \
                                            ' OWN %s' % request_res_host
                            logger.warning(perm['error'])
                            logger.warning('UNABLE TO ACCESS to %s '
                                           'with user id %s',
                                           resource, current_user.uid)
                            abort(403)
                            return perm['error']
                else:
                    perm['error'] = 'NO SUCH RESOURCE FOR ROLE'
    else:
        perm['error'] = 'NOT ALLOWED FOR THIS ROLE'
    if not perm['error']:
        return True
    else:
        logger.warning(perm['error'])
        logger.warning('UNABLE TO ACCESS to %s with user id %s',
                       resource, current_user.uid)
        abort(403)
        return perm['error']


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
        logger.info('__Permission Control Initialization__')
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
