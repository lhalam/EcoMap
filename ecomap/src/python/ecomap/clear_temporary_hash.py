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
    return [day_start, day_end]


def make_template(data):
    template_path = (os.path.join(os.environ['CONFROOT'],
                     "daily_report.html"))
    with open(template_path, "w") as html:
        html.write('')
        mes = '<h1>За даний період не було активності користувачів.</h1>'
        table_head = """<table>
            <tr>
                <th>користувач</th>
                <th>email</th>
                <th>кількість спроб зміни паролю</th>
                <th>дата зміни</th>
            </tr>
        """
        table_row = """
            <tr>
                <td>%s</td>
                <td>%s</td>
                <td>%d</td>
                <td>%s</td>
            </tr>
        """
        if data:
            html.write(table_head)
            for x in data:
                html.write(table_row % (x[1].encode('utf-8'),
                                        x[2].encode('utf-8'),
                                        int(x[3]),
                                        datetime.fromtimestamp(x[0]).date()))

            else:
                html.write('</table>')
        else:
            html.write(mes)

    return template_path


def get_password_stats(date):
    custom_date = _get_date_params(date)
    start = custom_date[0]
    end = custom_date[1]

    data = db.get_hash_data(start, end)

    print 'Sending email.'
    print data
    report_date = datetime.fromtimestamp(start).date()
    logger.log(logger.level, 'Email with statistic info for %s has been sent.'
               % report_date)

    templ = make_template(data)
    header = 'Звіт адміністратора ecomap.org за %s.' % report_date
    message = generate_email(header, _CONFIG['email.from_email'],
                             _CONFIG['email.admin_email'],
                             args=None, custom_template=templ)
    send_email(_CONFIG['email.user_name'],
               _CONFIG['email.app_password'],
               _CONFIG['email.from_email'],
               _CONFIG['email.admin_email'],
               message)


def get_deletion_stats(date):
    custom_date = _get_date_params(date)
    start = custom_date[0]
    end = custom_date[1]

    data = db.get_deletion_data(start, end)

    print 'Sending email.'
    print data
    report_date = datetime.fromtimestamp(start).date()
    logger.log(logger.level, 'Email with statistic info for %s has been sent.'
               % report_date)

    templ = make_template(data)
    header = 'Звіт адміністратора ecomap.org за %s.' % report_date
    message = generate_email(header, _CONFIG['email.from_email'],
                             _CONFIG['email.admin_email'],
                             args=None, custom_template=templ)
    send_email(_CONFIG['email.user_name'],
               _CONFIG['email.app_password'],
               _CONFIG['email.from_email'],
               _CONFIG['email.admin_email'],
               message)


def clear_password_hash(date):
    custom_date = _get_date_params(date)
    start = custom_date[0]
    end = custom_date[1]
    report_date = datetime.fromtimestamp(start).date()

    print 'Cleaning-up database.'
    logger.log(logger.level, 'Temporary hashes for %s has been cleared.'
               % report_date)

    db.clear_password_hash(start, end)


def clear_user_deletion_hash(date):
    custom_date = _get_date_params(date)
    start = custom_date[0]
    end = custom_date[1]
    report_date = datetime.fromtimestamp(start).date()

    print 'Cleaning-up database.'

    logger.log(logger.level, 'Temporary hashes for %s has been cleared.'
               % report_date)

    db.clear_user_deletion_hash(start, end)


def _init_optparse():
    parser = optparse.OptionParser(usage=USAGE, version='0.1',
                                   description=DESCRIPTION)

    parser.add_option('-d', '--date', type='string', dest='date',
                      help=DATE_NOTICE, default=None)
    parser.add_option('-t', '--type', choices=['password', 'deletion'],
                      help='Set type of operation from predefined list.',
                      default=None)
    parser.add_option('-v', '--verbosity', default='INFO',
                      choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'],
                      help='Choose logging level from predefined list.')
    options, arguments = parser.parse_args()
    return options


def main():
    if options.type == 'password':
        get_password_stats(options.date)
        clear_password_hash(options.date)
    elif options.type == 'deletion':
        get_deletion_stats(options.date)
        clear_user_deletion_hash(options.date)
    else:
        print USAGE


if __name__ == "__main__":
    options = _init_optparse()
    get_logger()
    logger = logging.getLogger('cron_admin')
    if options.verbosity:
        logger.setLevel(options.verbosity)

    sys.exit(main())
