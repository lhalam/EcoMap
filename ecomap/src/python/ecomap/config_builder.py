import os
import re

from ConfigParser import SafeConfigParser

CONFIG_PATH = os.path.join(os.environ['CONFROOT'], '_configvars.conf')

def config_variables_parser():
    """
    Parse config variables file.
    Returns:
        dictionary,which contains list of variable's value.
    """
    config = SafeConfigParser()
    config.readfp(open(CONFIG_PATH))
    sections = config.sections()
    template_config = {}
    for section in sections:
        template_config[section] = []
        for (key, value) in config.items(section):
            if not value:
                value = None
            template_config[section].append(value)
    return template_config

def validate_reg_expression(reg_exp, value):
    """
    Regular expression validation.
    Rerurns:
        True or False.
    """
    return bool(re.match(reg_exp, value))

def validate_type(value, value_type):
    # if value_type is 'int':
    #     value=int(value)
    pass

def input_variables(confvar_dict):
    """
    Function accepts dictionary with list of variables's values.
    Returns:
            dictionary where keys are variables for templates configs.
    """
    user_dict = {}
    for key, value in confvar_dict.iteritems():
        while True:
            user_dict[key] = raw_input('[%s] %s [default:%s]: ' % (key, value[0], value[1])) \
            or value[1]
            if user_dict[key]:
                if not validate_reg_expression(value[3], user_dict[key]):
                    print 'Must be  %s' % value[3]
                    user_dict[key] = None
                elif value[2] == 'int':
                    user_dict[key]=int(user_dict[key])
                    break
                else: 
                    break
    return user_dict

input_variables(config_variables_parser())