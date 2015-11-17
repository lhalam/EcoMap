import json
import logging
import logging.config
import os
import re

CONF_PATH = os.path.join(os.environ['CONFROOT'], 'log.conf')


def get_logger():
    """function for configuring default logger object
    from standard logging library
        Returns:
            configured logger object.
        Usage:
            import this method to your
            module and call it.
            then define a new logger object as usual
    """
    return logging.config.fileConfig(CONF_PATH)


class Singleton(type):
    """
    using a Singleton pattern to work with only one possible instance of Pool
    """
    def __call__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            cls._instance = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instance


class Validators(object):
    """
    Class contains all needed optional methods for validation
    request JSON data on backend server
    using REST and flask app.
    """
    def __init__(self):
        pass

    @staticmethod
    def required(val):
        """
        Validation for check value in JSON key is not empty.
        param val: JSON value to validate.
        return: True or False
        """
        return True if val else False

    @staticmethod
    def is_string(val):
        """
        Validator checks a type of json data send in request.
        :param val: json data.
        :return: True if type is str or unicode, False in else case.
        """
        return True if isinstance(val, basestring) else False

    @staticmethod
    def max_l(l):
        """
        Function wrapper, using closure to transfer user's validation argument.
        if no argument is given - run with default logic.
        :param l: max length of json data value given by user,
            if param not given - default value is 255.
        :return: inner function which does a work with user argument.
        """
        if isinstance(l, basestring):
            return True if len(l) <= 255 else False

        def max_length(val, length=l):
            """
            Inner function checks if the length of json data is less or
            equal to max_length user validation argument.
            :param val: JSON data
            :param length: max length of json data value defined by user.
            :return: True or False
            """
            return True if len(val) <= length else False
        return max_length

    @staticmethod
    def min_l(l):
        """
        Function wrapper, using closure to transfer user's validation argument.
        if no argument is given - run with default logic.
        :param l: min length of json data value given by user,
            if param not given - default value is 0.
        :return: inner function which does a work with user argument.
        """

        if isinstance(l, basestring):
            return True if len(l) > 0 else False

        def min_length(val, length=l):
            """
            Inner function checks if the length of json data is more or
            equal to min_length user validation argument.
            :param val: JSON data
            :param length: min length of json data value defined by user.
            :return: True or False
            """

            return True if len(val) >= length else False
        return min_length

    @staticmethod
    def no_spaces(val):
        """
        Validator checks if json contains no whitespace character.
        :param val: json data
        :return: true or false
        """
        return True if ' ' not in val else False

    @staticmethod
    def match(pattern):
        """
        Function wrapper, using closure to transfer user's validation argument.
        :param pattern: required. a custom users regexp pattern.
        :return: inner function which does a work with user argument.
        """
        def check_pattern(val, custom_pat=pattern):
            """
            Inner function checks if json value matches a
             custom regexp pattern.
            :param val: json data value
            :param custom_pat: reg_exp pattern given by wrapper function
            :return:True or False
            """
            return True if re.match(custom_pat, val) else False
        return check_pattern

    @staticmethod
    def enum(values):
        """
        Function wrapper, using closure to transfer user's validation argument.
        :param enums: required. list of optional values.
        :return: inner function which does a work with user argument.
        """
        def _enum(val, enums=values):
            """
            Inner function checks if json value matches allowed value.
            :param val: json input data
            :param enums: a list of values given by wrapper function
            :return:True or False
            """
            return True if val in enums else False
        return _enum

    @staticmethod
    def email_pattern(val):
        """
        Checks if json value matches a pre-defined email regexp pattern.

        :param val: json value
        :return: True or False
        """
        mail_pat = r"^[a-zA-Z0-9._]+@[a-zA-Z0-9._]+\.[a-zA-Z]{2,}$"
        return True if re.match(mail_pat, val) else False


v = Validators()


def validate(json_data, validators):
    """
    Function provides json data validation

    :param json_data: JSON object given in request
    :param validators: list of dicts with keys to check data and
                        validator functions of class Validators
    :return:
    """
    msg = {'errors': []}
    if len(validators) > 1:
        for _val in validators:
            if not _val.keys()[0] in [key for key in json_data.keys()]:
                msg['errors'].append({'key_error': 'no key {"%s":} in request '
                                      '<_debug_mode' % _val.keys()[0]})
                break
        else:
            for validator in validators:
                for key, value in validator.iteritems():
                    for func in value:
                        if not func(json_data[key]):
                            msg['errors'].append({'validation_error':
                                                  '%s error in "%s" value'
                                                  % (func.__name__, key)})
        if not msg['errors']:
            msg['status'] = 'ok'
    else:
        for _val in validators:
            if _val not in [key for key in json_data.keys()]:
                msg['errors'].append({'key_error': 'no key {"%s":} in request '
                                                   '<_debug_mode' % _val})
                break
        else:
            for key, value in validators.iteritems():
                for func in value:
                    if not func(json_data[key]):
                        msg['errors'].append({'validation_error':
                                              '%s error in "%s" value'
                                              % (func.__name__, key)})
        if not msg['errors']:
            msg['status'] = 'ok'
    return msg
