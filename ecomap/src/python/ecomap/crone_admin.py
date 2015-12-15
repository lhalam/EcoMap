# coding=utf-8

import time
import logging
import os
import optparse
import sys
from datetime import datetime

import ecomap.db.util as db
from ecomap.config import Config
from ecomap.utils import send_email


_CONFIG = Config().get_config()

parser = optparse.OptionParser(version='0.1',
                               description='Some text')
parser.add_option('-d', '--date', type='string', dest='file',
                  help='Input file for additional data')


def get_password_stats(date=None):
    if date:
        time.mktime(datetime.strptime(date, "%d/%m/%Y").timetuple())
        day_start = int(time.mktime(datetime.strptime(date, "%d/%m/%Y").timetuple()))
        day_end = day_start + 84600
        data = db.get_stored_data(day_start, day_end)
    else:
        last24h = int(time.time())-86400
        now = int(time.time())
        data = db.get_stored_data(last24h, now)

    email = 'vadime.padalko@gmail.com'
    send_email('daily_report',
               [_CONFIG['email.user_name'],
                _CONFIG['email.app_password'],
                _CONFIG['email.from_email'],
                email],
               data)


def refresh_table():
    last24h = int(time.time())-86400
    now = int(time.time())
    refresh_table = db.refresh_table(last24h, now)


def main():
    get_password_stats()
    refresh_table()

if __name__ == "__main__":
    sys.exit(main())
