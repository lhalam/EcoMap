"""Module which contains Config class. This class is singleton.
It exists to parse *.conf files which do not start with "_" symbol
and return dictionary, which contains configuration from those files.
Every 15 minutes it returns new dictionary which contains updated configs.
"""
import os
import time
import logging

from ConfigParser import SafeConfigParser

from ecomap.utils import Singleton

REFRESH_TIME = 900
CONFIG_PATH = os.environ['CONFROOT']


class Config(object):

    """Singleton class to get configs."""
    
    __metaclass__ = Singleton

    def __init__(self):
        self.config = {}
        self.update_time = 0
        self.path = CONFIG_PATH
        self.log = logging.getLogger('config_parser')
        self.log.info('Create instance of Config parser.')

    def get_config(self):
        """Call parse method if it needed.
        :return: dictionary, containing configs.
        """
        if self.update_time + REFRESH_TIME < time.time():
            self.log.info('Refresh configs')
            self.update_time = time.time()
            self._parse_confs()
        return self.config

    def _parse_confs(self):
        """Parses config file."""
        self.log.info('Parse ecomap.conf.')
        config = SafeConfigParser()
        for fname in os.listdir(self.path):
            if not (fname.startswith('_')) and fname.endswith(".conf"):
                with open(os.path.join(self.path, fname)) as config_file:
                    config.readfp(config_file)
        sections = config.sections()
        temp_config = {}
        for section in sections:
            for (key, value) in config.items(section):
                temp_config['%s.%s' %(section, key)] = self._value_eval(value)
        self.config = temp_config

    def _value_eval(self, value):
        """Get value from config file and
        :return: value in valid type.
        """
        if value.startswith('eval(') and value.endswith(')'):
            value = eval(value[5:-1])
        elif ((value.startswith('[') and value.endswith(']')) or
             (value.startswith('{') and value.endswith('}'))):
            value = eval(value)
        return value
