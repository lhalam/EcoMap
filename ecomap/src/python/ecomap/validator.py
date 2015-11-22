"""Validator module.
   Contains function to validate different forms in browser.
"""
import re

MODIFIERS = ['any', 'own', 'none']
ACTIONS = ['post', 'get', 'put', 'delete']
EMAIL_PATTERN = re.compile(r'^[a-zA-Z0-9._]+@[a-zA-Z0-9._]+\.[a-zA-Z]{2,}$')

MESSAGE = {'is_in_dictionary': 'not contain %s key.',
           'is_enough_length': '%s value it too long or short.',
           'is_not_empty': '%s field is empty.',
           'is_string': '%s value is not string.',
           'is_email': '%s value does not look like email.',
           'is_in_enum': 'invalid %s value'}


def validate_user_registration(data):
    """Validates user registration form. Checks: email, password,
       confirm password, first name, last name.
       :params: data - json object
       :return: dictionary with status key and error keys. By
                default status is True, and error is empty.
                If validation failed, status changes to False
                and error key saves error message
    """
    status = {'status': True, 'error': ''}

    result = validate_string(data, 'email', 5, 100)
    if not result:
        result = validate_string(data, 'firstName', 2, 255)
    if not result:
        result = validate_string(data, 'lastName', 2, 255)
    if not result:
        result = validate_string(data, 'password', 6, 100)
    if not result:
        result = validate_string(data, 'pass_confirm', 6, 100)
    if result:
        status['status'] = False
        status['error'] = result
    return status


def validate_user_login(data):
    """Validates user login form. Checks: email and password.
       :params: data - json object
       :return: dictionary with status key and error keys. By
                default status is True, and error is empty.
                If validation failed, status changes to False
                and error key saves error message
    """
    status = {'status': True, 'error': ''}

    result = validate_string(data, 'password', 6, 100)
    if not result:
        result = validate_string(data, 'email', 5, 100)
    if result:
        status['status'] = False
        status['error'] = result
    return status


def validate_resource_post(data):
    """Validates resource post form. Checks: name of resource.
       :params: data - json object
       :return: dictionary with status key and error keys. By
                default status is True, and error is empty.
                If validation failed, status changes to False
                and error key saves error message
    """
    status = {'status': True, 'error': ''}

    result = validate_string(data, 'resource_name', 2, 100)
    if result:
        status['status'] = False
        status['error'] = result
    return status


def validate_resource_put(data):
    """Validates resource put form. Checks: name and id of
       resource.
       :params: data - json object
       :return: dictionary with status key and error keys. By
                default status is True, and error is empty.
                If validation failed, status changes to False
                and error key saves error message
    """
    status = {'status': True, 'error': ''}

    result = validate_int(data, 'resource_id')
    if not result:
        result = validate_string(data, 'new_resource_name', 2, 100)
    if result:
        status['status'] = False
        status['error'] = result
    return status


def validate_resource_delete(data):
    """Validates resource delete form. Checks: id of resource.
       :params: data - json object
       :return: dictionary with status key and error keys. By
                default status is True, and error is empty.
                If validation failed, status changes to False
                and error key saves error message
    """
    status = {'status': True, 'error': ''}

    result = validate_int(data, 'resource_id')
    if result:
        status['status'] = False
        status['error'] = result
    return status


def validate_role_post(data):
    """Validates role post form. Checks: name of role.
       :params: data - json object
       :return: dictionary with status key and error keys. By
                default status is True, and error is empty.
                If validation failed, status changes to False
                and error key saves error message
    """
    status = {'status': True, 'error': ''}

    result = validate_string(data, 'name', 2, 255)
    if result:
        status['status'] = False
        status['error'] = result
    return status


def validate_role_put(data):
    """Validates role put form. Checks: id and name of role.
       :params: data - json object
       :return: dictionary with status key and error keys. By
                default status is True, and error is empty.
                If validation failed, status changes to False
                and error key saves error message
    """
    status = {'status': True, 'error': ''}

    result = validate_int(data, 'role_id')
    if not result:
        result = validate_string(data, 'new_role_name', 2, 255)
    if result:
        status['status'] = False
        status['error'] = result
    return status


def validate_role_delete(data):
    """Validates role delete form. Checks: id of role.
       :params: data - json object
       :return: dictionary with status key and error keys. By
                default status is True, and error is empty.
                If validation failed, status changes to False
                and error key saves error message
    """
    status = {'status': True, 'error': ''}

    result = validate_int(data, 'role_id')
    if result:
        status['status'] = False
        status['error'] = result
    return status


def validate_permission_post(data):
    """Validates permission post form. Checks: id of resource and
       action (POST, PUT, GET, DELETE), modifier (Any, Own, None)
       and description of permission.
       :params: data - json object
       :return: dictionary with status key and error keys. By
                default status is True, and error is empty.
                If validation failed, status changes to False
                and error key saves error message
    """
    status = {'status': True, 'error': ''}

    result = validate_int(data, 'resource_id')
    if not result:
        result = validate_enum(data, 'action', ACTIONS)
    if not result:
        result = validate_enum(data, 'modifier', MODIFIERS)
    if not result:
        result = validate_string(data, 'description', 1, 255)
    if result:
        status['status'] = False
        status['error'] = result
    return status


def validate_permission_put(data):
    """Validates permission put form. Checks: id of resource and
       action (POST, PUT, GET, DELETE), modifier (Any, Own, None)
       and description of permission.
       :params: data - json object
       :return: dictionary with status key and error keys. By
                default status is True, and error is empty.
                If validation failed, status changes to False
                and error key saves error message
    """
    status = {'status': True, 'error': ''}

    result = validate_int(data, 'resource_id')
    if not result:
        result = validate_enum(data, 'new_action', ACTIONS)
    if not result:
        result = validate_enum(data, 'new_modifier', MODIFIERS)
    if not result:
        result = validate_string(data, 'new_description', 1, 255)
    if result:
        status['status'] = False
        status['error'] = result
    return status


def validate_permission_delete(data):
    """Validates permission delete form. Checks: id of permission.
       :params: data - json object
       :return: dictionary with status key and error keys. By
                default status is True, and error is empty.
                If validation failed, status changes to False
                and error key saves error message
    """
    status = {'status': True, 'error': ''}

    result = validate_int(data, 'permission_id')
    if result:
        status['status'] = False
        status['error'] = result
    return status


def validate_role_permission_post(data):
    """Validates role permission post form. Checks: id of permission
       and id of role.
       :params: data - json object
       :return: dictionary with status key and error keys. By
                default status is True, and error is empty.
                If validation failed, status changes to False
                and error key saves error message
    """
    status = {'status': True, 'error': ''}

    result = validate_int(data, 'role_id')
    if not result:
        result = validate_int(data, 'permission_id')
    if result:
        status['status'] = False
        status['error'] = result
    return status


def validate_role_permission_put(data):
    """Validates role permission put form. Checks: id of permission
       and id of role.
       :params: data - json object
       :return: dictionary with status key and error keys. By
                default status is True, and error is empty.
                If validation failed, status changes to False
                and error key saves error message
    """
    status = {'status': True, 'error': ''}

    result = validate_int(data, 'role_id')
    if not result:
        result = validate_int(data, 'permission_id')
    if result:
        status['status'] = False
        status['error'] = result
    return status


def validate_role_permission_delete(data):
    """Validates role permission delete form. Checks: id of role.
       :params: data - json object
       :return: dictionary with status key and error keys. By
                default status is True, and error is empty.
                If validation failed, status changes to False
                and error key saves error message
    """
    status = {'status': True, 'error': ''}

    result = validate_int(data, 'role_id')
    if result:
        status['status'] = False
        status['error'] = result
    return status


def validate_user_role_post(data):
    """Validates user role post form. Checks: id of user
       and id of role.
       :params: data - json object
       :return: dictionary with status key and error keys. By
                default status is True, and error is empty.
                If validation failed, status changes to False
                and error key saves error message
    """
    status = {'status': True, 'error': ''}

    result = validate_int(data, 'role_id')
    if not result:
        result = validate_int(data, 'user_id')
    if result:
        status['status'] = False
        status['error'] = result
    return status


def validate_change_password(data):
    """Validates change user password form. Checks old password,
       new password and id of user.
       :params: data - json object
       :return: dictionary with status key and error keys. By
                default status is True, and error is empty.
                If validation failed, status changes to False
                and error key saves error message
    """
    status = {'status': True, 'error': ''}

    result = validate_int(data, 'id')
    if not result:
        result = validate_string(data, 'old_pass', 6, 100)
    if not result:
        result = validate_string(data, 'new_pass', 6, 100)
    if result:
        status['status'] = False
        status['error'] = result
    return status


def validate_string(data, key, minimum=0, maximum=0):
    """Function to validate string values.
       :params: data - json object
                key - json key
                min - minimal length of value
                max - maximum length of value
       :return: error message - if not passed validation
                None - if passed
    """
    result = None
    if not is_in_dictionary(data, key):
        result = MESSAGE['is_in_dictionary'] % key
    elif not is_not_empty(data, key):
        result = MESSAGE['is_not_empty'] % key
    elif not is_string(data, key):
        result = MESSAGE['is_string'] % key
    elif not is_enough_length(data, key, minimum, maximum):
        result = MESSAGE['is_enough_length'] % key
    elif key == 'email' and not is_email(data, key):
        result = MESSAGE['is_email'] % key
    return result


def validate_enum(data, key, enum):
    """Function to validate enum values.
       :params: data - json object
                key - json key
                enum - list of allowed values
       :return: error message - if not passed validation
                None - if passed
    """
    result = None
    if not is_in_dictionary(data, key):
        result = MESSAGE['is_in_dictionary'] % key
    elif not is_not_empty(data, key):
        result = MESSAGE['is_not_empty'] % key
    elif not is_in_enum(data, key, enum):
        result = MESSAGE['is_in_enum'] % key
    return result


def validate_int(data, key):
    """Function to validate id values.
       :params: data - json object
                key - json key
       :return: error message - if not passed validation
                None - if passed
    """
    result = None
    if not is_in_dictionary(data, key):
        result = MESSAGE['is_in_dictionary'] % key
    elif not is_not_empty(data, key):
        result = MESSAGE['is_not_empty'] % key
    return result


def is_in_dictionary(json, key):
    """Validator function, which checks if there is all needed keys json
       object.
       :params: json - json dictionary we want to check
                key - key, we expect to get from json
       :return: True - if all is ok
                False - if there is no expected key
    """
    return key in json


def is_enough_length(json, key, minimum, maximum):
    """Validator function, which checks if our string is longer than
       minimal value and shorted than maximum value.
       :params: json - JSON dictionary
                key - JSON key
                min - minimal length of string
                max - maximum length of string
       :return: True - if length of string is between min and max lengths
                False - if not
    """
    result = True
    if minimum:
        result = len(json[key]) >= minimum
    if result and maximum:
        result = len(json[key]) <= maximum
    return result


def is_email(json, key):
    """Validator function, which checks if string is similar to email.
       Uses regular expression pattern, declared above.
       :params: json - JSON dictionary
                key - JSON key
       :return: True - if string is similar to pattern
                False - if not
    """
    return EMAIL_PATTERN.match(json[key])


def is_not_empty(json, key):
    """Validator function which checks if value in json key is not empty.
       :params: json - JSON dictionary
                key - JSON key
       :return: True - if json value is not empty
                False - if it is empty
    """
    return json[key]


def is_string(json, key):
    """Validator function which checks if json value is string.
       :params: json - JSON dictionary
                key - JSON key
       :return: True - if value is string
                False - if it is not
    """
    return isinstance(json[key], basestring)


def is_in_enum(json, key, enum):
    """Validator function which checks if json value is in enum.
       :params: json - JSON dictionary
                key - JSON key
                enum - list of values
       :return: True - if value in enum
                False - if it is not
    """
    return json[key].lower() in enum
