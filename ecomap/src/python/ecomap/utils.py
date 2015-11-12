import logging
import logging.config
import os


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



MAX_LENGTH = 255


class Validators(object):
    def __init__(self):
        pass

    @staticmethod
    def required(val):
        return True if val else False

    @staticmethod
    def is_string(val):
        return True if isinstance(val, basestring) else False

    @staticmethod
    def no_spaces(val):
        # message = 'no spaces'

        return True if ' ' not in val else False

    # @length_dec(2)
    @staticmethod
    def max_lenth(val, length=MAX_LENGTH):
        return True if len(val) < length else False

    @staticmethod
    def email_pattern(val):
        return True if re.match(r"^[a-zA-Z0-9._]+\@[a-zA-Z0-9._]+"
                                r"\.[a-zA-Z]{3,}$", val) else False

# v = Validators()
# JSON_OBJ = {u'password': 'dddd', u'email': u'email@email.riu', u'age':34}
# KEYS = ('password', 'email', 'age')
# VALIDATORS = ([v.required, v.is_string, v.no_spaces], [v.required, v.no_spaces, v.max_lenth, v.email_pattern])


def validate(instance, keys, validators_list):
    errors = {}
    for k, v in instance.iteritems():
        if k not in keys:
            errors['key_error'] = 'error in key {%s}[debug_mode]' % k  # value k left for debug
            break
    else:
        key_validators = zip(keys, validators_list)
        for zipd in key_validators:
            for func in zipd[1]:
                if not func(instance[zipd[0]]):
                    errors['vaditation error'] = '%s error in value %s' % (func, zipd[0])

    return True if not errors else errors

# print validate(JSON_OBJ, KEYS, VALIDATORS)
