Ecomap API Documentation
========================
Ecomap.org is a web service build on RESTful Api concept.
It has web-application, ios and android based clients


API start
---------

.. automodule:: views

.. autoflask:: ecomap.app:app
   :endpoints: index

.. function:: index



Admin API
---------

.. automodule:: admin_views

resources
_________
.. function:: resource_post

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
.. function:: permission_post

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
.. function:: role_post

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
.. function:: role_permission_post

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


Static Pages API
________________

.. autoflask:: ecomap.app:app
   :endpoints: add_page, edit_page, delete_page, get_titles, get_faq


User API
--------
main application api

authentication
______________
routes provides site logging and app authentication functions

.. automodule:: authorize_views
.. function:: register


.. autoflask:: ecomap.app:app
   :endpoints: register, login, logout, email_exist, oauth_login

restore user password
_____________________
routes provides restoring user account password

.. autoflask:: ecomap.app:app
   :endpoints: restore_password_request, restore_password_page, restore_password

change user password
____________________

.. autoflask:: ecomap.app:app
   :endpoints: change_password

user profile
____________

.. autoflask:: ecomap.app:app
   :endpoints: get_user_info, add_profile_photo, delete_profile_photo


Problem API
-----------
routes handling API connected with adding and managing environment problems

adding and viewing problems
___________________________

.. automodule:: problem_views
.. function:: problems

.. autoflask:: ecomap.app:app
   :endpoints: problems, detailed_problem, post_problem, get_user_problems, get_all_users_problems

photos
______

.. autoflask:: ecomap.app:app
   :endpoints: problem_photo

comments
________
functions for adding and viewing comments of problems

.. autoflask:: ecomap.app:app
   :endpoints: post_comment, get_comments
