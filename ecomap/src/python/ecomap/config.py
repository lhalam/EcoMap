from ConfigParser import SafeConfigParser
from time import time
import logging
from utils import logger

password = ['password', 'pass', 'pswd']     # keys which must be string

  # 15 minutes


class Config(object):

    def __new__(cls, *args):
        if not hasattr(cls, '_instance'):        # if there is not instance
            cls._instance = object.__new__(cls)  # create it
        return cls._instance                     # else return it

    def __init__(self, path, logger):
        self.config = {}                         # dictionary, contains configs
        self.timeUpdate = None                   # time to update dictionary
        self.timeCreated = time()                # create time of instance
        self.path = path                         # path to file (temporary)
        self.logger = logger
        self._parseConfs()                       # get configs at start
        self.logger.debug('Initialized instance with time created: {}'.
                          format(self.timeCreated))

    def get(self):                               # method which checks if we
        if self.timeUpdate < time():             # need to update configs
            self.config = {}                     # nullify configs dictionary
            self.timeUpdate = time() + timeToUpdate  # set time to update
            self._parseConfs()                   # parse config file
        return self.config

    def _parseConfs(self):
        self.logger.debug('Parsed ecomap.conf at {}'.format(time()))
        config = SafeConfigParser()             # create config object
        config.readfp(open(self.path))          # read file
        sections = config.sections()            # get sections
        for section in sections:                # for each section
            for (key, value) in config.items(section):   # for each key/value
                if value and key.lower() not in password:
                    try:
                        value = eval(value)
                    except NameError:
                        pass
                self.config[section + '.' + key] = value


if __name__ == '__main__':

    x = Config('../../../etc/ecomap.conf', logger)
    y = Config('../../../etc/ecomap.conf', logger)

    # getTimer = threading.Timer(11.0, x.get)
    # getTimer.start()
    # getTimer2 = threading.Timer(21.0, x.get)
    # getTimer2.start()

    # print x.config
    # print '=' * 80
    # y = Config()
    # print y.config
