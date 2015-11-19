import db.util as util

from ecomap.app import app


def make_json(sql_list):
    """
    MOVE THIS SOMEWHERE AND RENAME
    PARSES DB TUPLE INTO JSON
    :param sql_list:
    :return:
    """
    dct = {}
    for (role, resource, method, perm) in sql_list:
        if resource not in dct:
            dct[resource] = {}
        if method not in dct[resource]:
            dct[resource][method] = []
        if role not in dct[resource][method]:
            dct[resource][method].append({role: perm})
    return dct


def get_perms():
    all_perms_list = util.select_all()
    if all_perms_list:
        parsed_data = [x for x in all_perms_list]
        app.logger.warning(parsed_data)
        return make_json(parsed_data)