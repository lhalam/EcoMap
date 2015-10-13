import ConfigParser
import time


configFilePath = '../../../etc/ecomap.conf'


# function which returns dictionary with parameters from
# ecomap.conf
def parseConfs():
    config = ConfigParser.ConfigParser()    # create config object
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


class Config(object):
    obj = None              # from start there is not object
    timeDelta = 60 * 15     # 60 secs * 15 minutes
    _deathTime = None       # lifetime of our object

    def __new__(cls):
        # check if there is object or lifetime is over
        if cls.obj is None or cls._deathTime < time.time():
            cls.obj = object.__new__(cls)       # create object
            cls._deathTime = time.time() + cls.timeDelta    # set lifetime
            cls.obj.conf = parseConfs()         # get dictionary with params
        return cls.obj

if __name__ == '__main__':
    x = Config()
