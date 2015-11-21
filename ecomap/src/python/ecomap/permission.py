import ecomap.utils
import db.util as util

from flask import abort

from ecomap.app import app


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

    def __init__(self ):
        pass

    def create_dct(self):
        parsed_data = {}
        all_perms_list = util.select_all()
        if all_perms_list:
            parsed_data = [x for x in all_perms_list]
            app.logger.warning(parsed_data)
        return make_json(parsed_data)


p = Permission()
control_dict = p.create_dct()


def get_perms():
    parsed_data = {}
    all_perms_list = util.select_all()
    if all_perms_list:
        parsed_data = [x for x in all_perms_list]
        app.logger.warning(parsed_data)
    return make_json(parsed_data)


# def check(role, resource, method, dct):
#     permission = {'status': None, 'error': None}
#     if role in dct:
#         if resource in dct[role]:
#             resource_methods = []
#             for perms in dct[role][resource]:
#                 resource_methods.append(perms.keys()[0])
#             if method in resource_methods:
#                 app.logger(method)
#                 permission['status'] = 'ok'
#             else:
#                 permission['error'] = 'METHOD FORBIDDEN'
#         else:
#             permission['error'] = 'NO SUCH RESOURCE FOR ROLE'
#     else:
#         permission['error'] = 'NOT ALLOWED FOR THIS ROLE'
#
#     app.logger.info(permission)
#     if not permission['error']:
#             return True
#     else:
#         return permission['error']

# print check(ROLE, REQUEST_RESOURCE, REQUEST_METHOD, dct3)


def check(role, resource, method, dct):
    permission = {'status': None, 'error': None}
    if role in dct:
        if resource in dct[role]:
            for perms in dct[role][resource]:
                if method in dct[role][resource] and dct[role][resource][method] is not 'None':
                    permission['status'] = 'ok'
                else:
                    permission['error'] = 'METHOD FORBIDDEN'
        else:
            permission['error'] = 'NO SUCH RESOURCE FOR ROLE'
    else:
        permission['error'] = 'NOT ALLOWED FOR THIS ROLE'

    print permission
    if not permission['error']:
            return True
    else:
        abort(403)
        return permission['error']

