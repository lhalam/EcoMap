"""Validator module.
   Contains function to validate different forms in browser.
"""
import re

from ecomap.db import util as db

# variable, contains all possible enum in database
ENUM = {'action': ['POST', 'GET', 'PUT', 'DELETE'],
        'modifier': ['Any', 'Own', 'None']}

# pattern to validate email is email
EMAIL_PATTERN = re.compile(r'^[a-zA-Z0-9._]+@[a-zA-Z0-9._]+\.[a-zA-Z]{2,}$')

# dictionary, contains all mininum and maximum lengths for keys
LENGTHS = {'email': [5, 100],
           'first_name': [2, 255],
           'last_name': [2, 255],
           'password': [6, 100],
           'pass_confirm': [6, 100],
           'resource_name': [2, 100],
           'role_name': [2, 255],
           'description': [2, 255]}

# dictionary of error messages
ERROR_MSG = {'has_key': 'not contain %s key.',
             'check_minimum_length': '%s value is too short.',
             'check_maximum_length': '%s value is too long.',
             'check_string': '%s value is not string.',
             'check_email': '%s value does not look like email.',
             'check_empty': '%s value is empty.',
             'check_enum_value': 'invalid %s value.',
             'check_email_exist': 'email allready exists.',
             'name_exists': '"%s" name allready exists.'}


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
        elif not check_string(data, keyname):
            status['error'].append({keyname: ERROR_MSG['check_string']
                                    % keyname})
        elif not check_minimum_length(data, keyname, LENGTHS[keyname][0]):
            status['error'].append({keyname: ERROR_MSG['check_minimum_length']
                                    % keyname})
        elif not check_maximum_length(data, keyname, LENGTHS[keyname][1]):
            status['error'].append({keyname: ERROR_MSG['check_maximum_length']
                                    % keyname})
        elif keyname == 'email':
            if not check_email(data, keyname):
                status['error'].append({keyname: ERROR_MSG['check_email']
                                        % keyname})
            elif check_email_exist(data, keyname):
                status['error'].append({keyname:
                                        ERROR_MSG['check_email_exist']})

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
        elif not check_string(data, keyname):
            status['error'].append({keyname: ERROR_MSG['check_string']
                                    % keyname})
        elif not check_minimum_length(data, keyname, LENGTHS[keyname][0]):
            status['error'].append({keyname: ERROR_MSG['check_minimum_length']
                                    % keyname})
        elif not check_maximum_length(data, keyname, LENGTHS[keyname][1]):
            status['error'].append({keyname: ERROR_MSG['check_maximum_length']
                                    % keyname})
        elif keyname == 'email' and not check_email(data, keyname):
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
    elif not check_string(data, keyname):
        status['error'].append({keyname: ERROR_MSG['check_string'] % keyname})
    elif not check_minimum_length(data, keyname, LENGTHS[keyname][0]):
        status['error'].append({keyname: ERROR_MSG['check_minimum_length']
                                % keyname})
    elif not check_maximum_length(data, keyname, LENGTHS[keyname][1]):
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
        elif not check_empty(data, keyname):
            status['error'].append({keyname: ERROR_MSG['check_empty']
                                    % keyname})
        elif keyname == 'resource_name':
            if not check_string(data, keyname):
                status['error'].append({keyname: ERROR_MSG['check_string']
                                        % keyname})
            elif not check_minimum_length(data, keyname, LENGTHS[keyname][0]):
                status['error'].append({keyname:
                                        ERROR_MSG['check_minimum_length']
                                        % keyname})
            elif not check_maximum_length(data, keyname, LENGTHS[keyname][1]):
                status['error'].append({keyname:
                                        ERROR_MSG['check_maximum_length']
                                        % keyname})
            elif resource_name_exists(data, keyname):
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
    elif not check_empty(data, keyname):
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
    elif not check_empty(data, keyname):
        status['error'].append({keyname: ERROR_MSG['check_empty'] % keyname})
    elif not check_string(data, keyname):
        status['error'].append({keyname: ERROR_MSG['check_string'] % keyname})
    elif not check_minimum_length(data, keyname, LENGTHS[keyname][0]):
        status['error'].append({keyname: ERROR_MSG['check_minimum_length']
                                % keyname})
    elif not check_maximum_length(data, keyname, LENGTHS[keyname][1]):
        status['error'].append({keyname: ERROR_MSG['check_maximum_length']
                                % keyname})
    elif role_name_exists(data, keyname):
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
        elif not check_empty(data, keyname):
            status['error'].append({keyname: ERROR_MSG['check_empty']
                                    % keyname})
        elif keyname == 'role_name':
            if not check_string(data, keyname):
                status['error'].append({keyname: ERROR_MSG['check_string']
                                        % keyname})
            elif not check_minimum_length(data, keyname, LENGTHS[keyname][0]):
                status['error'].append({keyname:
                                        ERROR_MSG['check_minimum_length']
                                        % keyname})
            elif not check_maximum_length(data, keyname, LENGTHS[keyname][1]):
                status['error'].append({keyname:
                                        ERROR_MSG['check_maximum_length']
                                        % keyname})
            elif role_name_exists(data, keyname):
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
    elif not check_empty(data, keyname):
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
        elif not check_empty(data, keyname):
            status['error'].append({keyname: ERROR_MSG['check_empty']
                                    % keyname})
        elif (keyname in ['action', 'modifier']):
            if not check_enum_value(data, keyname, ENUM[keyname]):
                status['error'].append({keyname: ERROR_MSG['check_enum_value']
                                        % keyname})
        elif keyname == 'description':
            if not check_string(data, keyname):
                status['error'].append({keyname: ERROR_MSG['check_string']
                                        % keyname})
            elif not check_minimum_length(data, keyname, LENGTHS[keyname][0]):
                status['error'].append({keyname:
                                        ERROR_MSG['check_minimum_length']
                                        % keyname})
            elif not check_maximum_length(data, keyname, LENGTHS[keyname][1]):
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
        elif not check_empty(data, keyname):
            status['error'].append({keyname: ERROR_MSG['check_empty']
                                    % keyname})
        elif keyname in ['action', 'modifier']:
            if not check_enum_value(data, keyname, ENUM[keyname]):
                status['error'].append({keyname: ERROR_MSG['is_in_enum']
                                        % keyname})
        elif keyname == 'description':
            if not check_string(data, keyname):
                status['error'].append({keyname: ERROR_MSG['check_string']
                                        % keyname})
            elif not check_minimum_length(data, keyname, LENGTHS[keyname][0]):
                status['error'].append({keyname:
                                        ERROR_MSG['check_minimum_length']
                                        % keyname})
            elif not check_maximum_length(data, keyname, LENGTHS[keyname][1]):
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
    elif not check_empty(data, keyname):
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
        elif not check_empty(data, keyname):
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
    elif not check_empty(data, keyname):
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
        elif not check_empty(data, keyname):
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
    elif not check_empty(data, keyname):
        status['error'].append({keyname: ERROR_MSG['check_empty'] % keyname})
    elif not check_string(data, keyname):
        status['error'].append({keyname: ERROR_MSG['check_string'] % keyname})
    elif not check_minimum_length(data, keyname, LENGTHS[keyname][0]):
        status['error'].append({keyname: ERROR_MSG['check_minimum_length']
                                % keyname})
    elif not check_maximum_length(data, keyname, LENGTHS[keyname][1]):
        status['error'].append({keyname: ERROR_MSG['check_maximum_length']
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


def check_minimum_length(dictionary, keyname, minimum):
    """Validator function which checks if string is bigger than
       minimum value.
       :params: dictionary - dictionary
                keyname - key
                minimum - minimal length
    """
    return len(dictionary[keyname]) >= minimum


def check_maximum_length(dictionary, keyname, maximum):
    """Validator function which checks if string is smaller than
       minimum value.
       :params: dict - json dictionary
                keyname - dictionary key we want to check
                minimum - minimal length
    """
    return len(dictionary[keyname]) <= maximum


def check_email(dictionary, keyname):
    """Validator function, which checks if string is similar to email.
       Uses regular expression pattern, declared above.
       :params: dictionary - dictionary
                keyname - key
       :return: True - if string is similar to pattern
                False - if not
    """
    return EMAIL_PATTERN.match(dictionary[keyname])


def check_string(dictionary, keyname):
    """Validator function which checks if json value is string.
       :params: dictionary - dictionary
                keyname - key
       :return: True - if value is string
                False - if it is not
    """
    return isinstance(dictionary[keyname], basestring)


def check_enum_value(dictionary, keyname, enum):
    """Validator function which checks if json value is in enum.
       :params: dictionary - dictionary
                keyname - key
                enum - list of values
       :return: True - if value in enum
                False - if it is not
    """
    return dictionary[keyname] in enum


def check_email_exist(dictionary, keyname):
    """Validator function which checks if email is allready in database.
       :params: dictionary - dictionary
                keyname - key (email)
       :return: True - if email is free not in database
                False - if it is in database
    """
    return db.get_user_by_email(dictionary[keyname])


def check_empty(dictionary, keyname):
    """Validator function to check if dictionary key is not empty.
       :params: dictionary - dictionary
                keyname - key
       :return: True - if value is not empty
                False - if it is empty
    """
    return dictionary[keyname]


def role_name_exists(dictionary, keyname):
    """Validator function which checks if role name is allready in database.
       :params: dictionary - dictionary
                keyname - key
       :return: True - if name is free not in database
                False - if it is in database
    """
    return db.get_role_id(dictionary[keyname])


def resource_name_exists(dictionary, keyname):
    """Validator function which checks if resource name is allready in database.
       :params: dictionary - dictionary
                keyname - key
       :return: True - if resource is free not in database
                False - if it is in database
    """
    return db.get_resource_id(dictionary[keyname])
