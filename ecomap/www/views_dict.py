import imghdr

import json
import os
import uuid

from flask import render_template, request, jsonify, Response, g, abort
from flask_login import login_user, logout_user, login_required, current_user
from random import random

import ecomap.user as usr

from ecomap.app import app, logger
from ecomap.db import util as db
from ecomap.db.db_pool import DBPoolError
from ecomap.utils import Validators as v, validate

import functools

@app.route('/creation', methods=['GET','POST'])
def create_dict_for_roles():


(('admin', 'page', 'DELETE', 'Own'), 
('User', 'page', 'DELETE', 'Own'), 
('admin', 'page', 'PUT', 'Own'), 
('User', 'page', 'PUT', 'Own'), 
, 
, 
('admin', 'page', 'POST', 'Any'), 
('User', 'page', 'POST', 'Any'), 
('admin', 'page', 'DELETE', 'Own'), 
('User', 'page', 'DELETE', 'Own'), 
('admin', 'page', 'PUT', 'Own'), 
('User', 'page', 'PUT', 'Own'), 
('admin', 'page', 'PUT', 'Own'), 
('User', 'page', 'PUT', 'Own'), 
('admin', 'page', 'PUT', 'Own'), 
('User', 'page', 'PUT', 'Own'), 
('admin', 'googles', 'GET', 'Any'), 
('User', 'googles', 'GET', 'Any'), 
('admin', 'page', 'DELETE', 'Own'), 
('User', 'page', 'DELETE', 'Own'), 
('admin', 'page', 'DELETE', 'Own'), 
('User', 'page', 'DELETE', 'Own'), 
('admin', 'page', 'PUT', 'Own'), 
('User', 'page', 'PUT', 'Own'), 
('admin', 'page', 'DELETE', 'Own'), 
('User', 'page', 'DELETE', 'Own'))
