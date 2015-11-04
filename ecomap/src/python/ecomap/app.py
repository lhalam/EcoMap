import os
from datetime import timedelta

from flask import Flask

template_folder = os.path.join(os.environ['PRODROOT'], 'www/templates/')
app = Flask(__name__, template_folder=template_folder)

app.config['SECRET_KEY'] = 'a7c268ab01141868811c070274413ea3c588733241659fcb'
app.config["REMEMBER_COOKIE_DURATION"] = timedelta(days=14)
