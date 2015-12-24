Документація Ecomap API
=======================
this is description of flask auto http


custom endpoints
----------------

description of custom

.. automodule:: views
.. autoflask:: ecomap.app:app
   :endpoints: index, get_titles, get_faq


Admin API
---------

.. automodule:: admin_views

resources
_________
this routes handles REST operations with site resources

``@login_required``

access for role:
   admin

:request headers:
   - Accept: `application/json, text/plain, */*`
   - Authorization: `remember_token to authenticate`
:response header:
   - Content-Type: `application/json`

.. autoflask:: ecomap.app:app
   :endpoints: resource_get, resource_post, resource_put, resource_delete

permissions
___________
this group of rotes provides control of permissions to site resources URLs

``@login_required``

access for role:
   admin

:request headers:
   - Accept: `application/json, text/plain, */*`
   - Authorization: `remember_token to authenticate`
:response header:
   - Content-Type: `application/json`

.. autoflask:: ecomap.app:app
   :endpoints: permission_get, permission_post, permission_put, permission_delete, get_all_permissions

roles
_____
this routes handles REST operations with site role base access control

``@login_required``

access for role:
   admin

:request headers:
   - Accept: `application/json, text/plain, */*`
   - Authorization: `remember_token to authenticate`
:response header:
   - Content-Type: `application/json`

.. autoflask:: ecomap.app:app
   :endpoints: role_get, role_post, role_put, role_delete, get_all_users, get_all_users_info


role_permission
_______________
this routes handles REST operations with site role base access control

``@login_required``

access for role:
   admin

:request headers:
   - Accept: `application/json, text/plain, */*`
   - Authorization: `remember_token to authenticate`
:response header:
   - Content-Type: `application/json`

.. autoflask:: ecomap.app:app
   :endpoints: role_permission_get, role_permission_post, role_permission_put, role_permission_delete


USER API
--------
main application api

authentication
______________
routes provides site logging and app authentication functions

.. autoflask:: ecomap.app:app
   :endpoints: register, login, logout, email_exist, oauth_login

restore user password
_____________________
routes provides restoring user account password

.. autoflask:: ecomap.app:app
   :endpoints: restore_password_request, restore_password_page, restore_password

PROBLEMS API
------------

.. autoflask:: ecomap.app:app
   :endpoints: problems, detailed_problem, post_problem, get_user_problems, get_all_users_problems, problem_photo, post_comment, get_comments

