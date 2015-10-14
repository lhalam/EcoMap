import logging
from ConfigParser import SafeConfigParser
from time import time

logger = logging.getLogger('example')
logging.basicConfig(level=logging.DEBUG)


class Config(object):

    def __init__(self):
        self.lifeTime = time() + 900            # current time + 15 minutes
        logger.debug('Created instance with lifeTime: {}'.
                     format(self.lifeTime))

    def __new__(cls):
        if not hasattr(cls, '_instance') or cls._instance.lifeTime < time():
            logger.debug('Create instance if it not exists or lifeTime expired')
            cls._instance = object.__new__(cls)
            cls._parseConfs(cls._instance)
        logger.debug('Returned instance: {}'.format(cls._instance))
        return cls._instance

    def _parseConfs(self):
        logger.debug('Parsed ecomap.conf')
        config = SafeConfigParser()             # create config object
        config.readfp(open(configFilePath))     # read file
        sections = config.sections()            # get all sections
        self.config = {}
        for section in sections:                # for each section
            for (key, value) in config.items(section):  # for each key/value
                if key != 'password':           # if key == password skip
                    try:
                        try:
                            value = int(value)  # try to convert value into int
                        except ValueError:
                            value = float(value)
                    except ValueError:
                        pass
                self.config[section + '.' + key] = value

if __name__ == '__main__':
    configFilePath = '../../../etc/ecomap.conf'
    x = Config()
