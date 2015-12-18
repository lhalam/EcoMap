# coding=utf-8
"""
This script executes in crontab by default.
But you can manually run it with custom options.
Parameter list is shown bellow
"""
import time
import logging
import optparse
import sys

import ecomap.db.util as db
from ecomap.config import Config
from ecomap import utils

_CONFIG = Config().get_config()
utils.get_logger()
LOGGER = logging.getLogger('cron_admin')


DESCRIPTION = """This script executes in crontab by default.
But you can manually run it with custom options.
Parameter list is shown bellow."""

USAGE = """
Please specify a type of activity to run script.
To set a type of activity use -t or --type option.
Allowed options parameters: <delete>, <password>.

Use -h or --help for help.
"""

DATE_NOTICE = """Please enter a date in format yyyy-mm-dd to run a script for
a specific day. If date is not defined, script executes with default value.
Default date value is today's date from 00:00.
"""


def _get_date_params(date=None):
    """Helper function provides proper date definition. Converts date from
    string format 'yyyy-mm-dd' to tuple with start period timestamp and end
    period timestamp.

    :param date: if defined - takes a date of report time period in string
    format 'yyyy-mm-dd'
    if not defined - default value is date of yesterday.
    :return: tuple with start time period in timestamp and end of period
     in timestamp
    """
    if date:
        try:
            day_start = int(time.mktime(time.strptime(date, '%Y-%m-%d')))
            day_end = day_start + 86400
        except ValueError:
            LOGGER.log(LOGGER.level, 'Error: invalid date format. %s',
                       DATE_NOTICE)
            sys.exit(1)
    else:
        date = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        day_end = int(time.mktime(time.strptime(date, '%Y-%m-%d')))
        day_start = day_end - 86400
    return day_start, day_end


def generate_string_template(data):
    """Function generates dynamic template of string type. Template consists of
    db query result with daily report statistics or with static content if was
    no user activity for this time period.

    :param data: query tuple from db with user activity data
    :return: string buffer with html markup
    """
    html = ''
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
        html += table_head
        for column in data:
            html += table_row % (column[1].encode('utf-8'),
                                 column[2].encode('utf-8'),
                                 int(column[3]),
                                 time.strftime('%Y-%m-%d',
                                               time.gmtime(column[0])))
        html += '</table>'
    else:
        html += mes

    return html


def generate_password_stats(date):
    """Function takes date tuple and gets user activity data from db according
    to chosen date. After that function sends email with custom template
     to admin's mailbox.

    :param date: tuple with 2 timestamp arguments(start_period, end_period)
    """
    custom_date = _get_date_params(date)
    start = custom_date[0]
    end = custom_date[1]

    data = db.get_hash_data(start, end)

    report_date = time.strftime('%Y-%m-%d', time.gmtime(start))
    LOGGER.log(LOGGER.level, 'Email with statistic info for %s has been sent.',
               report_date)

    template = generate_string_template(data)
    header = 'Звіт адміністратора ecomap.org за %s.' % report_date

    message = utils.generate_email('daily_report', _CONFIG['email.from_email'],
                                   _CONFIG['email.admin_email'],
                                   args=None, header=header,
                                   template_str=template)

    utils.send_email(_CONFIG['email.user_name'],
                     _CONFIG['email.app_password'],
                     _CONFIG['email.from_email'],
                     _CONFIG['email.admin_email'],
                     message)


def generate_deletion_stats(date):
    """Function takes date tuple and gets user activity data from db according
    to chosen date. After that function sends email with custom template
     to admin's mailbox.

    :param date: tuple with 2 timestamp arguments(start_period, end_period)
    """
    custom_date = _get_date_params(date)
    start = custom_date[0]
    end = custom_date[1]

    data = db.get_deletion_data(start, end)

    report_date = time.strftime('%Y-%m-%d', time.gmtime(start))
    LOGGER.log(LOGGER.level, 'Email with statistic info for %s has been sent.',
               report_date)

    template = generate_string_template(data)
    header = 'Звіт адміністратора ecomap.org за %s.' % report_date

    message = utils.generate_email('daily_report', _CONFIG['email.from_email'],
                                   _CONFIG['email.admin_email'],
                                   args=None, header=header,
                                   template_str=template)

    utils.send_email(_CONFIG['email.user_name'],
                     _CONFIG['email.app_password'],
                     _CONFIG['email.from_email'],
                     _CONFIG['email.admin_email'],
                     message)


def clear_password_hash(date):
    """Function clears temporary hashes of user's change password activity
     stored in DB for defined date.

    :param date: tuple with 2 timestamp arguments(start_period, end_period)
    """
    custom_date = _get_date_params(date)
    start = custom_date[0]
    end = custom_date[1]
    report_date = time.strftime('%Y-%m-%d', time.gmtime(start))

    LOGGER.log(LOGGER.level, 'Temporary hashes for %s has been cleared.',
               report_date)

    db.clear_password_hash(start, end)


def clear_user_deletion_hash(date):
    """Function clears temporary hashes with profile deletion confirmation.

    :param date: tuple with 2 timestamp arguments(start_period, end_period)
    """
    custom_date = _get_date_params(date)
    start = custom_date[0]
    end = custom_date[1]
    report_date = time.strftime('%Y-%m-%d', time.gmtime(start))

    LOGGER.log(LOGGER.level, 'Temporary hashes for %s has been cleared.',
               report_date)

    db.clear_user_deletion_hash(start, end)


def main():
    """Main module function. Initializes option parser and handles execution
    logic due to selected options.
    :return:
    """
    parser = optparse.OptionParser(usage=USAGE, version='0.1',
                                   description=DESCRIPTION)

    parser.add_option('-d', '--date', type='string', dest='date',
                      help=DATE_NOTICE)
    parser.add_option('-t', '--type', choices=('password', 'delete'),
                      help='Set type of operation from predefined list.')
    parser.add_option('-v', '--verbosity', default='INFO',
                      choices=('DEBUG', 'INFO', 'WARNING', 'ERROR'),
                      help='Choose logging level from predefined list.')
    options = parser.parse_args()[0]

    if options.verbosity:
        LOGGER.setLevel(options.verbosity)

    if options.type == 'password':
        generate_password_stats(options.date)
        clear_password_hash(options.date)
    elif options.type == 'delete':
        generate_deletion_stats(options.date)
        clear_user_deletion_hash(options.date)
    else:
        LOGGER.log(LOGGER.level, 'Please check required input args. %s', USAGE)


if __name__ == "__main__":
    sys.exit(main())
