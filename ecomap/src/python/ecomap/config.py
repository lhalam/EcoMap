import ConfigParser
import time


configFilePath = '../../../etc/ecomap.conf'


def parseConfs():
    config = ConfigParser.RawConfigParser()
    config.readfp(open(configFilePath))
    return {key: value for (key, value) in config.items('ecomap')}


class Config(object):
    obj = None
    timeDelta = 20  # 60 secs * 15 minutes
    _deathTime = None

    def __new__(cls):
        if cls.obj is None or cls._deathTime < time.time():
            cls.obj = object.__new__(cls)
            cls._deathTime = time.time() + cls.timeDelta
            cls.obj.conf = parseConfs()
        return cls.obj

if __name__ == '__main__':
    x = Config()
