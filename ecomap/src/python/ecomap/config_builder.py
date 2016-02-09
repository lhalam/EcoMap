"""Configuration builder module.
Module creates config files from user input data.
"""
import os
import re
import sys
import logging

from optparse import OptionParser
from ConfigParser import SafeConfigParser

from ecomap.db.util import insert_user

ROOT_PATH = os.environ['CONFROOT']

CONFIG_TYPES = {'str': {'regex': '.*',
                        'eval': '%s'},
                'bool': {'regex': '^(?:False|True)$',
                         'eval': 'eval(%s)'},
                'int': {'regex': r'^-?\d+$',
                        'eval': 'eval(%s)'},
                'float': {'regex': r'^-?\d*\.?\d+$',
                          'eval': 'eval(%s)'},
                'list': {'regex': r'^\[.*\]$',
                         'eval': '%s'},
                'dict': {'regex': r'^\{.*\}$',
                         'eval': '%s'}
                }


class BaseConfigBuilderException(Exception):

    """Class for config builder exceptions."""

    pass


def configvars_parser():
    """Parse config variables file.
    Returns:
        dictionary,which contains list of variable's value.
    """
    config = SafeConfigParser()
    config.readfp(open(os.path.join(ROOT_PATH, '_configvars.conf')))
    sections = config.sections()
    logging.info("Parse _configvars.conf")
    template_config = {}
    # for section in sections:
    #     template_config[section] = dict(tuple(config.items(section)))
    # logging.debug('Dictionary with list of variables was created.')
    # return template_config
    for section in sections:
        template_config[section] = {}
        for (key, value) in config.items(section):
            template_config[section][key] = value or None
    logging.debug('Dictionary with list of variables was created')
    return template_config


def check_regex(reg_exp, value):
    """Regular expression validation.
    Input: value to check, regular expression.
    Rerurns:
        True or False.
    """
    return bool(re.match(reg_exp, value))


def input_user_data(confvar_dict):
    """Function collects data from user input.
    Input: data - dictionary,which contains list of variable's value.
    Returns:
            dictionary where keys are variables for templates configs.
    """
    user_dict = {}
    logging.info('Function collects data from user input.')
    for key, value in confvar_dict.iteritems():
        while True:
            user_dict[key] = raw_input('[%s] %s [default:%s]: '
                                        % (key, value['help'],
                                        value['default'])) or value['default']
            if user_dict[key]:
                type_value = CONFIG_TYPES[value['type']]
                if 'validate_re' in confvar_dict[key]:
                    if not check_regex(value['validate_re'], user_dict[key]):
                        logging.warning('Invalid data! example@mail.com.')
                        continue
                elif not check_regex(type_value['regex'], user_dict[key]):
                    logging.warning('Invalid data!')
                    continue
                user_dict[key] = type_value['eval'] % user_dict[key]
                break
    logging.debug('Dictionary with user\'s input data was created.')
    return user_dict


def read_file(fpath, return_type='string', mode='r'):
    """Function for reading a file. If file exists, it's content is returned.
    Else, an error is thrown and execution is stopped.
    :param fpath: path to a file
    :param to_return: return value string or a list, [optional]
    :param mode: argument for open(), [optional]
    :return: string or list with content of read file.
    """
    with open(fpath, mode) as temp:
        if return_type == 'list':
            content = [x.strip() for x in temp.readlines()]
        else:
            content = temp.read()
    return content


def write_file(fpath, content, mode='w'):
    """Function for writing to a file.If file can't be written, error is thrown.
    Else, file is created with user data.
    :param fpath: path to a file
    :param content: data to put in the file
    :param mode: argument for open(), [optional].
    """
    with open(fpath, mode) as to_write:
        to_write.writelines(content)


def create_config_files(user_input):
    """Function creates 4 configurations files.
    param user_input: dictionary with user data.
    """
    file_conf = read_file(os.path.join(ROOT_PATH, '_configfiles.conf'), 'list')
    logging.info('Creating config files.')
    for line in file_conf:
        template_name = os.path.join(ROOT_PATH,
                                     'templates/' + line.split(',')[0])
        content = read_file(template_name)
        for key, value in user_input.items():
            content = content.replace('$%s' % key, value)
        new_file_name = os.path.join(ROOT_PATH,
                                     line.split(',')[1])
        write_file(new_file_name, content)
    logging.debug('Config files are created successfully.')


def main():
    """ Function runs config builder."""
    parser = OptionParser('usage: %prog [options]')
    parser.add_option('-v', '--verbosity', action='store', dest='verbosity',
                      type=int, default=1, help='Verbosity level [1-3]. \
                      1(default) - level INFO, 3  - level DEBUG.')
    (options, args) = parser.parse_args()
    list_level = range(1, 4)
    if options.verbosity == 1:
        log_level = logging.INFO
    elif options.verbosity >= 2 and options.verbosity in list_level:
        log_level = logging.DEBUG
    logging.basicConfig(format=u'[%(asctime)s] %(levelname)-8s %(message)s',
                        level=log_level)
    user_input = input_user_data(configvars_parser())
    create_config_files(user_input)
    insert_user('admin', 'admin',
                user_input['ecomap_admin_user_email'],
                user_input['ecomap_admin_user_password'])
    insert_user(user_input['ecomap_unknown_first_name'],
                user_input['ecomap_unknown_last_name'],
                user_input['ecomap_unknown_email'],
                user_input['ecomap_admin_user_password'])

if __name__ == '__main__':
    sys.exit(main())
