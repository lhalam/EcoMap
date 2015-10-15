import logging
from ConfigParser import SafeConfigParser
from time import time

logger = logging.getLogger('example')
logging.basicConfig(level=logging.DEBUG)


class Config(object):

    def __init__(self):
        self.lifeTime = time() + 900            # current time + 15 minutes
        logger.debug('Inited instance with lifeTime: {}'.
                     format(self.lifeTime))

    def __new__(cls):
        if not hasattr(cls, '_instance') or cls._instance.lifeTime < time():
            logger.debug('Create instance if it not exists or lifeTime ended')
            cls._instance = object.__new__(cls)
            cls._parseConfs(cls._instance)
        logger.debug('Returned instance: {}'.format(cls._instance))
        return cls._instance

    def _parseConfs(self):
        logger.debug('Parsed ecomap.conf')
        config = SafeConfigParser()             # create config object
        config.readfp(open(configFilePath))     # read file
        self.config = {}
        for section in config.sections():                # for each section
            for (key, value) in config.items(section):   # for each key/value
                if value and key != 'password':
                    try:
                        value = config.getboolean(section, key)
                    except ValueError:
                        try:
                            if '.' in value:
                                value = config.getfloat(section, key)
                            else:
                                value = config.getint(section, key)
                        except ValueError:
                            value = unicode(config.get(section, key).
                                            decode('utf-8'))
                self.config[section + '.' + key] = value

if __name__ == '__main__':
    configFilePath = '../../../etc/ecomap.conf'
    x = Config()
    print x.config
    print '=' * 80
    y = Config()
    print y.config
