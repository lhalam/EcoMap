"""
Module which contains Config class. This class is singleton.
It exists to parse *.conf files and return dictionary,
which contains configuration from those files. Every 15 minutes
it returns new dictionary which contains updated configs.
"""
from ConfigParser import SafeConfigParser
from bin.utils import logger
import time
import os

REFRESH_TIME = 900                               # 15 minutes
PASSWORD = 'password'
CONFIG_PATH = os.environ['CONFROOT'] + '/ecomap.conf'


class Singleton(type):
    """
    Metaclass for make Config class singleton.
    """
    def __call__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            cls._instance = super(
                Singleton, cls).__call__(*args, **kwargs)
        return cls._instance


class Config(object):

    """
    Singleton class which returns object which have method
    to parse config file every 15 minutes.
    :param path: name of file
    """
    __metaclass__ = Singleton

    def __init__(self, path):
        self.config = {}                         # dictionary, contains configs
        self.update_time = 0                     # time of living
        self.path = path                         # path to file (temporary)
        self.logger = logger
        self.logger.info('Initialized instance at')

    def get_config(self):                        # method which checks if we
        """
        Checks if it is needed to reload configs.
        Before calling parsing functian checks if
        elapsed 15 minutes after last update.
        returns: dictionary
        """
        self.logger.info('Check if need to update')
        if self.update_time < time.time():       # need to update configs
            self.config = {}                     # nullify configs dictionary
            self.update_time = time.time() + REFRESH_TIME  # set time to update
            self._parse_confs()                  # parse config file
        return self.config

    def _parse_confs(self):
        """
        Parses config file and returns dictionary.
        """
        self.logger.info('Parsed ecomap.conf')
        config = SafeConfigParser()              # create config object
        config.readfp(open(self.path))           # read file
        sections = config.sections()             # get sections
        for section in sections:                 # for each section
            for (key, value) in config.items(section):   # for each key/value
                if value and key != PASSWORD:
                    try:
                        value = eval(value)
                    except NameError:
                        pass
                self.config[section + '.' + key] = value
