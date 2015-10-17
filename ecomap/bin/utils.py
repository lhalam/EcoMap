# charset = utf-8
"""
logging to project local file(ecomap.conf), console(stdout)
    and rsyslog.LOG_LOCAL6 (file path: /var/log/ecomap_log.log)

seting-up your own syslog:
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

logging.config.fileConfig('logging.conf') # reading from logging config file
logger = logging.getLogger('ecomap') # initialization of our project logging system

# test log
logger.debug('TEST initial log from utils.py')




