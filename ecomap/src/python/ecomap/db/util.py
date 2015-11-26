"""This module contains functions for interacting with Database."""
from ecomap.db.db_pool import db_pool, retry_query


@retry_query(tries=3, delay=1)
def get_user_by_email(email):
    """Return user, found by email.
    :params: email - user email
    :retrun: tuple with user info
    """
    with db_pool().manager() as conn:
        cursor = conn.cursor()
        query = """SELECT `id`, `first_name`, `last_name`, `email`,
                   `password`, `avatar`
                   FROM `user` WHERE `email`=%s;
                """
        cursor.execute(query, (email,))
        return cursor.fetchone()


@retry_query(tries=3, delay=1)
def get_user_by_id(user_id):
    """Return user, found by id.
    :params: user_id - id of user
    :return: tuple with user info
    """
    with db_pool().manager() as conn:
        cursor = conn.cursor()
        query = """SELECT `id`, `first_name`, `last_name`, `email`,
                   `password`, `avatar`
                   FROM `user` WHERE `id`=%s;
                """
        cursor.execute(query, (user_id,))
        return cursor.fetchone()


@retry_query(tries=3, delay=1)
def get_user_by_oauth_id(user_id):
    """Return user, found by id.
    :params: user_id - id of user
    :return: tuple with user info
    """
    with db_pool().manager() as conn:
        cursor = conn.cursor()
        query = """SELECT `id`, `first_name`, `last_name`, `email`, `password`
                   FROM `user` WHERE `oauth_uid`=%s;
                """
        cursor.execute(query, (user_id,))
        return cursor.fetchone()


@retry_query(tries=3, delay=1)
def add_oauth_to_user(user_id, oauth_provider, oauth_uid):
    """Adds oauth id and provider name to user.
       This grants authentication within oauth to user.
       :params: user_id - id of user
                oauth_provider - provider name
                oauth_uid - user id from provider
    """
    with db_pool().manager() as conn:
        cursor = conn.cursor()
        query = """UPDATE `user` SET `oauth_provider`=%s,
                   `oauth_uid`=%s WHERE `id`=%s;
                """
        cursor.execute(query, oauth_provider, oauth_uid, user_id)
        conn.commit()


@retry_query(tries=3, delay=1)
def facebook_insert(first_name, last_name, email, password, role_id,
                    provider, uid):
    """Adds new user into db through facebook.
    :params: first_name - first name of user
             last_name - last name of user
             email - email of user
             password - hashed password of user
    """
    with db_pool().manager() as conn:
        conn.autocommit(True)
        cursor = conn.cursor()
        query = """INSERT INTO `user` (`first_name`,
                                       `last_name`,
                                       `email`,
                                       `password`,
                                       `oauth_provider`,
                                       `oauth_uid`)
                   VALUES (%s, %s, %s, %s, %s, %s);
                   INSERT INTO `user_role` (`user_id`, `role_id`)
                   values (LAST_INSERT_ID(), %s);
                """
        cursor.execute(query, (first_name, last_name, email, password,
                               provider, uid, role_id))


@retry_query(tries=3, delay=1)
def insert_user(first_name, last_name, email, password, role_id):
    """Adds new user into db.
    :params: first_name - first name of user
             last_name - last name of user
             email - email of user
             password - hashed password of user
    """
    with db_pool().manager() as conn:
        conn.autocommit(True)
        cursor = conn.cursor()
        query = """INSERT INTO `user` (`first_name`,
                                       `last_name`,
                                       `email`,
                                       `password`)
                   VALUES (%s, %s, %s, %s);
                   INSERT INTO `user_role` (`user_id`, `role_id`)
                   values (LAST_INSERT_ID(), %s);
                """
        cursor.execute(query, (first_name, last_name, email, password,
                               role_id))


@retry_query(tries=3, delay=1)
def get_role_id(name='user'):
    """Gets role id by it's name.
       :params: name - name of role, default - 'user'
       :return: tuple with id of role
    """
    with db_pool().manager() as conn:
        cursor = conn.cursor()
        query = """SELECT `id` FROM `role`
                   WHERE `name`=%s;"""
        cursor.execute(query, (name,))
        return cursor.fetchone()


@retry_query(tries=3, delay=1)
def get_role_by_name(name='user'):
    """Gets role id by it's name.
       :params: name - name of role, default - 'user'
       :return: tuple with id of role
    """
    with db_pool().manager() as conn:
        cursor = conn.cursor()
        query = """SELECT `id` FROM `role`
                   WHERE `name`=%s;"""
        cursor.execute(query, (name,))
        return cursor.fetchone()


@retry_query(tries=3, delay=1)
def insert_user_avatar(user_id, img_path):
    """Insert new user  avatar into db.
    :params: user_id - unique id user
             img_path - path to avatar image
    """
    with db_pool().manager() as conn:
        cursor = conn.cursor()
        query = """UPDATE `user` SET `avatar` = %s WHERE id = %s;"""
        cursor.execute(query, (img_path, user_id))
        conn.commit()


@retry_query(tries=3, delay=1)
def delete_user_avatar(user_id):
    """Deletes user profile photo from db.
    :params: user_id - unique id user

    """
    with db_pool().manager() as conn:
        cursor = conn.cursor()
        query = """UPDATE `user` SET `avatar` = '' WHERE `id`=%s;"""
        cursor.execute(query, (user_id,))
        conn.commit()


@retry_query(tries=3, delay=1)
def change_user_password(user_id, new_password):
    """Change password to user account.
    :params: new_password - new password
             user_id - id of user
    """
    with db_pool().manager() as conn:
        cursor = conn.cursor()
        query = """UPDATE `user` SET `password`=%s WHERE `id`=%s;"""
        cursor.execute(query, (new_password, user_id))
        conn.commit()


@retry_query(tries=3, delay=1)
def get_user_role_by_email(email):
    """Get all resources.
    :return: tuple of resources
    """
    with db_pool().manager() as conn:
        cursor = conn.cursor()
        query = """SELECT r.name FROM `user_role` AS ur
                   INNER JOIN `user` AS u ON ur.user_id = u.id
                   INNER JOIN `role` AS r ON ur.role_id = r.id
                   WHERE u.email=%s;
                """
        cursor.execute(query, (email,))
        return cursor.fetchone()


def get_all_permissions_by_role():
    """This query created for Restriction class.
    Restriction class is for lesser entering to DB.
    """
    with db_pool().manager() as conn:
        cursor = conn.cursor()
        query = """SELECT r.name , res.resource_name, p.action, p.modifier
                   FROM `role_permission` AS rp INNER JOIN `permission` AS p ON
                   rp.permission_id = p.id INNER JOIN `role` AS r
                   ON rp.role_id = r.id INNER JOIN `resource` AS res
                   ON p.resource_id = res.id;
                """
        cursor.execute(query)
    return cursor.fetchall()


@retry_query(tries=3, delay=1)
def get_user_role_by_id(user_id):
    """Get all resources.
    :return: tuple of resources
    """
    with db_pool().manager() as conn:
        cursor = conn.cursor()
        query = """SELECT r.name FROM `role` AS r
                   INNER JOIN `user_role` AS ur ON r.id=ur.role_id
                   WHERE ur.user_id=%s;
                """
        cursor.execute(query, (user_id,))
        return cursor.fetchone()


@retry_query(tries=3, delay=1)
def get_all_resources():
    """Get all resources.
    :return: tuple of resources
    """
    with db_pool().manager() as conn:
        cursor = conn.cursor()
        query = """SELECT `id`, `resource_name` FROM `resource`;"""
        cursor.execute(query)
        return cursor.fetchall()


@retry_query(tries=3, delay=1)
def get_resource_id(resource_name):
    """Gets resource id.
    :params: resource_name - name of resource
    :return: tuple, containing id
    """
    with db_pool().manager() as conn:
        cursor = conn.cursor()
        sql = """SELECT `id` FROM `resource` WHERE `resource_name`=%s;"""
        cursor.execute(sql, (resource_name,))
        return cursor.fetchone()


@retry_query(tries=3, delay=1)
def add_resource(resource_name):
    """Adds new resource in db.
    :params: resource_name - name of new resource
    """
    with db_pool().manager() as conn:
        cursor = conn.cursor()
        query = """INSERT INTO `resource` (`resource_name`)
                   VALUES (%s);
                """
        cursor.execute(query, (resource_name,))
        conn.commit()


@retry_query(tries=3, delay=1)
def edit_resource_name(new_resource_name, resource_id):
    """Edit resource name.
    :params: new_resource_name - new name of resource
             resource_id - id of  resource we change name
    """
    with db_pool().manager() as conn:
        cursor = conn.cursor()
        query = """UPDATE `resource` SET `resource_name`=%s WHERE `id`=%s;"""
        cursor.execute(query, (new_resource_name, resource_id))
        conn.commit()


@retry_query(tries=3, delay=1)
def get_all_roles():
    """Return all roles in db.
    :return: tuple, containing all roles
    """
    with db_pool().manager() as conn:
        cursor = conn.cursor()
        query = """SELECT `id`, `name` FROM `role`;"""
        cursor.execute(query)
        return cursor.fetchall()


@retry_query(tries=3, delay=1)
def insert_role(role_name):
    """Insert new role into db.
    :params: role_name - name of role
    """
    with db_pool().manager() as conn:
        cursor = conn.cursor()
        query = """INSERT INTO `role` (`name`) VALUES (%s);"""
        cursor.execute(query, (role_name,))
        conn.commit()


@retry_query(tries=3, delay=1)
def edit_role(new_role_name, role_id):
    """Edit role name.
    :params: role_name - new name of role
             role_id - if of role
    """
    with db_pool().manager() as conn:
        cursor = conn.cursor()
        query = """UPDATE `role` SET `name`=%s WHERE `id`=%s;"""
        cursor.execute(query, (new_role_name, role_id))
        conn.commit()


@retry_query(tries=3, delay=1)
def get_all_permissions_by_resource(resource_id):
    """Find all permissions by resource.
    :params: resource_id - id of resource
    :return: tuple, containing permissions
    """
    with db_pool().manager() as conn:
        cursor = conn.cursor()
        query = """SELECT `id`, `action`, `modifier`, `description`
                   FROM `permission` WHERE `resource_id`=%s;
                """
        cursor.execute(query, (resource_id,))
        return cursor.fetchall()


@retry_query(tries=3, delay=1)
def get_all_permissions():
    """Find all permissions by resource.
    :params: resource_id - id of resource
    :return: tuple, containing permissions
    """
    with db_pool().manager() as conn:
        cursor = conn.cursor()
        query = """SELECT p.id, r.resource_name, p.action, p.modifier,
                   p.description
                   FROM `permission` as p
                   INNER JOIN `resource` as r
                   ON p.resource_id = r.id;"""
        cursor.execute(query)
        return cursor.fetchall()


@retry_query(tries=3, delay=1)
def insert_permission(resource_id, action, modifier, description):
    """Insert new permission.
    :params: resource_id - id of resource
             action - action (POST, GET, DELETE, PUT)
             modifier - modifier (Own, Any, None)
             description - short description to this permission
    """
    with db_pool().manager() as conn:
        cursor = conn.cursor()
        query = """INSERT INTO `permission` (`resource_id`,
                                             `action`,
                                             `modifier`,
                                             `description`)
                   VALUES (%s, %s, %s, %s);
                """
        cursor.execute(query, (resource_id, action, modifier, description))
        conn.commit()


def edit_permission(action, modifier, permission_id, description):
    """Edit permission.
    :params: action - action (POST, GET, DELETE, PUT)
             modifier - modifier (Own, Any, None)
             permission_id - if of permission we want to update
             description - short description to this permission
    """
    with db_pool().manager() as conn:
        cursor = conn.cursor()
        query = """UPDATE `permission` SET `description`=%s, `action`=%s,
                   `modifier`=%s WHERE `id`=%s;
                """
        cursor.execute(query, (description, action, modifier, permission_id))
        conn.commit()


@retry_query(tries=3, delay=1)
def get_permission_id(resource_id, action, modifier):
    """Return permission id.
    :params: resource_id - id of resource
             action - action (POST, GET, DELETE, PUT)
             modifier - modifier (Own, Any, None)
    :return: tuple, containing permission id"""
    with db_pool().manager() as conn:
        cursor = conn.cursor()
        query = """SELECT `id` FROM `permission` WHERE `resource_id`=%s AND
                   `action`=%s AND `modifier`=%s;
                """
        cursor.execute(query, (resource_id, action, modifier))
        return cursor.fetchone()


@retry_query(tries=3, delay=1)
def set_role_to_user(user_id, role_id):
    """Set role to user.
    :params: user_id - id of user
             role_id - id of role
    """
    with db_pool().manager() as conn:
        cursor = conn.cursor()
        query = """INSERT INTO `user_role` (`user_id`,
                                            `role_id`)
                   VALUES (%s, %s);
                """
        cursor.execute(query, (user_id, role_id))
        conn.commit()


@retry_query(tries=3, delay=1)
def change_user_role(role_id, user_id):
    """Update users role.
    :params: user_id - id of user
             role_id - id of role
    """
    with db_pool().manager() as conn:
        cursor = conn.cursor()
        query = """UPDATE `user_role` SET `role_id`=%s WHERE `user_id`=%s;"""
        cursor.execute(query, (role_id, user_id))
        conn.commit()


@retry_query(tries=3, delay=1)
def add_role_permission(role_id, permission_id):
    """Add permission to role.
    :params: role_id - id of role
             permission_id - id of permission
    """
    with db_pool().manager() as conn:
        cursor = conn.cursor()
        query = """INSERT INTO `role_permission` (`role_id`,
                                                  `permission_id`)
                   VALUES (%s, %s);
                """
        cursor.execute(query, (role_id, permission_id))
        conn.commit()


@retry_query(tries=3, delay=1)
def get_role_permission(role_id):
    """Get all permission of role.
       :params: role_id - id of role
       :return: tuple, containing tuples with permission id,
                action, modifier and description
    """
    with db_pool().manager() as conn:
        cursor = conn.cursor()
        query = """SELECT p.id, p.action, p.modifier, p.description
                   FROM `role_permission` AS rp
                   LEFT JOIN `permission` AS p  ON rp.permission_id=p.id
                   WHERE `role_id`=%s;
                """
        cursor.execute(query, (role_id,))
        return cursor.fetchall()


@retry_query(tries=3, delay=1)
def delete_permissions_by_role_id(role_id):
    """Deletes all permissions from role_permission table by role_id.
    :params: role_id - id of role
    """
    with db_pool().manager() as conn:
        cursor = conn.cursor()
        query = """DELETE `role_permission` FROM `role_permission`
                   WHERE `role_id`=%s;
                """
        cursor.execute(query, (role_id,))
        conn.commit()


@retry_query(tries=3, delay=1)
def check_resource_deletion(res_id):
    """Serching connection with parent table 'permission'
        if match found abort entering to DB
        if match not found deleting resource
        :params: res_id = key for searching in parent table 'permission'
        :return: tuple, empty if not found
    """
    with db_pool().manager() as conn:
        cursor = conn.cursor()
        query = """SELECT `resource_id` FROM `permission`
                   WHERE `resource_id`=%s;
                """
        cursor.execute(query, (res_id,))
        return cursor.fetchall()


@retry_query(tries=3, delay=1)
def delete_resource_by_id(res_id):
    """delete resource in db.
    :params: res_id - key for searching resource name in DB for deleting
    """
    with db_pool().manager() as conn:
        cursor = conn.cursor()
        query = """DELETE FROM `resource` WHERE `id`=%s;"""
        cursor.execute(query, (res_id,))
        conn.commit()


@retry_query(tries=3, delay=1)
def check_permission_deletion(permission_id):
    """Serching connection with parent table 'role_permission'
        if match found abort entering to DB
        if match not found deleting permission row
        :params: permission_id = key for searching in parent table
                                 'role_permission'
        :return: tuple, empty if not found
    """
    with db_pool().manager() as conn:
        cursor = conn.cursor()
        query = """SELECT `permission_id` FROM `role_permission`
                   WHERE `permission_id`=%s;
                """
        cursor.execute(query, (permission_id,))
        return cursor.fetchall()


@retry_query(tries=3, delay=1)
def delete_permission_by_id(permission_id):
    """Delete permission row in db.
    :params: permission_id - key for searching resource name in DB for deleting
    """
    with db_pool().manager() as conn:
        cursor = conn.cursor()
        query = """DELETE FROM `permission` WHERE `id`=%s;"""
        cursor.execute(query, (permission_id,))
        conn.commit()


@retry_query(tries=3, delay=1)
def check_role_deletion(role_id):
    """Serching connection with parent table 'role_permission'
        if match found abort entering to DB
        if match not found deleting role
        :params: role_id = key for searching in table 'role_permission'
        :return: tuple, empty if not found
    """
    with db_pool().manager() as conn:
        cursor = conn.cursor()
        query = """SELECT `role_id` FROM `role_permission`
                   WHERE `role_id`=%s;
                """
        cursor.execute(query, (role_id,))
        return cursor.fetchall()


@retry_query(tries=3, delay=1)
def delete_role_by_id(role_id):
    """Delete role name in db.
    :params: role_id - key for searching resource name in DB for deleting
    """
    with db_pool().manager() as conn:
        cursor = conn.cursor()
        query = """DELETE FROM `role` WHERE `id`=%s;"""
        cursor.execute(query, (role_id,))
        conn.commit()


@retry_query(tries=3, delay=1)
def get_pages_titles():
    """This method retrieves brief info from db
       about all pages(ex-resources).
    """
    with db_pool().manager() as conn:
        cursor = conn.cursor()
        query = """SELECT `id`, `title`, `alias`, `is_enabled` FROM `page`;"""
        cursor.execute(query)
        return cursor.fetchall()


@retry_query(tries=3, delay=1)
def get_page_by_alias(alias):
    """This method retrieves all info about exact
       page from db via it's alias.
       :returns tuple with data.
    `"""
    with db_pool().manager() as conn:
        cursor = conn.cursor()
        query = """SELECT `id`, `title`, `alias`, `description`, `content`,
                   `meta_keywords`, `meta_description`, `is_enabled`
                   FROM `page`
                   WHERE `alias`=%s;
                """
        cursor.execute(query, (alias,))
        return cursor.fetchone()


@retry_query(tries=3, delay=1)
def edit_page(page_id, title, alias, descr, content,
              meta_key, meta_descr, is_enabled):
    """Updates page(ex-resource).
       :params: page_id - id of pafe
                title - new title
                alias - new alias
                descr - new description
                content - new content
                meta_key - new meta keywords
                meta_descr - new meta_description
                is_enabled - changed view option
    """
    with db_pool().manager() as conn:
        cursor = conn.cursor()
        query = """UPDATE `page`
                   SET `title`=%s, `alias`=%s,
                   `description`=%s, `content`=%s,
                   `meta_keywords`=%s, `meta_description`=%s,
                   `is_enabled`=%s
                   WHERE `id`=%s;
                """
        cursor.execute(query, (title, alias, descr, content,
                               meta_key, meta_descr, is_enabled, page_id))
        conn.commit()


@retry_query(tries=3, delay=1)
def add_page(title, alias, descr, content,
             meta_key, meta_descr, is_enabled):
    """This method adds page(ex-resource) into db.
       :params: title - new title
                alias - new alias
                descr - new description
                content - new content
                meta_key - new meta keywords
                meta_descr - new meta_description
                is_enabled - changed view option
    """
    with db_pool().manager() as conn:
        cursor = conn.cursor()
        query = """INSERT INTO `page` (`title`, `alias`, `description`,
                                       `content`, `meta_keywords`,
                                       `meta_description`, `is_enabled`)
                   VALUES (%s, %s, %s, %s, %s, %s, %s);
                """
        cursor.execute(query, (title, alias, descr, content,
                               meta_key, meta_descr, is_enabled))
        conn.commit()


@retry_query(tries=3, delay=1)
def delete_page_by_id(page_id):
    """This method deletes page by it's id from db.
       :params: id - id of the page, which needs to be
       deleted.
    """
    with db_pool().manager() as conn:
        cursor = conn.cursor()
        query = """DELETE FROM `page` WHERE `id`=%s;"""
        cursor.execute(query, (page_id,))
        conn.commit()


@retry_query(tries=3, delay=1)
def get_page_by_id(page_id):
    """This method retrieves all info about exact
       page from db via it's id.
       :returns tuple with data.
    """
    with db_pool().manager() as conn:
        cursor = conn.cursor()
        query = """SELECT `id`, `title`, `alias`, `description`, `content`,
                   `meta_keywords`, `meta_description`, `is_enabled`
                   FROM `page`
                   WHERE `id`=%s;
                """
        cursor.execute(query, (page_id,))
        return cursor.fetchone()


def get_all_users():
    """Return all registered users from db.
    :return: tuples with user info
    """
    with db_pool().manager() as conn:
        cursor = conn.cursor()
        query = """SELECT u.id, u.first_name, u.last_name, u.email, r.name
                   FROM  `user_role` as ur
                   INNER JOIN `user` as u ON ur.user_id = u.id
                   INNER JOIN `role` as r ON ur.role_id = r.id;
                """
        cursor.execute(query)
        return cursor.fetchall()


@retry_query(tries=3, delay=1)
def get_permission_control_data():
    """Gets resources with permissions and role_permissions.
    :return: list of permissions
    """
    with db_pool().manager() as conn:
        cursor = conn.cursor()
        sql = """SELECT r.name, res.resource_name, p.action, p.modifier
                FROM role_permission AS rp
                INNER JOIN role AS r ON rp.role_id = r.id
                INNER JOIN permission AS p ON rp.permission_id = p.id
                INNER JOIN resource AS res ON p.resource_id = res.id;"""
        cursor.execute(sql)
        return cursor.fetchall()


@retry_query(tries=3, delay=1)
def get_all_problems():
    """Return all problems in db.
    :return: tuple, containing all problems
    """
    with db_pool().manager() as conn:
        cursor = conn.cursor()
        query = """ SELECT `id`,`title`,`latitude`,`longtitude`,
                    `problem_type_id`,`status`,`created_date`
                    FROM `problem`;
                """
        cursor.execute(query)
        return cursor.fetchall()


@retry_query(tries=3, delay=1)
def get_problem_by_id(problem_id):
    """Return problem, found by id.
    :params: problem_id - id of problem which was selected
    :return: list with lists where located dictionary
    """
    with db_pool().manager() as conn:
        cursor = conn.cursor()
        query = """ SELECT `id`, `title`, `content`, `proposal`,
                `severity`, `status`, `latitude`,`longtitude`,
                `problem_type_id` FROM `problem` WHERE `id` = %s;
                """
        cursor.execute(query, (problem_id, ))
        return cursor.fetchone()


@retry_query(tries=3, delay=1)
def get_activity_by_problem_id(problem_id):
    """Return problem, found by id.
    :params: problem_id - id of problem which was selected
    :return: tuple with problem_activity info
    """
    with db_pool().manager() as conn:
        cursor = conn.cursor()
        query = """ SELECT `created_date`, `problem_id`, `user_id`,
                    `activity_type` FROM `problem_activity`
                    WHERE `problem_id` = %s;
                """
        cursor.execute(query, (problem_id, ))
        return cursor.fetchone()

@retry_query(tries=3, delay=1)
def get_users_pagination(offset, per_page):
    """Users per page
    """
    with db_pool().manager() as conn:
        cursor = conn.cursor()
        query = """SELECT u.id, u.first_name, u.last_name, u.email, r.name
                   FROM  `user_role` AS ur
                   INNER JOIN `user` AS u ON ur.user_id = u.id
                   INNER JOIN `role` AS r ON ur.role_id = r.id
                   ORDER BY `id` LIMIT %s,%s;
                """
        cursor.execute(query % (offset, per_page))
        return cursor.fetchall()


@retry_query(tries=3, delay=1)
def pagination_test(page, per_page):
    """Users per page
    """
    if page == 1:
        offset = 0
    else:
        offset = (page-1) * per_page

    with db_pool().manager() as conn:
        cursor = conn.cursor()
        query = """SELECT u.id, u.first_name, u.last_name, u.email, r.name
                   FROM  `user_role` AS ur
                   INNER JOIN `user` AS u ON ur.user_id = u.id
                   INNER JOIN `role` AS r ON ur.role_id = r.id
                   ORDER BY `id` LIMIT %s,%s;
                """
        cursor.execute(query % (offset, per_page))
        return cursor.fetchall()


@retry_query(tries=3, delay=1)
def count_users():
    """Users per page
    """
    with db_pool().manager() as conn:
        cursor = conn.cursor()
        query = """SELECT COUNT(*) FROM `user`;"""
        cursor.execute(query)
        return cursor.fetchone()
