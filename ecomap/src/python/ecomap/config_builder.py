"""
Configuration builder module.
Module creates config files from user input data.
"""
import os
import re
import sys

from ConfigParser import SafeConfigParser

CONFIG_VARS = os.path.join(os.environ['CONFROOT'], '_configvars.conf')
CONFIG_FILES = os.path.join(os.environ['CONFROOT'], '_configfiles.conf')

CONFIG_TYPES = {'str' :   {'regex' : '.*',
                           'eval' : '%s'
                           },
                'bool' :  {'regex' : '^(?:False|True)$',
                           'eval' : 'eval("%s")'
                           },
                'int' :   {'regex' : r'^-?\d+$',
                           'eval' : 'eval("%s")'
                           },
                'float' : {'regex' : r'^-?\d*\.?\d+$',
                            'eval' : 'eval("%s")'
                           },
                'list' :  {'regex' : r'^\[.*\]$',
                           'eval' : '%s'
                           },
                'dict' :  {'regex' : r'^\{.*\}$',
                           'eval' : '%s'
                           },
                }


def configvars_parser():
    """
    Parse config variables file.
    Returns:
        dictionary,which contains list of variable's value.
    """
    config = SafeConfigParser()
    config.readfp(open(CONFIG_VARS))
    sections = config.sections()
    template_config = {}
    for section in sections:
        template_config[section] = []
        for (key, value) in config.items(section):
            template_config[section].append(value or None)
    return template_config


def check_regex(reg_exp, value):
    """
    Regular expression validation.
    Input: value to check, regular expression.
    Rerurns:
        True or False.
    """
    return bool(re.match(reg_exp, value))



def input_user_data(confvar_dict):
    """
    Function collects data from user input.
    Input: data - dictionary,which contains list of variable's value.
    Returns:
            dictionary where keys are variables for templates configs.
    """
    user_dict = {}
    for key, value in confvar_dict.iteritems():
        while True:
            user_dict[key] = raw_input('[%s] %s [default:%s]: '
                                       % (key, value[0], value[1])) or value[1]
            if user_dict[key]:
                type_value = CONFIG_TYPES[value[2]]
                if not check_regex(type_value['regex'], user_dict[key]):
                    print 'Invalid data! Should be type %s.' % value[2]
                #checking if email is valid. 
                elif len(value)>3:
                    if not check_regex(value[3], user_dict[key]):
                        print 'Invalid data! Example: mail@mail.com.'
                    else:
                        break
                else:
                    user_dict[key] = type_value['eval'] % user_dict[key]
                    break            
    return user_dict


def create_config_files(user_input):
    """
    Function creates 4 configurations files.
    Input: data - dictionary
    """
    with open(CONFIG_FILES, 'r+') as file_conf:
        for line in file_conf:
            template_name = line.split(', ')[0]
            file_name = line.split(', ')[-1]
            with open(template_name, 'r+') as temp:
                content = temp.readlines()
                for row in content:
                    for key in user_input:
                        to_replace = ('$%s' % key)
                        if to_replace in row:
                            place = content.index(row)
                            content[place] = \
                                row.replace(to_replace, user_input[key])
                            row = content[place]
            new_file_name = os.path.join(os.environ['CONFROOT'], file_name)
            with open(new_file_name, 'w+') as to_write:
                to_write.writelines(content)


def main():
    """
    Function runs config builder.
    """
    input_user_data(configvars_parser())

if __name__ == '__main__':
    sys.exit(main())
