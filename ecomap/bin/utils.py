# charset = utf-8
"""
seting-up your own syslog on Ubuntu:
    1. go to /etc/rsyslog.d/
    2. create file ecomap.conf
    3. add to newly created file ecomap.conf this line:
            local6.*        /var/log/ecomap_log.log
    4. run in terminal: sudo restart rsyslog

    5. now logs from ecomap project will be sending via UDP socket to our system
        and will be stored locally in our system.
        path to logs = in /var/log/ecomap_log.log
    6. run this file to test.
    if everything is OK you'll get:
        1. log message in console
        2. local logfile stored in project_directory
        3. log file in your system rsyslog (file path: /var/log/ecomap_log.log)
        4. all this logs must have different output format
    7. to add logger function to your module just make such import:

            from utils import logger

        *in case if environment is setted up properly
         or copy files(utils.py and logging.conf) to your module directory
         and make import
"""
import logging
import logging.config


def get_logger(logger_name):
    """
    :param logger_name: your custom name of new created logger object
    :return: logger object ready to use. just assign it to some variable
    example logger = get_logger('your_name')
    """
    logging.config.fileConfig('logging.conf')
    return logging.getLogger(logger_name)

# example usage
logger = get_logger('ecomap')
# test log
logger.debug('TEST initial log from utils.py')


class Singleton(type):
    """
    using a singleton pattern to work with only one possible instance of Pool
    """
    def __call__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            cls._instance = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instance

