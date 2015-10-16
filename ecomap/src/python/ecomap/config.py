import logging
from ConfigParser import SafeConfigParser
from time import time
import threading
import md5

logger = logging.getLogger('example')
logging.basicConfig(level=logging.DEBUG)
timeToUpdate=12

class Config(object):
    def __new__(cls,*args):
        if not hasattr(cls, '_instance'):
            cls._instance = object.__new__(cls)
        return cls._instance

    def __init__(self,path,logger):
        self.timecreated = time()          # current time + 15 minutes
        self.path=path
        self.logger=logger
        self._parseConfs()
        self.logger.debug('Inited instance with time created: {}'.
                     format(self.timecreated))

    def get(self):
        if self.timeUpdate+timeToUpdate>time():
            self.LastHashsum=hash(frozenset(self.config.items()))
            self._parseConfs()
            self.currentHashSum=hash(frozenset(self.config.items()))
            if self.LastHashsum !=self.currentHashSum:
                print "dieferent hashSum"
                self.timeUpdate=time()
        return self.config        


    def _parseConfs(self):
        self.logger.debug('Parsed ecomap.conf')
        config = SafeConfigParser()             # create config object
        config.readfp(open(self.path))     # read file
        self.config = {}
        self.timeUpdate=time()
        for section in config.sections():                # for each section
            for (key, value) in config.items(section):   # for each key/value
                if value and key != 'password':
                    try:
                        value = config.getboolean(section, key)
                    except ValueError:
                        try:
                            if '.' in value :
                                value = config.getfloat(section, key)
                            else:
                                value = config.getint(section, key)
                        except ValueError:
                            value = unicode(config.get(section, key).
                                            decode('utf-8'))
                self.config[section + '.' + key] = value
               

if __name__ == '__main__':
    
    x = Config('../../../etc/ecomap.conf',logger)
    
    getTimer =threading.Timer(11.0,x.get)
    getTimer.start()
    getTimer2 =threading.Timer(21.0,x.get)
    getTimer2.start()

    print x.config
    #print '=' * 80
    #y = Config()
    #print y.config
