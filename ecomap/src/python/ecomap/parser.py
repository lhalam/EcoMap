# coding = utf-8
import logging
import os
import warnings
import ConfigParser
from ConfigParser import SafeConfigParser
import time

#probably we could convert this to ENVIROMENT PATH using module package system?? <from ecomap import *?>
configPath = '../../../etc/ecomap.conf'

logger = logging.getLogger('file_name') #file name/path to log
# more info in log lines( we can leave here only necessary options)
logging.basicConfig(format=u'%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s',
                    level=logging.DEBUG)


class SingletonDecorator:
    def __init__(self, cls):
        self.cls = cls
        self.instance = None
        print 'init'

    def __call__(self, *args, **kwds):
        if self.instance is None:
            self.instance = self.cls(*args, **kwds)
            self.delta = time.time()
            print self.delta
            logger.debug('Returned instance: {}'.format(self.instance))
            print 'called'

            """
            big problem starts below:
            i wanted to incapsulate Singleton creating and updating logic into the class decorator.
            i thought that our class could recreate new instance each 15 min
            and we need to set this option in decorator's constructor.
            or our class could __call__() itself each interval of time, sending its activity to log.

            anyway it doesn't work with this conditions
            """

            # #bad code:
            # return self.instance
        # else:
        #     while time.time() - self.delta > 0.001:
        #         print self.delta
        #         time.sleep(1)
        #
        #         logger.debug('Returned instance: {}'.format(self.instance))
        #         print 'called'
        return self.instance


# transforming our Parser class to a Singleton.
@SingletonDecorator
class Parser(SafeConfigParser):


    """
    i don't think that it is a good idea to keep whole parsing logic and variables in the one metod of a class.
    but i can't refactor this to any smart version
    """
    def parse(self):
        parser = Parser()

        # !properly working parsing function( with safe types converting)
        parser.read(configPath)
        dct = {}
        for section_name in parser.sections():
            for name, value in parser.items(section_name):
                if value:
                    try:
                        value = parser.getboolean(section_name, name)
                    except ValueError:
                        try:
                            if '.' in value:
                                value = parser.getfloat(section_name, name)
                            else:
                                value = parser.getint(section_name, name)
                        except ValueError:
                            value = unicode(parser.get(section_name, name).decode('utf-8'))
                dct[section_name + '.' + name] = value
        logger.debug('new conf read {}'.format(dct))
        return dct

p = Parser()
s = Parser()
print p.parse()
print s.parse()
print p == s


