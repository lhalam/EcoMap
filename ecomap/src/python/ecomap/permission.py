"""
Module providing complex and secure access control for all application's
resources by checking user role permissions predifined by admin.
Permission data stores in db. This module checks data from user's request
and compares it with dynamic permission App JSON object.

"""
import ecomap.utils
import db.util as util

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
    pass


def get_current_user_id(user_id):
    """returns id of current user
    :param user_id - user id to check
    :return: id of problem owner
    """
    return current_user.uid if int(user_id) == int(current_user.uid) else False


def get_id_photo_owner(photo_id):
    """Method for checking custom dynamic url pattern.
    :param photo_id - photo id
    :return: id_user
    """
    pass


dynamic_url_rules = {':idUser': get_current_user_id,
                     ':idProblem': get_id_problem_owner
                     }


def check_permissions(role, resource, method, dct):
    """Main module's function. Handles permission control.
    :param role:
    :param resource:
    :param method:
    :param dct:
    :return:
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
                    dynamic_res_pattern = perm_res.split('/')[-1]
                    dynamic_res_host = '/'.join(perm_res.split('/')[:-1])
                    request_res_arg = resource.split('/')[-1]
                    request_res_host = '/'.join(resource.split('/')[:-1])
                    if request_res_host == dynamic_res_host \
                            and dynamic_res_pattern in dynamic_url_rules:
                        owner_id = dynamic_url_rules \
                            [dynamic_res_pattern](request_res_arg)
                        if dct[role][perm_res][method] == 'Any':
                            perm['status'] = 'ok'
                            return True

                        if dct[role][perm_res][method] == 'Own':
                            if current_user.uid == owner_id:
                                perm['status'] = 'ok own'
                                return True
                            else:
                                perm['error'] = 'YOU HAVE ACCESS ONLY TO YOUR OWN %s' % request_res_host

                        # if dct[role][perm_res][method] == 'Own' \
                        #         and current_user.uid == owner_id:
                        #     perm['status'] = 'ok'
                        #     return True
                        # else:
                        #     perm['error'] = 'YOU CAN ACCESS ONLY YOUR OWN %s' \
                        #                     % request_res_host
                else:
                    perm['error'] = 'NO SUCH RESOURCE FOR ROLE'

                    #
                    # if request_res_host == dynamic_res_host:
                    #     print 'MATCH %s = %s' % (request_res_host, dynamic_res_host)
                    #     print dynamic_res_pattern
                    #     if dynamic_res_pattern in d:
                    #             owner_id = d[dynamic_res_pattern](request_res_arg)
                    #             if dct[role][permission_res][method] == 'Any':
                    #                 permission['status'] = 'ok any'
                    #                 return True
                    #             if dct[role][permission_res][method] == 'Own':
                    #                 if current_user.uid == owner_id:
                    #                     permission['status'] = 'ok own'
                    #                     return True
                    #                 else:
                    #                     permission['error'] = 'YOU HAVE ACCESS ONLY TO YOUR OWN %s' % request_res_host
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
    Singleton class for store actual info abou permissions.
    """
    __metaclass__ = ecomap.utils.Singleton

    def __init__(self):
        """
        init
        :return:
        """
        self.permissions_dict = None

    def create_dct(self):
        """

        :return:
        """
        parsed_data = {}
        logger.info('__Permission Control Initialization__')
        all_perms_list = util.get_permission_control_data()
        if all_perms_list:
            parsed_data = [x for x in all_perms_list]
        self.permissions_dict = make_json(parsed_data)
        return self.permissions_dict

    def get_dct(self):
        """

        :return:
        """
        if self.permissions_dict is None:
            self.permissions_dict = self.create_dct()
        return self.permissions_dict

    def reload_dct(self):
        """

        :return:
        """
        self.permissions_dict = self.create_dct()
        return self.permissions_dict


permission_control = Permission()
