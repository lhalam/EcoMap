from ConfigParser import SafeConfigParser
from time import time
import logging
import unittest

password = ['password', 'pass', 'pswd']          # keys which must be string
logger = logging.getLogger('example')
logging.basicConfig(level=logging.DEBUG)
timeToUpdate = 15 * 60                           # 15 minutes


class Config(object):

    def __new__(cls, *args):
        if not hasattr(cls, '_instance'):        # if there is not instance
            cls._instance = object.__new__(cls)  # create it
        return cls._instance                     # else return it

    def __init__(self, path, logger, lifetime):
        self.config = {}                         # dictionary, contains configs
        self.timeCreated = time()                # generate time of creation
        self.timeUpdate = self.timeCreated + lifetime  # time of living
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
    class Test(unittest.TestCase):

        def test_sameinstances(self):
            self.a = Config('../../../etc/ecomap.conf', logger, timeToUpdate)
            self.b = Config('../../../etc/ecomap.conf', logger, timeToUpdate)
            self.assertEquals(self.a, self.b)

        def test_createtime(self):
            self.a = Config('../../../etc/ecomap.conf', logger, timeToUpdate)
            self.b = Config('../../../etc/ecomap.conf', logger, timeToUpdate)
            self.assertEquals(self.a.timeCreated, self.b.timeCreated)

        def test_config(self):
            self.a = Config('../../../etc/ecomap.conf', logger, timeToUpdate)
            self.b = Config('../../../etc/ecomap.conf', logger, timeToUpdate)
            self.assertEquals(self.a.get(), self.b.get())

        def test_updatetime(self):
            self.a = Config('../../../etc/ecomap.conf', logger, timeToUpdate)
            self.b = Config('../../../etc/ecomap.conf', logger, timeToUpdate)
            self.assertEquals(self.a.timeUpdate, self.b.timeUpdate)

    unittest.main()
