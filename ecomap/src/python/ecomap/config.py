from ConfigParser import SafeConfigParser
import logging
import time
import unittest

logging.basicConfig(level=logging.DEBUG)
REFRESH_TIME = 900                               # 15 minutes
PASSWORD = 'password'


class Singleton(type):

    def __call__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            cls._instance = super(
                Singleton, cls).__call__(*args, **kwargs)
        return cls._instance


class Config(object):
    __metaclass__ = Singleton

    def __init__(self, path):
        self.config = {}                         # dictionary, contains configs
        self.update_time = 0                     # time of living
        self.path = path                         # path to file (temporary)
        self.logger = logging.getLogger('exapmle')
        self.logger.debug('Initialized instance at: %s', time.time())

    def get_config(self):                        # method which checks if we
        self.logger.debug('Check if need to update at %s', time.time())
        if self.update_time < time.time():       # need to update configs
            self.config = {}                     # nullify configs dictionary
            self.update_time = time.time() + REFRESH_TIME  # set time to update
            self._parse_confs()                  # parse config file
        return self.config

    def _parse_confs(self):
        self.logger.debug('Parsed ecomap.conf at %s', (time.time()))
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


if __name__ == '__main__':
    class Test(unittest.TestCase):

        def test_sameinstances(self):
            self.a = Config('../../../etc/ecomap.conf')
            self.b = Config('../../../etc/ecomap.conf')
            self.assertEquals(self.a, self.b)

        def test_config(self):
            self.a = Config('../../../etc/ecomap.conf')
            self.b = Config('../../../etc/ecomap.conf')
            self.assertEquals(self.a.get_config(), self.b.get_config())

        def test_updatetime(self):
            self.a = Config('../../../etc/ecomap.conf')
            self.b = Config('../../../etc/ecomap.conf')
            self.assertEquals(self.a.update_time, self.b.update_time)

    unittest.main()
