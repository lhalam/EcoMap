"""
Module which contains Config class. This class is singleton.
It exists to parse *.conf files and return dictionary,
which contains configuration from those files. Every 15 minutes
it returns new dictionary which contains updated configs.
"""
import os
import time
from ConfigParser import SafeConfigParser
from ecomap.utils import get_logger
from ecomap.utils import Singleton


REFRESH_TIME = 900
PASSWORD = 'password'
CONFIG_PATH = os.path.join(os.environ['CONFROOT'], 'ecomap.conf')


class Config(object):
    """
    Singleton class to get configs
    """
    __metaclass__ = Singleton

    def __init__(self):
        self.config = {}
        self.update_time = 0
        self.path = CONFIG_PATH
        self.log = get_logger('Config parser')
        self.log.info('Create instance of Config parser')

    def get_config(self):
        """
        Call parse method if need.
        Returns:
            dictionary, containing configs
        """
        if self.update_time + REFRESH_TIME < time.time():
            self.log.info('Refresh configs')
            self.update_time = time.time()
            self._parse_confs()
        self.log.info('Return configs')
        return self.config

    def _parse_confs(self):
        """
        Parses config file.
        """
        self.log.info('Parsed ecomap.conf')
        config = SafeConfigParser()
        config.readfp(open(self.path))
        sections = config.sections()
        temp_config = {}
        for section in sections:
            for (key, value) in config.items(section):
                if value and key != PASSWORD:
                    try:
                        value = eval(value)
                    except NameError:
                        pass
                temp_config[section + '.' + key] = value
        self.config = temp_config
