Документація API
================
Заголовок содержит главную тему и отделяется символами '='.
Их количество должно быть не меньше, чем количество символов
в заголовке.



Quickstart
----------
Подзаголовки отделяются символами '-'. Их количество должно 
быть тем же, что и количество символов в подзаголовке
(так же, как и в случае с заголовками).

Списки могут быть маркированными:

 * Элемент Foo
 * Элемент Bar

Или же автоматически пронумерованными:

 #. Элемент 1
 #. Элемент 2

Admin API
=========
Слова можно выделять *наклонным* или **полужирным** шрифтами.
Фрагменты кода (например, примеры команд) можно заключать в обратные кавычки, например:
команда ``sudo`` дает вам привилегии суперпользователя!

**/api/resources**
------------------
 * METHOD: *GET*

  ARGUMENTS: None

  DESCRIPTION: Function which returns resources list from db with pagination options.

  :return: 
   json such format:
    ``[ [{"resource_name": "name", "id": 1}, {"resource_name":      
    "name_2","id": 2}], [{"total_res_count": 2}] ]``

 * METHOD: *POST*

  ARGUMENTS: None

  DESCRIPTION: Function which edits resource name.
  
  :return: 
   If there is already resource with this name:
    ``{'error': 'resource already exists'}, 400``
   If request data is invalid:
    ``{'status': False, 'error': [list of errors]}, 400``
   If all ok:
    ``{'added_resource': 'resource_name','resource_id': 'resource_id'}``




**/api/permissions**
--------------------
METHOD: 
  *DELETE*

  ARGUMENTS:
    None

  DESCRIPTION: 
    Function which edits permission.

  :return: 
   If permission is binded with any role:
    ``{'error': 'Cannot delete!'}``
   If request data is invalid:
    ``{'status': False, 'error': [list of errors]}, 400``
   If all ok:
    ``{'status': 'success','edited_perm_id': 'permission_id'}``
   
:method: *GET*
 
 :arguments: None

 :description: Function which gets all permissions.  
 
 :return: 
   ``{'permission_id': 'permission_id', 'action': 'action',
   'modifier': 'modifier', 'description': 'description'}``


User API
========
Слова можно выделять *наклонным* или **полужирным** шрифтами.
Фрагменты кода (например, примеры команд) можно заключать в обратные кавычки, например:
команда ``sudo`` дает вам привилегии суперпользователя!

**/**
-----
 * METHOD: *GET*

  ARGUMENTS: None

  DESCRIPTION: Enter to site Renders a main template for single-page application.


