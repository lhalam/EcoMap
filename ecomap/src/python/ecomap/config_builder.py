"""Configuration builder module.
Module creates config files from user input data.
"""
import os
import re
import sys
import hashlib
import logging

from optparse import OptionParser
from ConfigParser import SafeConfigParser

import MySQLdb

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


class BaseConfigBuilderError(Exception):
    """Class for config builder errors."""
    pass


class ConfigBuilderMysqlError(BaseConfigBuilderError):
    """Class for Mysql errors in config builder."""
    pass


def configvars_parser():
    """Parse config variables file.
    :return: dictionary,which contains dictionary of variable's value.
    """
    config = SafeConfigParser()
    config.readfp(open(os.path.join(ROOT_PATH, '_configvars.conf')))
    logging.info("Parse _configvars.conf")
    template_config = {section: {key: value or None
                                 for (key, value) in config.items(section)}
                       for section in config.sections()}
    logging.debug('Dictionary with list of variables was created.')
    return template_config


def check_regex(reg_exp, value):
    """Regular expression validation.
    :param reg_exp: regular expression.
    :param value: value to check.
    :return: True or False.
    """
    return bool(re.match(reg_exp, value))


def input_user_data(confvar_dict):
    """Function collects data from user input.
    :param confvar_dict: dictionary,which contains dictionary
    of variable's value.
    :return: dictionary where keys are variables for templates configs.
    """
    user_dict = {}
    logging.info('Function collects data from user input.')
    for key, value in confvar_dict.iteritems():
        while True:
            user_dict[key] = raw_input('[%s] %s [default:%s]: '
                                       % (key, value['help'],
                                          value['default']))or value['default']
            if user_dict[key]:
                type_value = CONFIG_TYPES[value['type']]
                if value.get('validate_re') \
                and not check_regex(value.get('validate_re'),
                                    user_dict[key]):
                    logging.warning('Invalid data! Use template: \
                                              example@mail.com.')
                    continue
                if not check_regex(type_value['regex'], user_dict[key]):
                    logging.warning('Invalid data! Wrong type!')
                    continue
                user_dict[key] = type_value['eval'] % user_dict[key]
                break
    logging.debug('Dictionary with user\'s input data was created.')
    return user_dict


def read_file(fpath, return_type='string', mode='r'):
    """Read data from a file.
    :param fpath: path to a file
    :param to_return: return value string or a list, [optional]
    :param mode: argument for open(), [optional]
    :return: string or list with content of read file.
    :exception: file doesn't exist, permission denied.
    """
    try:
        with open(fpath, mode) as temp:
            content = [x.strip() for x in temp.readlines()] \
             if return_type in ('list',) else temp.read()
    except (IOError, OSError) as error:
        logging.error(error)
        raise BaseConfigBuilderError(error)
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
    :param user_input: dictionary with user data.
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


def hash_pass(password, secret_key):
    """This function adds some salt(secret_key) to the password.
    :param password: user password.
    :param secret_key: hesh sum of secret key.
    :return: hash sum from password + salt.
    """
    salted_password = password + secret_key
    return hashlib.md5(salted_password).hexdigest()


def insert_user(first_name, last_name, email, password, host, db_user,
                db_pasword, db_name):
    """Function creates connection to db and adds new user into it.
    :param first_name: first name of user
    :param last_name: last name of user
    :param email: email of user
    :param password: hashed password of user
    :param host: database host name
    :param db_user: database user
    :param db_pasword: database password
    :param db_name: database name
    """
    try:
        mysql = MySQLdb.connect(host, db_user, db_pasword, db_name)
        cursor = mysql.cursor()
        query = """INSERT INTO `user` (`first_name`,
                                       `last_name`,
                                       `email`,
                                       `password`)
                   VALUES (%s, %s, %s, %s);
                """
        cursor.execute(query, (first_name, last_name, email, password))
        mysql.commit()
        logging.info('User %s %s was successfully added to database %s',
                     first_name, last_name, db_name)
        mysql.close()
    except MySQLdb.Error as mysql_error:
        logging.error(mysql_error)
        raise ConfigBuilderMysqlError(mysql_error)


def main():
    """Function runs config builder.
    And insert to database admin and unknown user.
    """
    parser = OptionParser('usage: %prog [options]')
    parser.add_option('-v', '--verbosity', action='store', dest='verbosity',
                      default='1', choices=['1', '2', '3'],
                      help='Verbosity level [1-3]. \
                      1(default) - level INFO, 3 - level DEBUG.')
    (options, args) = parser.parse_args()
    if options.verbosity == '1':
        log_level = logging.INFO
    elif options.verbosity >= '2':
        log_level = logging.DEBUG
    logging.basicConfig(format=u'[%(asctime)s] %(levelname)-8s %(message)s',
                        level=log_level)
    user_input = input_user_data(configvars_parser())
    create_config_files(user_input)
    insert_user('admin', 'admin',
                user_input['ecomap_admin_user_email'],
                hash_pass(user_input['ecomap_admin_user_password'],
                          user_input['ecomap_secret_key']),
                user_input['rw_db_host'], user_input['rw_db_user'],
                user_input['rw_db_password'], user_input['db_name'])
    insert_user(user_input['ecomap_unknown_first_name'],
                user_input['ecomap_unknown_last_name'],
                user_input['ecomap_unknown_email'],
                hash_pass(user_input['ecomap_admin_user_password'],
                          user_input['ecomap_secret_key']),
                user_input['rw_db_host'], user_input['rw_db_user'],
                user_input['rw_db_password'], user_input['db_name'])


if __name__ == '__main__':
    sys.exit(main())
