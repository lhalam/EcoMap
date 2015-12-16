# coding=utf-8
import time
import logging
import os
import optparse
import sys
from datetime import datetime

import ecomap.db.util as db
from ecomap.config import Config
from ecomap.utils import send_email, get_logger, generate_email

_CONFIG = Config().get_config()

DESCRIPTION = """This script executes in crontab by default.
But you can manually run it with custom options.
Parameter list is shown bellow."""

USAGE = """
Please specify a type of activity to run script.
To set a type of activity use -t or --type option.
Allowed options parameters: <deletion>, <password>.

Use -h or --help for help.
"""

DATE_NOTICE = """Please enter a date in format yyyy-mm-dd to run a script for
a specific day. If date is not defined, script executes with default value.
Default date value is today's date from 00:00.
"""


def _get_date_params(date=None):
    print 'initial from get date'
    print date
    if date:
        try:
            dt = time.mktime(datetime.strptime(date, "%Y-%m-%d").timetuple())
            day_start = int(dt)
            day_end = day_start + 86400
        except ValueError:
            print DATE_NOTICE
            sys.exit(1)
    else:
        day_end = int(time.time())
        day_start_dt = datetime.now().replace(hour=0, minute=0,
                                              second=0, microsecond=0)
        day_start = int(time.mktime(day_start_dt.timetuple()))
        # print [day_start, day_end]
    return [day_start, day_end]


def make_template(data):
    with open((os.path.join(os.environ['CONFROOT'],
              "new_template.html")), "w") as html:
        html.write('')
        mes = '<h1>Жоден з користувачів пароль не змінював.</h1>'
        table_head = """<table>
            <tr>
                <th>користувач</th>
                <th>mail</th>
                <th>number request</th>
                <th>time</th>
            </tr>
        """
        table_row = """
            <tr>
                <td>%s</td>
                <td>%s</td>
                <td>%d</td>
                <td>%d</td>
            </tr>
        """
        if data:
            html.write(table_head)
            for x in data:
                html.write(table_row % (x[1].encode('utf-8'),
                                        x[2].encode('utf-8'),
                                        int(x[3]),
                                        int(x[0])))
            else:
                html.write('</table>')
        else:
            html.write(mes)


def get_password_stats(date):
    print 'initial date from get pass stat'
    print date
    custom_date = _get_date_params(date)
    start = custom_date[0]
    end = custom_date[1]
    print 'start is %s' % start
    print 'end is %s' % end
    # print type(start)
    # print type(end)
    data = db.get_stored_data(start, end)

    email = 'vadime.padalko@gmail.com'
    print 'OUTPUT:'
    print data
    logger.log(logger.level, 'TEST FROM CRON!!!!')

    # message = generate_email('registration', _CONFIG['email.from_email'],
    #                          email, data)

    # mes2 = generate_email('registration', _CONFIG['email.from_email'],
    #                          email, (first_name, last_name, email, password))

    # send_email(_CONFIG['email.user_name'],
    #            _CONFIG['email.app_password'],
    #            _CONFIG['email.from_email'],
    #            email,
    #            generate_email)


    # send_email('daily_report',
    #            [_CONFIG['email.user_name'],
    #             _CONFIG['email.app_password'],
    #             _CONFIG['email.from_email'],
    #             email], data)


def refresh_table():
    last24h = int(time.time())-86400
    now = int(time.time())
    refresh_table = db.refresh_table(last24h, now)


def _init_optparse():
    parser = optparse.OptionParser(usage=USAGE, version='0.1',
                                   description=DESCRIPTION)

    parser.add_option('-d', '--date', type='string', dest='date',
                      help=DATE_NOTICE, default=None)
    parser.add_option('-t', '--type', choices=['password', 'deletion'],
                      help='Set type of operation from predefined list.',
                      default=None)
    parser.add_option('-l', '--logging', default='INFO',
                      choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'],
                      help='Choose logging level from predefined list.')
    options, arguments = parser.parse_args()
    return options


def main():
    if options.type == 'password':
        get_password_stats(options.date)
    elif options.type == 'deletion':
        print 'RUN DELETION OF USER'
    else:
        print USAGE

    # refresh_table()

if __name__ == "__main__":
    options = _init_optparse()
    get_logger()
    logger = logging.getLogger('cron_admin')
    if options.logging:
        logger.setLevel(options.logging)

    sys.exit(main())
