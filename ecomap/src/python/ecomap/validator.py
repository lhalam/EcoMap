import imghdr
import re

email_pattern = re.compile(r'^[a-zA-Z0-9._]+@[a-zA-Z0-9._]+\.[a-zA-Z]{2,}$')

message = {'validate_key': 'no {} key in JSON.',
           'validate_length': '{} value it too long or short.',
           'validate_empty': '{} field is empty.',
           'validate_string': '{} value is not string.',
           'validate_email': '{} value does not look like email.'}


def main_validator(to_validate):
    """General validator function. Import this to validate.
       :params: to_validate - list of lists with values and functions to
                validate validate your value
       :return: error message if validation was bad
    """
    for args in to_validate:
        valid = validator(*args)
        if valid:
            return valid
            break


def validator(json, key, min_len, max_len, *args):
    """Validator function, which launches other functions.
       :params: json - JSON dictionary
                key - key we want to check
                min_len - minimal length of string
                max_len - maximum length of string
                *args - list of methods we want to use to check our value
       :return: message - if validation was bad
    """
    for method in args:
        if not method(json, key, min_len, max_len):
            return message[method.func_name].format(key)
            break


def validate_key(*args):
    """Validator function, which checks if there is all needed keys json
       object.
       :params: args[0] - json dictionary we want to check
                args[1] - key, we expect to get from json
       :return: True - if all is ok
                False - if there is no expected key
    """
    return args[1] in args[0].keys()


def validate_length(*args):
    """Validator function, which checks if our string is longer than
       minimal value and shorted than maximum value.
       :params: args[0] - JSON dictionary
                args[1] - JSON key
                args[0][args[1]] - string, we want to check
                args[2] - minimal length of string
                args[3] - maximum length of string
       :return: True - if length of string is between min and max lengths
                False - if not
    """
    return len(args[0][args[1]]) in range(args[2], args[3])


def validate_email(*args):
    """Validator function, which checks if string is similar to email.
       Uses regular expression pattern, declared above.
       :params: args[0] - JSON dictionary
                args[1] - JSON key
                args[0][args[1]] - string, we want to check if it is email
       :return: True - if string is similar to pattern
                False - if not
    """
    return True if email_pattern.match(args[0][args[1]]) else False


def validate_empty(*args):
    """Validator function which checks if value in json key is not empty.
       :params: args[0] - JSON dictionary
                args[1] - JSON key
                args[0][args[1]] - value we want to check if it is not empty
       :return: True - if json value is not empty
                False - if it is empty
    """
    return True if args[0][args[1]] else False


def validate_string(*args):
    """Validator function which checks if json value is string.
       :params: args[0] - JSON dictionary
                args[1] - JSON key
                args[0][args[1]] - value we want to check
       :return: True - if value is string
                False - if it is not
    """
    return True if isinstance(args[0][args[1]], basestring) else False


def validate_image_file(file):
    return True if str(imghdr.what(file)) == 'png' else False

