# coding=utf-8
import time
from ecomap.app import app
from flask import render_template

import ecomap.db.util as db

from ecomap.config import Config
from ecomap.utils import send_email

from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def admin_stats_template(data=None):
    """Sends email to new created users.
       :params: app_name - app's login
                app_key - app's key
                name - user name
                surname - user surname
                email - user email
                password - user password
    """
    msg = MIMEMultipart('alternative')
    msg['Subject'] = Header('звіт адміністратора на ecomap.org', 'utf-8')

    with app.app_context():
        msg.html = render_template('admin_report.html', data=data)

    htmltext = MIMEText(msg.html, 'html', 'utf-8')
    msg.attach(htmltext)
    msg['Subject'] = 'звіт за добу'
    msg['From'] = 'admin@ecomap.com'
    msg['To'] = 'vadime.padalko@gmail.com'
    return msg

_CONFIG = Config().get_config()
last24h = int(time.time())-86400
now = int(time.time())

data = db.get_change_pass_stats(last24h)

# Insert here admins email_variable.
email = 'vadime.padalko@gmail.com'
send_email(_CONFIG['email.user_name'],
           _CONFIG['email.app_password'],
           admin_stats_template(data), email)

refresh_table = db.refresh_table(last24h, now)
