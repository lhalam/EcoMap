# -*- coding: utf-8 -*-
"""Module contains functionality to send email to user."""
import smtplib
import os

from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Not needed when postfix will be configured.
USER_NAME = 'frut.jass779'
# Create secret within 2 step authentication in gmail.
# Not needed when postfix will be configured.
USER_KEY = 'your_key'
# Path to email template.
TEMPLATE_PATH = os.path.join(os.environ['CONFROOT'],
                             'registration_email_template.html')


def send_email(name, surname, email, password):
    """Sends email to new created users.
       :params: name - user name
                surname - user surname
                email - user email
                password - user password
    """
    html = open(TEMPLATE_PATH, 'rb').read().decode('utf-8')
    html_decoded = html % (unicode(name), unicode(surname), email,
                           unicode(password))

    msg = MIMEMultipart('alternative')
    msg['Subject'] = Header('Реєстрація на ecomap.org', 'utf-8')

    htmltext = MIMEText(html_decoded, 'html', 'utf-8')

    msg.attach(htmltext)
    msg['Subject'] = 'Test email'
    msg['From'] = 'admin@ecomap.com'
    msg['To'] = email

    server = smtplib.SMTP_SSL('smtp.gmail.com')
    server.login(USER_NAME, USER_KEY)
    server.sendmail('admin@ecomap.com', email,
                    msg.as_string())
    server.quit()

if __name__ == '__main__':
    send_email('Illya', 'Pavlovskiy', 'frut.jass779@gmail.com',
               'password')
