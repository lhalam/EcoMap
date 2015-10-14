import ConfigParser
import time


configFilePath = '../../../etc/ecomap.conf'


class Config(object):
    obj = None              # from start there is not object
    timeDelta = 15 * 60     # 60 secs * 15 minutes
    _deathTime = None       # lifetime of our object

    def __new__(cls):
        # check if there is object or lifetime is over
        if cls.obj is None or cls._deathTime < time.time():
            cls.obj = object.__new__(cls)       # create object
            cls._deathTime = time.time() + cls.timeDelta    # set lifetime
            cls.obj.conf = cls.__parseConfs()     # get dictionary with params
        return cls.obj

    @staticmethod
    def __parseConfs():
        config = ConfigParser.SafeConfigParser()    # create config object
        config.readfp(open(configFilePath))     # read file
        sections = config.sections()            # get all sections
        result = {}
        for section in sections:                # for each section
            for (key, value) in config.items(section):  # for each key/value
                if key != 'password':           # if key == password skip
                    try:
                        value = int(value)      # try to convert value into int
                    except ValueError:
                        pass
                result[section + '.' + key] = value
        return result


if __name__ == '__main__':
    x = Config()
