# coding=utf-8
"""
This module holds all views controls for
ecomap project.
"""
from flask import render_template, session, request, Response, g, url_for, abort
from flask_login import current_user

from ecomap.app import app, logger
from authorize_views import *
from admin_views import *
from user_views import *
from problem_views import *

from ecomap.db import util as db
from ecomap.permission import permission_control, check_permissions


@app.before_request
def load_users():
    """Function to check if user is authenticated, else creates
       Anonymous user.
       Launches before requests.
    """
    if current_user.is_authenticated:
        g.user = current_user
    else:
        anon = ecomap_usr.Anonymous()
        g.user = anon
        # logger.info(g.user.role)
        # logger.info(current_user)
    logger.info('current user is %s, %s', g.user.role, g.user)


# @app.before_request
def check_access():
    """Global decorator for each view.
    Checks permissions to access app resources by each user's request.
    Gets dynamic user info(user role, url, request method)from request context.
    :return: nested function returns true or 403
    """
    logger.info(session)
    if 'access_control' not in session:
        session['access_control'] = permission_control.get_dct()
    session['access_control'] = permission_control.reload_dct()
    logger.info(session)
    access_rules = session['access_control']
    route = '/' + '/'.join(request.url.split('/')[3:])
    access_result = check_permissions(current_user.role,
                                      route, request.method, access_rules)
    if not access_result['error']:
        access_status = access_result['status']
        logger.info('ACCESS STATUS: %s DETAILS:(url= %s[%s], user ID:%s (%s))'
                 % (access_status, route, request.method, current_user.uid,
                    current_user.role))
    else:
        logger.debug('ACCESS: FORBIDDEN! DETAILS:(url= %s[%s], '
                     'user ID:%s (%s), errors=%s)'
                     % (route, request.method, current_user.uid,
                        current_user.role, access_result['error']))
        abort(403)


@app.route('/', methods=['GET'])
def index():
    """Controller starts main application page.
    return: renders html template with angular app.
    """
    return render_template('index.html')


@app.route('/api/getTitles', methods=['GET'])
def get_titles():
    """This method returns short info about all defined static pages.

      :returns list of dicts with title, id, alias and is_enabled
      values.
    """
    if request.method == 'GET':
        pages = db.get_pages_titles()
        result = []
        if pages:
            for page in pages:
                result.append({'id': page[0],
                               'title': page[1],
                               'alias': page[2],
                               'is_enabled': page[3]})
        return Response(json.dumps(result), mimetype="application/json")


@app.route('/api/resources/<alias>', methods=['GET'])
def get_faq(alias):
    """This method retrieves exact faq page(ex-resource) via
       alias, passed to it.

        :params - alias - url path to exact page.

        :returns object with all page's attributes within a list.
    """
    if request.method == 'GET':
        page = db.get_page_by_alias(alias)
        status_code = None
        result = None
        if page:
            result = [{'id': page[0],
                       'title': page[1],
                       'alias': page[2],
                       'description': page[3],
                       'content': page[4],
                       'meta_keywords': page[5],
                       'meta_description': page[6],
                       'is_enabled': page[7]}]
            status_code = 200
        else:
            result = []
            status_code = 404
        return Response(json.dumps(result), mimetype="application/json",
                        status=status_code)


if __name__ == '__main__':
    app.run()
