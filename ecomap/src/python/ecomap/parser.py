# coding = utf-8
import logging
import os
import warnings
import ConfigParser
from ConfigParser import SafeConfigParser
import time
#
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
        print '__init__ decorator'

    def __call__(self, *args, **kwds):
        if self.instance is None:
            self.instance = self.cls(*args, **kwds)
            print 'called from decorator'
            logger.debug('Returned instance: {}'.format(self.instance))

            """
            big problem starts below:
            i wanted to incapsulate Singleton creating and updating logic into the class decorator.
            i thought that our class could recreate new instance each 15 min
            and we need to set this option in decorator's constructor.
            or our class could __call__() itself each interval of time, sending its activity to log.

            anyway it doesn't work with this conditions
            """
            # #bad code:
        return self.instance
        # else:
        #     t2 = time.time() - self.delta
        #     while t2 > 0:
        #         print t2
        #         print self.delta
        #         time.sleep(1)
        #
        #         logger.debug('Returned instance: {}'.format(self.instance.parse()))
        #         print 'called'
        # return self.instance


# transforming our Parser class to a Singleton.

# class Singleton(object):
#   _instance = None
#   def __new__(class_, *args, **kwargs):
#     if not isinstance(class_._instance, class_):
#         class_._instance = object.__new__(class_, *args, **kwargs)
#     return class_._instance
#
# class MyClass(Singleton, BaseClass):
#   pass

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        
        return cls._instances[cls]

# @SingletonDecorator
class Parser(object): # without inheritance of ConfPars
    __metaclass__ = Singleton


    """
    i don't think that it is a good idea to keep whole parsing logic and variables in the one metod of a class.
    but i can't refactor this to any smart version
    """
    def parse(self):
        parser = SafeConfigParser() #without inheritance
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
print p.parse()
time.sleep(2)
s = Parser()
print s.parse()
time.sleep(2)
p2 = Parser()
print p2.parse()

print p == s == p2
#
# #
# # -*- coding: utf-8 -*-
# #
# # Copyright 2012-2015 Spotify AB
# #
# # Licensed under the Apache License, Version 2.0 (the "License");
# # you may not use this file except in compliance with the License.
# # You may obtain a copy of the License at
# #
# # http://www.apache.org/licenses/LICENSE-2.0
# #
# # Unless required by applicable law or agreed to in writing, software
# # distributed under the License is distributed on an "AS IS" BASIS,
# # WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# # See the License for the specific language governing permissions and
# # limitations under the License.
# #
#
# """
# luigi.configuration provides some convenience wrappers around Python's
# ConfigParser to get configuration options from config files.
#
# The default location for configuration files is luigi.cfg (or client.cfg) in the current
# working directory, then /etc/luigi/client.cfg.
#
# Configuration has largely been superseded by parameters since they can
# do essentially everything configuration can do, plus a tighter integration
# with the rest of Luigi.
#
# See :doc:`/configuration` for more info.
# """
#
# import logging
# import os
# import warnings
#
# try:
#     from ConfigParser import ConfigParser, NoOptionError, NoSectionError
# except ImportError:
#     from ConfigParser import ConfigParser, NoOptionError, NoSectionError
#
#
# class Parser(SafeConfigParser):
#     NO_DEFAULT = object()
#     _instance = None
#     _config_paths = [
#         '../../../etc/ecomap.conf'
#     ]
#     if '_CONFIG_PATH' in os.environ:
#         _config_paths.append(os.environ['_CONFIG_PATH'])
#
#     # @classmethod
#     # def add_config_path(cls, path):
#     #     cls._config_paths.append(path)
#     #     cls.reload()
#
#     @classmethod
#     def instance(cls, *args, **kwargs):
#         """ Singleton getter """
#         if cls._instance is None:
#             cls._instance = cls(*args, **kwargs)
#             # loaded = cls._instance.reload()
#             logging.getLogger('-interface').info('created inst')
#             while True:
#                 time.sleep(1)
#                 print 'while'
#                 return cls._instance
#         return cls._instance
#
#     # @classmethod
#     # def reload(cls):
#     #     # Warn about deprecated old-style config paths.
#     #     deprecated_paths = [p for p in cls._config_paths if os.path.basename(p) == 'client.cfg' and os.path.exists(p)]
#     #     if deprecated_paths:
#     #         warnings.warn("Luigi configuration files named 'client.cfg' are deprecated if favor of 'luigi.cfg'. " +
#     #                       "Found: {paths!r}".format(paths=deprecated_paths),
#     #                       DeprecationWarning)
#     #
#     #     return cls.instance().read(cls._config_paths)
#     @classmethod
#     def parse(self):
#         parser.read(configPath)
#         dct = {}
#         for section_name in parser.sections():
#             for name, value in parser.items(section_name):
#                 if value:
#                     try:
#                         value = parser.getboolean(section_name, name)
#                     except ValueError:
#                         try:
#                             if '.' in value:
#                                 value = parser.getfloat(section_name, name)
#                             else:
#                                 value = parser.getint(section_name, name)
#                         except ValueError:
#                             value = unicode(parser.get(section_name, name).decode('utf-8'))
#                 dct[section_name + '.' + name] = value
#         logger.debug('new conf read {}'.format(dct))
#         return dct
#
#     @classmethod
#     def timer(cls):
#         while True:
#             time.sleep(1)
#             return cls._instance
#
#
#
# def get_config():
#     """
#     Convenience method (for backwards compatibility) for accessing config singleton.
#     """
#     return Parser.instance()


# parser = Parser()
#
# # !properly working parsing function( with safe types converting)
# p = Parser.instance()
# s = Parser.instance()
# print p.parse()
# print s.parse()
# print p == s