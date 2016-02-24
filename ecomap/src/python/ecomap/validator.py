"""Validator module.
   Contains function to validate different forms in browser.
"""
import imghdr
import re

from ecomap.db import util as db

# Variable, contains all possible enum in database.
ENUM = {'action': ['POST', 'GET', 'PUT', 'DELETE'],
        'modifier': ['Any', 'Own', 'None']}

# Pattern to validate email is email.
EMAIL_PATTERN = re.compile(r'^[a-zA-Z0-9._]+@[a-zA-Z0-9._]+\.[a-zA-Z]{2,}$')

# Pattern to validate coordinates.
COORDINATES_PATTER = re.compile(r'^[-]{0,1}[0-9]{0,3}[.]{1}[0-9]{0,20}$')

# Dictionary, contains all mininum and maximum lengths for keys.
LENGTHS = {'email': [5, 100],
           'first_name': [2, 255],
           'last_name': [2, 255],
           'password': [6, 100],
           'pass_confirm': [6, 100],
           'resource_name': [2, 100],
           'role_name': [2, 255],
           'description': [2, 255],
           'title': [2, 255],
           'content': [2, 255],
           'problem_type_id': [1, 255],
           'problem_type_name': [1, 50],
           'problem_type_radius': [1, 10],
           'problem_type_picture': [1, 50],
           'user_id': [1, 255],
           'type': [1, 255],
           'latitude': [-90.0, 90.0],
           'longitude': [-180.0, 180.0]}

# Dictionary of error messages.
ERROR_MSG = {'has_key': 'not contain %s key.',
             'check_minimum_length': '%s value is too short.',
             'check_maximum_length': '%s value is too long.',
             'check_string': '%s value is not string.',
             'check_email': '%s value does not look like email.',
             'check_empty': '%s value is empty.',
             'check_enum_value': 'invalid %s value.',
             'check_email_exist': 'email allready exists.',
             'name_exists': '"%s" name allready exists.',
             'check_coordinates': '%s is not coordinates.',
             'check_coordinates_length': '%s is out of range.'}


def user_registration(data):
    """Validates user registration form. Checks: email, password,
       confirm password, first name, last name.
       :params: data - json object
       :return: dictionary with status key and error keys. By
                default status is True, and error is empty.
                If validation failed, status changes to False
                and error keynamename saves error ERROR_MSG
    """
    status = {'status': True, 'error': []}
    keys = ['email', 'first_name', 'last_name', 'password', 'pass_confirm']

    for keyname in keys:
        if not has_key(data, keyname):
            status['error'].append({keyname: ERROR_MSG['has_key'] % keyname})
        elif not data[keyname]:
            status['error'].append({keyname: ERROR_MSG['check_empty']
                                    % keyname})
        elif not check_string(data[keyname]):
            status['error'].append({keyname: ERROR_MSG['check_string']
                                    % keyname})
        elif not check_minimum_length(data[keyname], LENGTHS[keyname][0]):
            status['error'].append({keyname: ERROR_MSG['check_minimum_length']
                                    % keyname})
        elif not check_maximum_length(data[keyname], LENGTHS[keyname][1]):
            status['error'].append({keyname: ERROR_MSG['check_maximum_length']
                                    % keyname})
        elif keyname is 'email':
            if not check_email(data[keyname]):
                status['error'].append({keyname: ERROR_MSG['check_email']
                                        % keyname})
            elif check_email_exist(data[keyname]):
                status['error'].append({keyname:
                                        ERROR_MSG['check_email_exist']})

    if status['error']:
        status['status'] = False

    return status


def check_post_comment(data):
    """Validates if post comment request is valid.
       :params: data - dictionary of keys and field need to validate
       :return: dictionary with status keyname and error keys. By
                default status is True, and error is empty.
                If validation failed, status changes to False
                and error keyname saves error ERROR_MSG
    """
    status = {'status': True, 'error': []}
    keys = ['problem_id','parent_id','content']

    for keyname in keys:
        if not has_key(data, keyname):
            status['error'].append({keyname: ERROR_MSG['has_key'] % keyname})
        elif not data[keyname]:
            status['error'].append({keyname: ERROR_MSG['check_empty']
                                    % keyname})
        elif keyname is 'content':
            if not check_string(data[keyname]):
                status['error'].append({keyname: ERROR_MSG['check_string']
                                        % keyname})
            elif not check_minimum_length(data[keyname], LENGTHS[keyname][0]):
                status['error'].append({keyname:
                                        ERROR_MSG['check_minimum_length']
                                        % keyname})
            elif not check_maximum_length(data[keyname], LENGTHS[keyname][1]):
                status['error'].append({keyname:
                                        ERROR_MSG['check_maximum_length']
                                        % keyname})

    if status['error']:
        status['status'] = False

    return status


def hash_check(data):
    """Validates if restore password/user_deletion hash has length of 64.
       :params: data - hash, to check
       :return: dictionary with status keyname and error keys. By
                default status is True, and error is empty.
                If validation failed, status changes to False
                and error keyname saves error ERROR_MSG
    """
    status = {'status': True, 'error': []}
    if len(data) is not 64:
        status['error'].append({'hash_sum': 'hash sum has wrong length.'})
    elif not db.check_hash_in_db(data):
        status['error'].append({'hash_sum': 'hash does not exist.'})

    if status['error']:
        status['status'] = False

    return status


def user_login(data):
    """Validates user login form. Checks: email and password.
       :params: data - json object
       :return: dictionary with status keyname and error keys. By
                default status is True, and error is empty.
                If validation failed, status changes to False
                and error keyname saves error ERROR_MSG
    """
    status = {'status': True, 'error': []}
    keys = ['email', 'password']

    for keyname in keys:
        if not has_key(data, keyname):
            status['error'].append({keyname: ERROR_MSG['has_key'] % keyname})
        elif not data[keyname]:
            status['error'].append({keyname: ERROR_MSG['check_empty']
                                    % keyname})
        elif not check_string(data[keyname]):
            status['error'].append({keyname: ERROR_MSG['check_string']
                                    % keyname})
        elif not check_minimum_length(data[keyname], LENGTHS[keyname][0]):
            status['error'].append({keyname: ERROR_MSG['check_minimum_length']
                                    % keyname})
        elif not check_maximum_length(data[keyname], LENGTHS[keyname][1]):
            status['error'].append({keyname: ERROR_MSG['check_maximum_length']
                                    % keyname})
        elif keyname is 'email' and not check_email(data[keyname]):
            status['error'].append({keyname: ERROR_MSG['check_email']
                                    % keyname})

    if status['error']:
        status['status'] = False

    return status


def resource_post(data):
    """Validates resource post form. Checks: name of resource.
       :params: data - json object
       :return: dictionary with status keyname and error keys. By
                default status is True, and error is empty.
                If validation failed, status changes to False
                and error keyname saves error ERROR_MSG
    """
    status = {'status': True, 'error': []}
    keyname = 'resource_name'

    if not has_key(data, keyname):
        status['error'].append({keyname: ERROR_MSG['has_key'] % keyname})
    elif not data[keyname]:
        status['error'].append({keyname: ERROR_MSG['check_empty'] % keyname})
    elif not check_string(data[keyname]):
        status['error'].append({keyname: ERROR_MSG['check_string'] % keyname})
    elif not check_minimum_length(data[keyname], LENGTHS[keyname][0]):
        status['error'].append({keyname: ERROR_MSG['check_minimum_length']
                                % keyname})
    elif not check_maximum_length(data[keyname], LENGTHS[keyname][1]):
        status['error'].append({keyname: ERROR_MSG['check_maximum_length']
                                % keyname})

    if status['error']:
        status['status'] = False

    return status


def resource_put(data):
    """Validates resource put form. Checks: name and id of
       resource.
       :params: data - json object
       :return: dictionary with status keyname and error keys. By
                default status is True, and error is empty.
                If validation failed, status changes to False
                and error keyname saves error ERROR_MSG
    """
    status = {'status': True, 'error': []}
    keys = ['resource_name', 'resource_id']

    for keyname in keys:
        if not has_key(data, keyname):
            status['error'].append({keyname: ERROR_MSG['has_key']
                                    % keyname})
        elif not data[keyname]:
            status['error'].append({keyname: ERROR_MSG['check_empty']
                                    % keyname})
        elif keyname is 'resource_name':
            if not check_string(data[keyname]):
                status['error'].append({keyname: ERROR_MSG['check_string']
                                        % keyname})
            elif not check_minimum_length(data[keyname], LENGTHS[keyname][0]):
                status['error'].append({keyname:
                                        ERROR_MSG['check_minimum_length']
                                        % keyname})
            elif not check_maximum_length(data[keyname], LENGTHS[keyname][1]):
                status['error'].append({keyname:
                                        ERROR_MSG['check_maximum_length']
                                        % keyname})
            elif resource_name_exists(data[keyname]):
                status['error'].append({keyname: ERROR_MSG['name_exists']
                                        % data[keyname]})

    if status['error']:
        status['status'] = False

    return status


def resource_delete(data):
    """Validates resource delete form. Checks: id of resource.
       :params: data - json object
       :return: dictionary with status keyname and error keys. By
                default status is True, and error is empty.
                If validation failed, status changes to False
                and error keyname saves error ERROR_MSG
    """
    status = {'status': True, 'error': []}
    keyname = 'resource_id'

    if not has_key(data, keyname):
        status['error'].append({keyname: ERROR_MSG['has_key'] % keyname})
    elif not data[keyname]:
        status['error'].append({keyname: ERROR_MSG['check_empty']
                                % keyname})

    if status['error']:
        status['status'] = False

    return status


def role_post(data):
    """Validates role post form. Checks: name of role.
       :params: data - json object
       :return: dictionary with status keyname and error keys. By
                default status is True, and error is empty.
                If validation failed, status changes to False
                and error keyname saves error ERROR_MSG
    """
    status = {'status': True, 'error': []}
    keyname = 'role_name'

    if not has_key(data, keyname):
        status['error'].append({keyname: ERROR_MSG['has_key'] % keyname})
    elif not data[keyname]:
        status['error'].append({keyname: ERROR_MSG['check_empty'] % keyname})
    elif not check_string(data[keyname]):
        status['error'].append({keyname: ERROR_MSG['check_string'] % keyname})
    elif not check_minimum_length(data[keyname], LENGTHS[keyname][0]):
        status['error'].append({keyname: ERROR_MSG['check_minimum_length']
                                % keyname})
    elif not check_maximum_length(data[keyname], LENGTHS[keyname][1]):
        status['error'].append({keyname: ERROR_MSG['check_maximum_length']
                                % keyname})
    elif role_name_exists(data[keyname]):
        status['error'].append({keyname: ERROR_MSG['name_exists']
                                % data[keyname]})

    if status['error']:
        status['status'] = False

    return status


def role_put(data):
    """Validates role put form. Checks: id and name of role.
       :params: data - json object
       :return: dictionary with status keyname and error keys. By
                default status is True, and error is empty.
                If validation failed, status changes to False
                and error keyname saves error ERROR_MSG
    """
    status = {'status': True, 'error': []}
    keys = ['role_id', 'role_name']

    for keyname in keys:
        if not has_key(data, keyname):
            status['error'].append({keyname: ERROR_MSG['has_key'] % keyname})
        elif not data[keyname]:
            status['error'].append({keyname: ERROR_MSG['check_empty']
                                    % keyname})
        elif keyname is 'role_name':
            if not check_string(data[keyname]):
                status['error'].append({keyname: ERROR_MSG['check_string']
                                        % keyname})
            elif not check_minimum_length(data[keyname], LENGTHS[keyname][0]):
                status['error'].append({keyname:
                                        ERROR_MSG['check_minimum_length']
                                        % keyname})
            elif not check_maximum_length(data[keyname], LENGTHS[keyname][1]):
                status['error'].append({keyname:
                                        ERROR_MSG['check_maximum_length']
                                        % keyname})
            elif role_name_exists(data[keyname]):
                status['error'].append({keyname: ERROR_MSG['name_exists']
                                        % data[keyname]})

    if status['error']:
        status['status'] = False

    return status


def role_delete(data):
    """Validates role delete form. Checks: id of role.
       :params: data - json object
       :return: dictionary with status keyname and error keys. By
                default status is True, and error is empty.
                If validation failed, status changes to False
                and error keyname saves error ERROR_MSG
    """
    status = {'status': True, 'error': []}
    keyname = 'role_id'

    if not has_key(data, keyname):
        status['error'].append({keyname: ERROR_MSG['has_key'] % keyname})
    elif not data[keyname]:
        status['error'].append({keyname: ERROR_MSG['check_empty'] % keyname})

    if status['error']:
        status['status'] = False

    return status


def permission_post(data):
    """Validates permission post form. Checks: id of resource and
       action (POST, PUT, GET, DELETE), modifier (Any, Own, None)
       and description of permission.
       :params: data - json object
       :return: dictionary with status keyname and error keys. By
                default status is True, and error is empty.
                If validation failed, status changes to False
                and error keyname saves error ERROR_MSG
    """
    status = {'status': True, 'error': []}
    keys = ['resource_id', 'action', 'modifier', 'description']

    for keyname in keys:
        if not has_key(data, keyname):
            status['error'].append({keyname: ERROR_MSG['has_key'] % keyname})
        elif not data[keyname]:
            status['error'].append({keyname: ERROR_MSG['check_empty']
                                    % keyname})
        elif (keyname in ['action', 'modifier']):
            if not check_enum_value(data[keyname], ENUM[keyname]):
                status['error'].append({keyname: ERROR_MSG['check_enum_value']
                                        % keyname})
        elif keyname is 'description':
            if not check_string(data[keyname]):
                status['error'].append({keyname: ERROR_MSG['check_string']
                                        % keyname})
            elif not check_minimum_length(data[keyname], LENGTHS[keyname][0]):
                status['error'].append({keyname:
                                        ERROR_MSG['check_minimum_length']
                                        % keyname})
            elif not check_maximum_length(data[keyname], LENGTHS[keyname][1]):
                status['error'].append({keyname:
                                        ERROR_MSG['check_maximum_length']
                                        % keyname})

    if status['error']:
        status['status'] = False

    return status


def permission_put(data):
    """Validates permission put form. Checks: id of resource and
       action (POST, PUT, GET, DELETE), modifier (Any, Own, None)
       and description of permission.
       :params: data - json object
       :return: dictionary with status keyname and error keys. By
                default status is True, and error is empty.
                If validation failed, status changes to False
                and error keyname saves error ERROR_MSG
    """
    status = {'status': True, 'error': []}
    keys = ['permission_id', 'action', 'modifier', 'description']

    for keyname in keys:
        if not has_key(data, keyname):
            status['error'].append({keyname: ERROR_MSG['has_key'] % keyname})
        elif not data[keyname]:
            status['error'].append({keyname: ERROR_MSG['check_empty']
                                    % keyname})
        elif keyname in ['action', 'modifier']:
            if not check_enum_value(data[keyname], ENUM[keyname]):
                status['error'].append({keyname: ERROR_MSG['check_enum_value']
                                        % keyname})
        elif keyname is 'description':
            if not check_string(data[keyname]):
                status['error'].append({keyname: ERROR_MSG['check_string']
                                        % keyname})
            elif not check_minimum_length(data[keyname], LENGTHS[keyname][0]):
                status['error'].append({keyname:
                                        ERROR_MSG['check_minimum_length']
                                        % keyname})
            elif not check_maximum_length(data[keyname], LENGTHS[keyname][1]):
                status['error'].append({keyname:
                                        ERROR_MSG['check_maximum_length']
                                        % keyname})

    if status['error']:
        status['status'] = False

    return status


def permission_delete(data):
    """Validates permission delete form. Checks: id of permission.
       :params: data - json object
       :return: dictionary with status keyname and error keys. By
                default status is True, and error is empty.
                If validation failed, status changes to False
                and error keyname saves error ERROR_MSG
    """
    status = {'status': True, 'error': []}
    keyname = 'permission_id'

    if not has_key(data, keyname):
        status['error'].append({keyname: ERROR_MSG['has_key'] % keyname})
    elif not data[keyname]:
        status['error'].append({keyname: ERROR_MSG['check_empty'] % keyname})

    if status['error']:
        status['status'] = False

    return status


def role_permission_post(data):
    """Validates role permission post form. Checks: id of permission
       and id of role.
       :params: data - json object
       :return: dictionary with status keyname and error keys. By
                default status is True, and error is empty.
                If validation failed, status changes to False
                and error keyname saves error ERROR_MSG
    """
    status = {'status': True, 'error': []}
    keys = ['role_id', 'permission_id']

    for keyname in keys:
        if not has_key(data, keyname):
            status['error'].append({keyname: ERROR_MSG['has_key'] % keyname})
        elif not data[keyname]:
            status['error'].append({keyname: ERROR_MSG['check_empty']
                                    % keyname})

    if status['error']:
        status['status'] = False

    return status


def role_permission_put(data):
    """Validates role permission put form. Checks: id of permission
       and id of role.
       :params: data - json object
       :return: dictionary with status keyname and error keys. By
                default status is True, and error is empty.
                If validation failed, status changes to False
                and error keyname saves error ERROR_MSG
    """
    return role_permission_post(data)


def role_permission_delete(data):
    """Validates role permission delete form. Checks: id of role.
       :params: data - json object
       :return: dictionary with status keyname and error keys. By
                default status is True, and error is empty.
                If validation failed, status changes to False
                and error keyname saves error ERROR_MSG
    """
    status = {'status': True, 'error': []}
    keyname = 'role_id'

    if not has_key(data, keyname):
        status['error'].append({keyname: ERROR_MSG['has_key'] % keyname})
    elif not data[keyname]:
        status['error'].append({keyname: ERROR_MSG['check_empty'] % keyname})

    if status['error']:
        status['status'] = False

    return status


def user_role_put(data):
    """Validates user role post form. Checks: id of user
       and id of role.
       :params: data - json object
       :return: dictionary with status keyname and error keys. By
                default status is True, and error is empty.
                If validation failed, status changes to False
                and error keyname saves error ERROR_MSG
    """
    status = {'status': True, 'error': []}
    keys = ['role_id', 'user_id']

    for keyname in keys:
        if not has_key(data, keyname):
            status['error'].append({keyname: ERROR_MSG['has_key'] % keyname})
        elif not data[keyname]:
            status['error'].append({keyname: ERROR_MSG['check_empty']
                                    % keyname})

    if status['error']:
        status['status'] = False

    return status


def change_password(data):
    """Validates change user password form. Checks old password,
       new password and id of user.
       :params: data - json object
       :return: dictionary with status keyname and error keys. By
                default status is True, and error is empty.
                If validation failed, status changes to False
                and error keyname saves error ERROR_MSG
    """
    status = {'status': True, 'error': []}
    keyname = 'password'

    if not has_key(data, keyname):
        status['error'].append({keyname: ERROR_MSG['has_key'] % keyname})
    elif not data[keyname]:
        status['error'].append({keyname: ERROR_MSG['check_empty'] % keyname})
    elif not check_string(data[keyname]):
        status['error'].append({keyname: ERROR_MSG['check_string'] % keyname})
    elif not check_minimum_length(data[keyname], LENGTHS[keyname][0]):
        status['error'].append({keyname: ERROR_MSG['check_minimum_length']
                                % keyname})
    elif not check_maximum_length(data[keyname], LENGTHS[keyname][1]):
        status['error'].append({keyname: ERROR_MSG['check_maximum_length']
                                % keyname})

    if status['error']:
        status['status'] = False

    return status


def problem_post(data):
    """Validates problem post form.
       :params: data - json object
       :return: dictionary with status keyname and error keys. By
                default status is True, and error is empty.
                If validation failed, status changes to False
                and error keyname saves error ERROR_MSG
    """
    status = {'status': True, 'error': []}
    keys = ['title', 'content', 'latitude', 'longitude', 'type']
    for keyname in keys:
        if not has_key(data, keyname):
            status['error'].append({keyname: ERROR_MSG['has_key'] % keyname})
        elif not data[keyname]:
            status['error'].append({keyname:
                                    ERROR_MSG['check_empty'] % keyname})
        elif keyname in ['title', 'content']:
            if not check_string(data[keyname]):
                status['error'].append({keyname:
                                        ERROR_MSG['check_string'] % keyname})
            elif not check_minimum_length(data[keyname], LENGTHS[keyname][0]):
                status['error'].append({keyname:
                                        ERROR_MSG['check_minimum_length']
                                        % keyname})
            elif not check_maximum_length(data[keyname], LENGTHS[keyname][1]):
                status['error'].append({keyname:
                                        ERROR_MSG['check_maximum_length']
                                        % keyname})
        elif keyname in ['latitude', 'longitude']:
            if not check_coordinates(data[keyname]):
                status['error'].append({keyname:
                                        ERROR_MSG['check_coordinates']
                                        % data[keyname]})
            if not check_coordinates_length(data[keyname], LENGTHS[keyname]):
                status['error'].append({keyname:
                                        ERROR_MSG['check_coordinates_length']
                                        % data[keyname]})

    if status['error']:
        status['status'] = False

    return status


def problem_type_post(data):
    """Validates permission put form. Checks: problem type id, name, radius.
       :params: data - json object
       :return: dictionary with status keyname and error keys. By
                default status is True, and error is empty.
                If validation failed, status changes to False
                and error keyname saves error ERROR_MSG
    """
    status = {'status': True, 'error': []}
    keys = ['problem_type_name', 'problem_type_radius']

    for keyname in keys:
        if not has_key(data, keyname):
            status['error'].append({keyname: ERROR_MSG['has_key'] % keyname})
        elif not data[keyname]:
            status['error'].append({keyname: ERROR_MSG['check_empty']
                                    % keyname})
        elif keyname is 'problem_type_name':
            if not check_string(data[keyname]):
                status['error'].append({keyname: ERROR_MSG['check_string']
                                        % keyname})
            elif not check_minimum_length(data[keyname], LENGTHS[keyname][0]):
                status['error'].append({keyname:
                                        ERROR_MSG['check_minimum_length']
                                        % keyname})
            elif not check_maximum_length(data[keyname], LENGTHS[keyname][1]):
                status['error'].append({keyname:
                                        ERROR_MSG['check_maximum_length']
                                        % keyname})
        elif keyname is 'problem_type_radius':
            if not check_minimum_length(data[keyname], LENGTHS[keyname][0]):
                status['error'].append({keyname:
                                        ERROR_MSG['check_minimum_length']
                                        % keyname})
            elif not check_maximum_length(data[keyname], LENGTHS[keyname][1]):
                status['error'].append({keyname:
                                        ERROR_MSG['check_maximum_length']
                                        % keyname})

    if status['error']:
        status['status'] = False

    return status


def problem_type_delete(data):
    """Validates problem type delete form. Checks: id of problem type.
       :params: data - json object
       :return: dictionary with status keyname and error keys. By
                default status is True, and error is empty.
                If validation failed, status changes to False
                and error keyname saves error ERROR_MSG
    """
    status = {'status': True, 'error': []}
    keyname = 'problem_type_id'
    if not has_key(data, keyname):
        status['error'].append({keyname: ERROR_MSG['has_key'] % keyname})
    elif not data[keyname]:
        status['error'].append({keyname: ERROR_MSG['check_empty']
                                % keyname})
    if status['error']:
        status['status'] = False
    return status


def problem_type_put(data):
    """Validates permission put form. Checks: problem type id, name, radius.
       :params: data - json object
       :return: dictionary with status keyname and error keys. By
                default status is True, and error is empty.
                If validation failed, status changes to False
                and error keyname saves error ERROR_MSG
    """
    status = {'status': True, 'error': []}
    keys = ['problem_type_id', 'problem_type_name', 'problem_type_radius']

    for keyname in keys:
        if not has_key(data, keyname):
            status['error'].append({keyname: ERROR_MSG['has_key'] % keyname})
        elif not data[keyname]:
            status['error'].append({keyname: ERROR_MSG['check_empty']
                                    % keyname})
        if keyname is 'problem_type_name':
            if not check_string(data[keyname]):
                status['error'].append({keyname: ERROR_MSG['check_string']
                                        % keyname})
            elif not check_minimum_length(data[keyname], LENGTHS[keyname][0]):
                status['error'].append({keyname:
                                        ERROR_MSG['check_minimum_length']
                                        % keyname})
            elif not check_maximum_length(data[keyname], LENGTHS[keyname][1]):
                status['error'].append({keyname:
                                        ERROR_MSG['check_maximum_length']
                                        % keyname})
        elif keyname is 'problem_type_radius':
            if not check_minimum_length(data[keyname], LENGTHS[keyname][0]):
                status['error'].append({keyname:
                                        ERROR_MSG['check_minimum_length']
                                        % keyname})
            elif not check_maximum_length(data[keyname], LENGTHS[keyname][1]):
                status['error'].append({keyname:
                                        ERROR_MSG['check_maximum_length']
                                        % keyname})

    if status['error']:
        status['status'] = False

    return status


def has_key(dictionary, keyname):
    """Validator function, which checks if there is all needed keys json
       object.
       :params: dictionary - json dictionary we want to check
                keyname - key, we expect to get from json
       :return: True - if all is ok
                False - if there is no expected keyname
    """
    return keyname in dictionary


def check_minimum_length(string, minimum):
    """Validator function which checks if string is bigger than
       minimum value.
       :params: string - string to check
                minimum - minimal length
    """
    return len(string) >= minimum


def check_maximum_length(string, maximum):
    """Validator function which checks if string is smaller than
       minimum value.
       :params: string - string to check
                minimum - minimal length
    """
    return len(string) <= maximum


def check_email(email):
    """Validator function, which checks if string is similar to email.
       Uses regular expression pattern, declared above.
       :params: email - string to check
       :return: True - if string is similar to pattern
                False - if not
    """
    return EMAIL_PATTERN.match(email)


def check_string(value):
    """Validator function which checks if json value is string.
       :params: value - string to check
       :return: True - if value is string
                False - if it is not
    """
    return isinstance(value, basestring)


def check_enum_value(value, enum):
    """Validator function which checks if json value is in enum.
       :params: value - string to check
       :return: True - if value in enum
                False - if it is not
    """
    return value in enum


def check_email_exist(email):
    """Validator function which checks if email is allready in database.
       :params: dictionary - dictionary
                keyname - key (email)
       :return: True - if it is in database
                False - if name is free not in database
    """
    return bool(db.get_user_by_email(email))


def role_name_exists(role_name):
    """Validator function which checks if role name is allready in database.
       :params: role_name - string to check
       :return: True - if it is in database
                False - if name is free not in database
    """
    return bool(db.get_role_by_name(role_name))


def resource_name_exists(resource_name):
    """Validator function which checks if resource name is allready in database.
       :params: resource_name - string to check
       :return: True - if it is in database
                False - if name is free not in database
    """
    return bool(db.get_resource_id(resource_name))


def validate_image_file(img_file):
    """Custom validation by file type.
    :parems: img_file - file uploaded by user in base64
    :return: True - if if extension is valid
                False - if file not in png format
    """
    return True if str(imghdr.what(img_file)) is 'png' else False


def user_photo_deletion(data):
    """Custom validation to identify photo owner.
    :parems: value - user data to check
    :return: True - id data is valid
                False - if data is not valid
    """
    status = {'status': True, 'error': []}
    keyname = 'user_id'

    if not has_key(data, keyname):
        status['error'].append({keyname: ERROR_MSG['has_key'] % keyname})
    elif not data[keyname]:
        status['error'].append({keyname: ERROR_MSG['check_empty'] % keyname})

    if status['error']:
        status['status'] = False

    return status


def check_coordinates(value):
    """Validator function to check if value looks like coordinates.
       :params: value - string to check
       :return: True - it value looks like coordinates
                False - if it is not
    """
    return COORDINATES_PATTER.match(value)


def check_coordinates_length(value, length):
    """Validator function to check if longitude or latitude is
       in valid range (from -90 to 90 for latitude and -180 to
       180 for longitude).
       :params: value - string to check
                length - minimum and maximum range (list)
       :return: True - if inside range
                False - if not
    """
    result = False
    if float(value) >= length[0] and float(value) <= length[1]:
        result = True
    return result
