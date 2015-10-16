
"""
logging to local file(ecomap.conf), console and syslog.LOG_LOCAL6 (/var/log/ecomap_log.log)

seting-up syslog:
    1. go to /etc/rsyslog.d/
    2. create file ecomap.conf
    3. add to ecomap.conf this line:
            local6.*        /var/log/ecomap_log.log
    4. run in terminal: sudo restart rsyslog

    5. now logs from ecomap project will be sending via UDP socket to our system
        and will be stored locally in our system.
        path to logs = in /var/log/ecomap_log.log
"""
import logging
import logging.config

logging.config.fileConfig('logging.cfg')
logger = logging.getLogger('ecomap')

# log something
logger.debug(' NEW NEW debug message')
logger.info('info message')
logger.warn('warn message')
logger.error('error message')
logger.critical('critical message')



