"""This module contains functions for interacting with Database."""
from ecomap.db.db_pool import retry_query, pool_manager

ANONYMOUS_ID = "2"
READ_ONLY = 'ro'
READ_WRITE = 'rw'


@retry_query(tries=3, delay=1)
def get_user_by_email(email):
    """Return user, found by email.
    :params email: user email
    :retrun: tuple with user info
    """
    with pool_manager(READ_ONLY).manager() as conn:
        cursor = conn.cursor()
        query = """SELECT `id`, `first_name`, `last_name`, `nickname`,
                   `email`, `password`, `avatar`
                   FROM `user` WHERE `email`=%s;
                """
        cursor.execute(query, (email,))
        return cursor.fetchone()


@retry_query(tries=3, delay=1)
def get_user_by_nick_name(nickname):
    """Return user, found by nickname.
    :params nickname: user nickname
    :retrun: tuple with user info
    """
    with pool_manager(READ_ONLY).manager() as conn:
        cursor = conn.cursor()
        query = """SELECT `id`, `first_name`, `last_name`, `nickname`,
                   `email`, `password`, `avatar`
                   FROM `user` WHERE `nickname`=%s;
                """
        cursor.execute(query, (nickname,))
        return cursor.fetchone()


@retry_query(tries=3, delay=1)
def get_user_by_id(user_id):
    """Return user, found by id.
    :params user_id: id of user
    :return: tuple with user info
    """
    with pool_manager(READ_ONLY).manager() as conn:
        cursor = conn.cursor()
        query = """SELECT `id`, `first_name`, `last_name`, `nickname`,
                   `email`, `password`, `avatar`
                   FROM `user` WHERE `id`=%s;
                """
        cursor.execute(query, (user_id,))
        return cursor.fetchone()


def get_user_by_nickname(nickname, offset, per_page):
    """Return information about creation problem by user, found by nickname.
    :params nickname: user nickname.
    :retrun: tuple with user and problem info.
    """
    with pool_manager(READ_ONLY).manager() as conn:
        cursor = conn.cursor()
        query = """SELECT p.id, p.title, p.status,
                   p.created_date, p.is_enabled,
                   p.severity, u.nickname,
                   u.last_name, u.first_name, pt.name
                   FROM `problem` AS p
                   INNER JOIN `problem_type` AS pt ON p.problem_type_id=pt.id
                   INNER JOIN `user` AS u ON p.user_id = u.id
                   WHERE u.nickname LIKE '%{}%' LIMIT {},{};
                """
        cursor.execute(query.format(nickname, offset, per_page))
        return cursor.fetchall()


def count_user_by_nickname(nickname):
    """Count of problems created by user with special nickname.
    :return: count of problems.
    """
    with pool_manager(READ_ONLY).manager() as conn:
        cursor = conn.cursor()
        query = """SELECT count(p.id)
                   FROM `problem` AS p
                   INNER JOIN `user` AS u ON p.user_id = u.id
                   WHERE u.nickname LIKE '%{}%';
                """
        cursor.execute(query.format(nickname))
        return cursor.fetchone()


@retry_query(tries=3, delay=1)
def get_user_by_oauth_id(user_id):
    """Return user, found by id.
    :params user_id: id of user
    :return: tuple with user info
    """
    with pool_manager(READ_ONLY).manager() as conn:
        cursor = conn.cursor()
        query = """SELECT `id`, `first_name`, `last_name`,
                   `nickname`, `email`, `password`
                   FROM `user` WHERE `oauth_uid`=%s;
                """
        cursor.execute(query, (user_id,))
        return cursor.fetchone()


@retry_query(tries=3, delay=1)
def add_oauth_to_user(user_id, oauth_provider, oauth_uid):
    """Adds oauth id and provider name to user.
       This grants authentication within oauth to user.
       :params user_id: id of user
       :params oauth_provider: provider name
       :params oauth_uid: user id from provider
    """
    with pool_manager(READ_WRITE).transaction() as conn:
        query = """UPDATE `user` SET `oauth_provider`=%s,
                   `oauth_uid`=%s WHERE `id`=%s;
                """
        conn.execute(query, (oauth_provider, oauth_uid, user_id))


@retry_query(tries=3, delay=1)
def facebook_insert(first_name, last_name, nickname, email, password,
                    provider, uid):
    """Adds new user into db through facebook.
    :params: first_name - first name of user
             last_name - last name of user
             nickname - nickname of user
             email - email of user
             password - hashed password of user
    """
    with pool_manager(READ_WRITE).transaction() as conn:
        query = """INSERT INTO `user` (`first_name`,
                                       `last_name`,
                                       `nickname`,
                                       `email`,
                                       `password`,
                                       `oauth_provider`,
                                       `oauth_uid`)
                   VALUES (%s, %s, %s, %s, %s, %s, %s);
                """
        conn.execute(query, (first_name, last_name, nickname, email, password,
                               provider, uid))
        registered_user_id = conn.lastrowid
        return registered_user_id


@retry_query(tries=3, delay=1)
def insert_user(first_name, last_name, nickname, email, password):
    """Adds new user into db.
    :params: first_name - first name of user
             last_name - last name of user
             email - email of user
             password - hashed password of user
    """
    with pool_manager(READ_WRITE).transaction() as conn:
        query = """INSERT INTO `user` (`first_name`,
                                       `last_name`,
                                       `nickname`,
                                       `email`,
                                       `password`)
                   VALUES (%s, %s, %s, %s ,%s);
                """
        conn.execute(query, (first_name, last_name, nickname, email, password))
        registered_user_id = conn.lastrowid
        return registered_user_id


@retry_query(tries=3, delay=1)
def add_users_role(user_id, role_id):
    """Adds to recenty registered user role "User".
    :params: user_id - id of recenty created user
             role_id - default is "User"
    """
    with pool_manager(READ_WRITE).transaction() as conn:
        query = """INSERT INTO `user_role` (`user_id`, `role_id`)
                   VALUES (%s, %s);
                """
        conn.execute(query, (user_id, role_id))


@retry_query(tries=3, delay=1)
def get_role_id(name='user'):
    """Gets role id by it's name.
       :params: name - name of role, default - 'user'
       :return: tuple with id of role
    """
    with pool_manager(READ_ONLY).manager() as conn:
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
    with pool_manager(READ_ONLY).manager() as conn:
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
    with pool_manager(READ_WRITE).transaction() as conn:
        query = """UPDATE `user` SET `avatar`=%s WHERE id=%s;"""
        conn.execute(query, (img_path, user_id))


@retry_query(tries=3, delay=1)
def delete_user_avatar(user_id):
    """Deletes user profile photo from db.
    :params: user_id - unique id user
    """
    with pool_manager(READ_WRITE).transaction() as conn:
        query = """UPDATE `user` SET `avatar`='' WHERE `id`=%s;"""
        conn.execute(query, (user_id,))


@retry_query(tries=3, delay=1)
def change_user_password(user_id, new_password):
    """Change password to user account.
    :params: new_password - new password
             user_id - id of user
    """
    with pool_manager(READ_WRITE).transaction() as conn:
        query = """UPDATE `user` SET `password`=%s WHERE `id`=%s;"""
        conn.execute(query, (new_password, user_id))


@retry_query(tries=3, delay=1)
def change_user_nickname(user_id, new_nickname):
    """Change user's nickname.
    :params: new_nickname - new nickname
             user_id - id of user
    """
    with pool_manager(READ_WRITE).transaction() as conn:
        query = """UPDATE `user` SET `nickname`=%s WHERE `id`=%s;"""
        conn.execute(query, (new_nickname, user_id))


@retry_query(tries=3, delay=1)
def get_user_role_by_email(email):
    """Get all resources.
    :return: tuple of resources
    """
    with pool_manager(READ_ONLY).manager() as conn:
        cursor = conn.cursor()
        query = """SELECT r.name FROM `user_role` AS ur
                   INNER JOIN `user` AS u ON ur.user_id=u.id
                   INNER JOIN `role` AS r ON ur.role_id=r.id
                   WHERE u.email=%s;
                """
        cursor.execute(query, (email,))
        return cursor.fetchone()


@retry_query(tries=3, delay=1)
def get_all_permissions_by_role():
    """This query created for Restriction class.
    Restriction class is for lesser entering to DB.
    """
    with pool_manager(READ_ONLY).manager() as conn:
        cursor = conn.cursor()
        query = """SELECT r.name, res.resource_name, p.action, p.modifier
                   FROM `role_permission` AS rp INNER JOIN `permission` AS p ON
                   rp.permission_id=p.id INNER JOIN `role` AS r
                   ON rp.role_id=r.id INNER JOIN `resource` AS res
                   ON p.resource_id=res.id;
                """
        cursor.execute(query)
    return cursor.fetchall()


@retry_query(tries=3, delay=1)
def get_user_role_by_id(user_id):
    """Get all resources.
    :return: tuple of resources
    """
    with pool_manager(READ_ONLY).manager() as conn:
        cursor = conn.cursor()
        query = """SELECT r.name FROM `role` AS r
                   INNER JOIN `user_role` AS ur ON r.id=ur.role_id
                   WHERE ur.user_id=%s;
                """
        cursor.execute(query, (user_id,))
        return cursor.fetchone()


@retry_query(tries=3, delay=1)
def get_all_resources(offset, per_page):
    """Get all resources.
    :return: tuple of resources
    """
    with pool_manager(READ_ONLY).manager() as conn:
        cursor = conn.cursor()
        query = """SELECT `id`, `resource_name` FROM `resource`
                   ORDER BY `id` LIMIT %s,%s;"""
        cursor.execute(query % (offset, per_page))
        return cursor.fetchall()


@retry_query(tries=3, delay=1)
def get_resource_id(resource_name):
    """Gets resource id.
    :params: resource_name - name of resource
    :return: tuple, containing id
    """
    with pool_manager(READ_ONLY).manager() as conn:
        cursor = conn.cursor()
        query = """SELECT `id` FROM `resource` WHERE `resource_name`=%s;"""
        cursor.execute(query, (resource_name,))
        return cursor.fetchone()


@retry_query(tries=3, delay=1)
def add_resource(resource_name):
    """Adds new resource in db.
    :params: resource_name - name of new resource
    """
    with pool_manager(READ_WRITE).transaction() as conn:
        query = """INSERT INTO `resource` (`resource_name`)
                   VALUES (%s);
                """
        conn.execute(query, (resource_name,))


@retry_query(tries=3, delay=1)
def edit_resource_name(new_resource_name, resource_id):
    """Edit resource name.
    :params: new_resource_name - new name of resource
             resource_id - id of  resource we change name
    """
    with pool_manager(READ_WRITE).transaction() as conn:
        query = """UPDATE `resource` SET `resource_name`=%s
                   WHERE `id`=%s;
                """
        conn.execute(query, (new_resource_name, resource_id))


@retry_query(tries=3, delay=1)
def get_all_roles():
    """Return all roles in db.
    :return: tuple, containing all roles
    """
    with pool_manager(READ_ONLY).manager() as conn:
        cursor = conn.cursor()
        query = """SELECT `id`, `name` FROM `role`;"""
        cursor.execute(query)
        return cursor.fetchall()


@retry_query(tries=3, delay=1)
def insert_role(role_name):
    """Insert new role into db.
    :params: role_name - name of role
    """
    with pool_manager(READ_WRITE).transaction() as conn:
        query = """INSERT INTO `role` (`name`) VALUES (%s);"""
        conn.execute(query, (role_name,))


@retry_query(tries=3, delay=1)
def edit_role(new_role_name, role_id):
    """Edit role name.
    :params: role_name - new name of role
             role_id - if of role
    """
    with pool_manager(READ_WRITE).transaction() as conn:
        query = """UPDATE `role` SET `name`=%s WHERE `id`=%s;"""
        conn.execute(query, (new_role_name, role_id))


@retry_query(tries=3, delay=1)
def get_all_permissions_by_resource(resource_id):
    """Find all permissions by resource.
    :params: resource_id - id of resource
    :return: tuple, containing permissions
    """
    with pool_manager(READ_ONLY).manager() as conn:
        cursor = conn.cursor()
        query = """SELECT `id`, `action`, `modifier`, `description`
                   FROM `permission` WHERE `resource_id`=%s;
                """
        cursor.execute(query, (resource_id,))
        return cursor.fetchall()


@retry_query(tries=3, delay=1)
def get_all_permissions(offset, per_page):
    """Find all permissions by resource.
    :params: - offset - pagination option
             - per_page - pagination option
    :return: tuple, containing permissions
    """
    with pool_manager(READ_ONLY).manager() as conn:
        cursor = conn.cursor()
        query = """SELECT p.id, r.resource_name, p.action, p.modifier,
                   p.description
                   FROM `permission` as p
                   INNER JOIN `resource` as r
                   ON p.resource_id=r.id
                   GROUP BY `id` LIMIT %s,%s;
                """
        cursor.execute(query % (offset, per_page))
        return cursor.fetchall()


@retry_query(tries=3, delay=1)
def get_all_permission_list():
    """Find all permissions by resource.
    :params: resource_id - id of resource
    :return: tuple, containing permissions
    """
    with pool_manager(READ_ONLY).manager() as conn:
        cursor = conn.cursor()
        query = """SELECT p.id, r.resource_name, p.action, p.modifier,
                   p.description
                   FROM `permission` as p
                   INNER JOIN `resource` as r
                   ON p.resource_id=r.id
                """
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
    with pool_manager(READ_WRITE).transaction() as conn:
        query = """INSERT INTO `permission` (`resource_id`,
                                             `action`,
                                             `modifier`,
                                             `description`)
                   VALUES (%s, %s, %s, %s);
                """
        conn.execute(query, (resource_id, action, modifier, description))


@retry_query(tries=3, delay=1)
def edit_permission(action, modifier, permission_id, description):
    """Edit permission.
    :params: action - action (POST, GET, DELETE, PUT)
             modifier - modifier (Own, Any, None)
             permission_id - if of permission we want to update
             description - short description to this permission
    """
    with pool_manager(READ_WRITE).transaction() as conn:
        query = """UPDATE `permission` SET `description`=%s, `action`=%s,
                   `modifier`=%s WHERE `id`=%s;
                """
        conn.execute(query, (description, action, modifier, permission_id))


@retry_query(tries=3, delay=1)
def get_permission_id(resource_id, action, modifier):
    """Return permission id.
    :params: resource_id - id of resource
             action - action (POST, GET, DELETE, PUT)
             modifier - modifier (Own, Any, None)
    :return: tuple, containing permission id"""
    with pool_manager(READ_ONLY).manager() as conn:
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
    with pool_manager(READ_WRITE).transaction() as conn:
        query = """INSERT INTO `user_role` (`user_id`,
                                            `role_id`)
                   VALUES (%s, %s);
                """
        conn.execute(query, (user_id, role_id))


@retry_query(tries=3, delay=1)
def change_user_role(role_id, user_id):
    """Update users role.
    :params: user_id - id of user
             role_id - id of role
    """
    with pool_manager(READ_WRITE).transaction() as conn:
        query = """UPDATE `user_role` SET `role_id`=%s WHERE `user_id`=%s;"""
        conn.execute(query, (role_id, user_id))


@retry_query(tries=3, delay=1)
def add_role_permission(role_id, permission_id):
    """Add permission to role.
    :params: role_id - id of role
             permission_id - id of permission
    """
    with pool_manager(READ_WRITE).transaction() as conn:
        query = """INSERT INTO `role_permission` (`role_id`,
                                                  `permission_id`)
                   VALUES (%s, %s);
                """
        conn.execute(query, (role_id, permission_id))


@retry_query(tries=3, delay=1)
def get_role_permission(role_id):
    """Get all permission of role.
       :params: role_id - id of role
       :return: tuple, containing tuples with permission id,
                action, modifier and description
    """
    with pool_manager(READ_ONLY).manager() as conn:
        cursor = conn.cursor()
        query = """SELECT p.id, p.action, p.modifier, p.description
                   FROM `role_permission` AS rp
                   LEFT JOIN `permission` AS p  ON rp.permission_id= p.id
                   WHERE `role_id`=%s;
                """
        cursor.execute(query, (role_id,))
        return cursor.fetchall()


@retry_query(tries=3, delay=1)
def delete_permissions_by_role_id(role_id):
    """Deletes all permissions from role_permission table by role_id.
    :params: role_id - id of role
    """
    with pool_manager(READ_WRITE).transaction() as conn:
        query = """DELETE `role_permission` FROM `role_permission`
                   WHERE `role_id`=%s;
                """
        conn.execute(query, (role_id,))


@retry_query(tries=3, delay=1)
def check_resource_deletion(res_id):
    """Serching connection with parent table 'permission'
        if match found abort entering to DB
        if match not found deleting resource
        :params: res_id = key for searching in parent table 'permission'
        :return: tuple, empty if not found
    """
    with pool_manager(READ_ONLY).manager() as conn:
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
    with pool_manager(READ_WRITE).transaction() as conn:
        query = """DELETE FROM `resource` WHERE `id`=%s;"""
        conn.execute(query, (res_id,))


@retry_query(tries=3, delay=1)
def check_permission_deletion(permission_id):
    """Serching connection with parent table 'role_permission'
        if match found abort entering to DB
        if match not found deleting permission row
        :params: permission_id = key for searching in parent table
                                 'role_permission'
        :return: tuple, empty if not found
    """
    with pool_manager(READ_ONLY).manager() as conn:
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
    with pool_manager(READ_WRITE).transaction() as conn:
        query = """DELETE FROM `permission` WHERE `id`=%s;"""
        conn.execute(query, (permission_id,))


@retry_query(tries=3, delay=1)
def check_role_deletion(role_id):
    """Serching connection with parent table 'role_permission'
        if match found abort entering to DB
        if match not found deleting role
        :params: role_id = key for searching in table 'role_permission'
        :return: tuple, empty if not found
    """
    with pool_manager(READ_ONLY).manager() as conn:
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
    with pool_manager(READ_WRITE).transaction() as conn:
        query = """DELETE FROM `role` WHERE `id`=%s;"""
        conn.execute(query, (role_id,))


@retry_query(tries=3, delay=1)
def get_pages_titles():
    """This method retrieves brief info from db
       about all pages(ex-resources).
    """
    with pool_manager(READ_ONLY).manager() as conn:
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
    with pool_manager(READ_ONLY).manager() as conn:
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
    with pool_manager(READ_WRITE).transaction() as conn:
        query = """UPDATE `page`
                   SET `title`=%s, `alias`=%s,
                   `description`=%s, `content`=%s,
                   `meta_keywords`=%s, `meta_description`=%s,
                   `is_enabled`=%s
                   WHERE `id`=%s;
                """
        conn.execute(query, (title, alias, descr, content,
                               meta_key, meta_descr, is_enabled, page_id))


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
    with pool_manager(READ_WRITE).transaction() as conn:
        query = """INSERT INTO `page` (`title`, `alias`, `description`,
                                       `content`, `meta_keywords`,
                                       `meta_description`, `is_enabled`)
                   VALUES (%s, %s, %s, %s, %s, %s, %s);
                """
        conn.execute(query, (title, alias, descr, content,
                               meta_key, meta_descr, is_enabled))


@retry_query(tries=3, delay=1)
def delete_page_by_id(page_id):
    """This method deletes page by it's id from db.
       :params: id - id of the page, which needs to be
       deleted.
    """
    with pool_manager(READ_WRITE).transaction() as conn:
        query = """DELETE FROM `page` WHERE `id`=%s;"""
        conn.execute(query, (page_id,))


@retry_query(tries=3, delay=1)
def get_page_by_id(page_id):
    """This method retrieves all info about exact
       page from db via it's id.
       :returns tuple with data.
    """
    with pool_manager(READ_ONLY).manager() as conn:
        cursor = conn.cursor()
        query = """SELECT `id`, `title`, `alias`, `description`, `content`,
                   `meta_keywords`, `meta_description`, `is_enabled`
                   FROM `page`
                   WHERE `id`=%s;
                """
        cursor.execute(query, (page_id,))
        return cursor.fetchone()


@retry_query(tries=3, delay=1)
def get_all_users():
    """Return all registered users from db.
    :return: tuples with user info
    """
    with pool_manager(READ_ONLY).manager() as conn:
        cursor = conn.cursor()
        query = """SELECT u.id, u.first_name, u.last_name, u.email, r.name
                   FROM  `user_role` as ur
                   INNER JOIN `user` as u ON ur.user_id=u.id
                   INNER JOIN `role` as r ON ur.role_id=r.id;
                """
        cursor.execute(query)
        return cursor.fetchall()


@retry_query(tries=3, delay=1)
def get_permission_control_data():
    """Gets resources with permissions and role_permissions.
    :return: list of permissions
    """
    with pool_manager(READ_ONLY).manager() as conn:
        cursor = conn.cursor()
        sql = """SELECT r.name, res.resource_name, p.action, p.modifier
                 FROM role_permission AS rp
                 INNER JOIN role AS r ON rp.role_id=r.id
                 INNER JOIN permission AS p ON rp.permission_id=p.id
                 INNER JOIN resource AS res ON p.resource_id=res.id;
              """
        cursor.execute(sql)
        return cursor.fetchall()


@retry_query(tries=3, delay=1)
def get_users_pagination(offset, per_page):
    """Users per page
    """
    with pool_manager(READ_ONLY).manager() as conn:
        cursor = conn.cursor()
        query = """SELECT u.id, u.first_name, u.last_name, u.nickname, u.email, r.name
                   FROM  `user_role` AS ur
                   INNER JOIN `user` AS u ON ur.user_id=u.id
                   INNER JOIN `role` AS r ON ur.role_id=r.id
                   ORDER BY `id` LIMIT %s,%s;
                """
        cursor.execute(query % (offset, per_page))
        return cursor.fetchall()


@retry_query(tries=3, delay=1)
def count_users():
    """Users per page
    """
    with pool_manager(READ_ONLY).manager() as conn:
        cursor = conn.cursor()
        query = """SELECT COUNT(*) FROM `user`;"""
        cursor.execute(query)
        return cursor.fetchone()


@retry_query(tries=3, delay=1)
def get_all_problems():
    """Return all problems in db.
    :return: tuple, containing all problems
    """
    with pool_manager(READ_ONLY).manager() as conn:
        cursor = conn.cursor()
        query = """SELECT problem.id, title, latitude, longitude,
                   problem_type_id, status, created_date, problem_type.radius,
                   problem_type.picture
                   FROM `problem` INNER JOIN `problem_type`
                   ON problem.problem_type_id = problem_type.id;
                """
        cursor.execute(query)
        return cursor.fetchall()


@retry_query(tries=3, delay=1)
def get_user_problems(user_id, offset, per_page):
    """Gets all problems posted by given user."""
    with pool_manager(READ_ONLY).manager() as conn:
        cursor = conn.cursor()
        query = """SELECT p.id, p.title, p.latitude, p.longitude,
                   p.problem_type_id, p.status, p.created_date, p.is_enabled,
                   p.severity, pt.name
                   FROM `problem` AS p
                   INNER JOIN `problem_type` AS pt ON p.problem_type_id=pt.id
                   WHERE `user_id`=%s LIMIT %s,%s;
                """
        cursor.execute(query, (user_id, offset, per_page))
        return cursor.fetchall()

@retry_query(tries=3, delay=1)
def get_problem_by_id(problem_id):
    """Return problem, found by id.
    :params: problem_id - id of problem which was selected
    :return: list with lists where located dictionary
    """
    with pool_manager(READ_ONLY).manager() as conn:
        cursor = conn.cursor()
        query = """SELECT p.id, p.title, p.content, p.proposal,
                   p.severity, p.status, p.latitude,p.longitude,
                   p.problem_type_id, p.created_date, t.name
                   FROM `problem` AS p INNER JOIN `problem_type` AS t
                   ON p.problem_type_id=t.id
                   WHERE p.id=%s;
                """
        cursor.execute(query, (problem_id, ))
        return cursor.fetchone()


@retry_query(tries=3, delay=1)
def get_activity_by_problem_id(problem_id):
    """Return problem, found by id.
    :params: problem_id - id of problem which was selected
    :return: tuple with problem_activity info
    """
    with pool_manager(READ_ONLY).manager() as conn:
        cursor = conn.cursor()
        query = """SELECT `created_date`, `problem_id`, `user_id`,
                   `activity_type` FROM `problem_activity`
                   WHERE `problem_id`=%s;
                """
        cursor.execute(query, (problem_id, ))
        return cursor.fetchone()


@retry_query(tries=3, delay=1)
def problem_post(title, content, proposal, latitude, longitude,
                 problem_type_id, created_date, user_id):
    """This method adds problem into db.
       :params: title - new title
                content - new content
                proposal - new proposal
                latitude - new latitude of a new problem
                longitude - new longitude of a new problem
                problem_type_id - type of a new problem
    """
    with pool_manager(READ_WRITE).transaction() as conn:
        query = """INSERT INTO `problem`
                   (`title`, `content`, `proposal`, `latitude`, `longitude`,
                    `problem_type_id`,`created_date`, `user_id`)
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
                """
        conn.execute(query, (title, content, proposal, latitude,
                               longitude, problem_type_id, created_date,
                               user_id))
        last_id = conn.lastrowid
        return last_id


@retry_query(tries=3, delay=1)
def problem_activity_post(problem_id, created_date, user_id, act_type):
    """This method adds new problem_activity into db.
       :params: problem_id - id of problem
                created_date - time of problem creation
                user_id - id of user that posted problem
    """
    with pool_manager(READ_WRITE).transaction() as conn:
        query = """INSERT INTO `problem_activity`
                   (`problem_id`, `created_date`, `user_id`,
                    `activity_type`)
                   VALUES (%s, %s, %s, %s);
                """
        conn.execute(query, (problem_id, created_date, user_id, act_type))


@retry_query(tries=3, delay=1)
def get_id_problem_owner(problem_id):
    """Return problem, found by id.
    :params: problem_id - id of problem which was selected
    :return: tuple with problem_activity info
    """
    with pool_manager(READ_ONLY).manager() as conn:
        cursor = conn.cursor()
        query = """SELECT `created_date`, `problem_id`, `user_id`,
                   `activity_type` FROM `problem_activity`
                   WHERE `problem_id`=%s;
                """
        cursor.execute(query, (problem_id, ))
        return cursor.fetchone()


@retry_query(tries=3, delay=1)
def add_problem_photo(problem_id, photo_url, photo_descr, user_id):
    """Adds a link for added problem photo into db.
    :param problem_id:
    :param photo_url:
    :param photo_descr:
    :param user_id:
    :return:
    """
    with pool_manager(READ_WRITE).transaction() as conn:
        query = """INSERT INTO `photo`
                   (`name`, `description`, `problem_id`, user_id)
                   VALUES (%s, %s, %s, %s);
                """
        conn.execute(query, (photo_url, photo_descr, problem_id, user_id))


@retry_query(tries=3, delay=1)
def get_problem_photos(problem_id):
    """Gets all photos posted by user to problem."""
    with pool_manager(READ_ONLY).manager() as conn:
        cursor = conn.cursor()
        query = """SELECT `name`, `description`, `user_id`
                   FROM `photo` WHERE `problem_id`=%s;
                """
        cursor.execute(query, (problem_id,))
        return cursor.fetchall()


@retry_query(tries=3, delay=1)
def get_problem_owner(problem_id):
    """Gets all photos posted by user to problem."""
    with pool_manager(READ_ONLY).manager() as conn:
        cursor = conn.cursor()
        query = """SELECT `user_id` FROM `problem` WHERE `id`=%s;"""
        cursor.execute(query, (problem_id,))
        return cursor.fetchone()


@retry_query(tries=3, delay=1)
def insert_into_restore_password(hashed, user_id, create_time):
    """Inserts info restore_password table new line."""
    with pool_manager(READ_WRITE).transaction() as conn:
        query = """INSERT INTO `user_operation` (`creation_date`,
                                                   `hash_sum`,
                                                   `user_id`,
                                                   `type`)
                   VALUES (%s, %s, %s, 'password');
                """
        conn.execute(query, (create_time, hashed, user_id))


@retry_query(tries=3, delay=1)
def insert_into_hash_delete(hex_hash, user_id, create_time):
    """Inserts into user_operation table new line."""
    with pool_manager(READ_WRITE).transaction() as conn:
        query = """INSERT INTO `user_operation`(`creation_date`,
                                                  `hash_sum`,
                                                  `user_id`,
                                                  `type`)
                    VALUES (%s, %s, %s, 'delete');
                """
        conn.execute(query, (create_time, hex_hash, user_id))


@retry_query(tries=3, delay=1)
def check_hash_in_db(hashed):
    """Returns restore password request time.
       :params: hashed - hash sum
       :return: time
    """
    with pool_manager(READ_ONLY).manager() as conn:
        cursor = conn.cursor()
        query = """SELECT `creation_date`
                   FROM `user_operation`
                   WHERE `hash_sum`=%s;
                """
        cursor.execute(query, (hashed,))
        return cursor.fetchone()


@retry_query(tries=3, delay=3)
def restore_password(user_id, password):
    """Updates user password.
       :params: user_id - user id
                password - new password
    """
    with pool_manager(READ_WRITE).transaction() as conn:
        query = """UPDATE `user` SET `password`=%s
                   WHERE `id`=%s;
                """
        conn.execute(query, (password, user_id))


@retry_query(tries=3, delay=1)
def get_user_id_by_hash(hash_sum):
    """Get user id by hash sum from restore password table.
       :params: hash_sum - hash sum
       :return: user id
    """
    with pool_manager(READ_ONLY).manager() as conn:
        cursor = conn.cursor()
        query = """SELECT `user_id` FROM `user_operation`
                   WHERE `hash_sum`=%s;
                """
        cursor.execute(query, (hash_sum,))
        return cursor.fetchone()


@retry_query(tries=3, delay=1)
def get_hash_data(startime, endtime):

    """
    Gets statistic info from db about user's change password activity during
    the last 24hours or any specified date between 2 timestamp objects.
    :return: tuple(creation_time(timestamp), user_name, user_email, number
             of change tries)

    """
    with pool_manager(READ_ONLY).manager() as conn:
        cursor = conn.cursor()
        query = """SELECT  p.creation_date, u.first_name, u.email, count(u.id)
                   FROM `user_operation` AS p
                   INNER JOIN `user` AS u ON p.user_id = u.id
                   WHERE p.creation_date BETWEEN %d AND %d
                   AND p.type = 'password'
                   GROUP BY u.id;
                """
        cursor.execute(query % (startime, endtime))
        return cursor.fetchall()


@retry_query(tries=3, delay=1)
def get_deletion_data(startime, endtime):

    """Gets statistic info from db about user's deletion profile activity
    during the last 24hours or any specified date between 2 timestamp objects.
    :return: tuple(creation_time(timestamp), user_name, user_email, number
             of tries)

    """
    with pool_manager(READ_ONLY).manager() as conn:
        cursor = conn.cursor()
        query = """SELECT  p.creation_date, u.first_name, u.email, count(u.id)
                   FROM `user_operation` AS p
                   INNER JOIN `user` AS u ON p.user_id = u.id
                   WHERE p.creation_date BETWEEN %d AND %d
                   AND p.type = 'delete'
                   GROUP BY u.id;
                """
        cursor.execute(query % (startime, endtime))
        return cursor.fetchall()


@retry_query(tries=3, delay=1)
def clear_password_hash(startime, endtime):
    """Deletes statistics info from db for defined time period.
    :return:
    """

    with pool_manager(READ_WRITE).transaction() as conn:
        query = """DELETE FROM `user_operation`
                   WHERE `creation_date` BETWEEN %d AND %d
                   AND `type` = 'password';
                """
        conn.execute(query % (startime, endtime))


@retry_query(tries=3, delay=1)
def clear_user_deletion_hash(startime, endtime):
    """Deletes statistics info from db for defined time period.
    :return:
    """

    with pool_manager(READ_WRITE).manager() as conn:
        query = """DELETE FROM `user_operation`
                   WHERE `creation_date` BETWEEN %d AND %d
                   AND `type` = 'delete';
                """
        conn.execute(query % (startime, endtime))


@retry_query(tries=3, delay=1)
def count_resources():
    """Users per page
    :return: count of user's problem per page
    """
    with pool_manager(READ_ONLY).manager() as conn:
        cursor = conn.cursor()
        query = """SELECT COUNT(id) FROM `resource`;"""
        cursor.execute(query)
        return cursor.fetchone()


@retry_query(tries=3, delay=1)
def count_permissions():
    """
    :return:
    """
    with pool_manager(READ_ONLY).manager() as conn:
        cursor = conn.cursor()
        query = """SELECT COUNT(p.id) FROM permission AS p
                   INNER JOIN resource AS r
                   ON p.resource_id = r.id"""
        cursor.execute(query)
        return cursor.fetchone()


@retry_query(tries=3, delay=1)
def get_all_users_problems(offset, per_page):
    """Function selects from db all problems created by user.
    :return: tuple with problem data.
    """
    with pool_manager(READ_ONLY).manager() as conn:
        cursor = conn.cursor()
        query = """SELECT p.id, p.title, p.latitude, p.longitude,
                   p.problem_type_id, p.status, p.created_date, p.is_enabled,
                   p.severity, u.last_name, u.first_name, u.nickname, pt.name
                   FROM `problem` AS p
                   INNER JOIN `user` AS u ON p.user_id = u.id
                   INNER JOIN `problem_type` AS pt ON p.problem_type_id=pt.id
                   GROUP BY p.id LIMIT %s,%s;
                """
        cursor.execute(query % (offset, per_page))
        return cursor.fetchall()


@retry_query(tries=3, delay=1)
def count_problems():
    """Count all problems from db.
    :return: count.
    """
    with pool_manager(READ_ONLY).manager() as conn:
        cursor = conn.cursor()
        query = """SELECT COUNT(id) FROM `problem`;
                """
        cursor.execute(query)
        return cursor.fetchone()


@retry_query(tries=3, delay=1)
def count_user_problems(user_id):
    """Count of user's problem.
    :return: count
    """
    with pool_manager(READ_ONLY).manager() as conn:
        cursor = conn.cursor()
        query = """SELECT COUNT(id) FROM `problem`
                where `user_id` =%s;"""
        cursor.execute(query, (user_id,))
        return cursor.fetchone()


@retry_query(tries=3, delay=1)
def add_comment(user_id, problem_id, parent_id, content, created_date):
    """Adds new comment to problem.
       :params: user_id - user id
                problem_id - id of problem
                parent_id - id of parent comment
                content - comment content
                created_date - create time
    """
    with pool_manager(READ_WRITE).transaction() as conn:
        query = """INSERT INTO `comment` (`user_id`, `problem_id`,
                                          `parent_id`, `content`,
                                          `created_date`)
                   VALUES (%s, %s, %s, %s, %s);
                """
        conn.execute(query, (user_id, problem_id, parent_id,
                               content, created_date))


@retry_query(tries=3, delay=1)
def get_comments_by_problem_id(problem_id):
    """Get all comments of problem.
       :params: problem_id - id of problem
       :return: tuple of comments (id, content, problem id,
                                   created date, user id,
                                   user first name, user last name)
    """
    with pool_manager(READ_ONLY).manager() as conn:
        cursor = conn.cursor()
        query = """SELECT c.id, c.content, c.problem_id, c.created_date,
                          c.user_id, u.nickname
                   FROM `comment` AS c LEFT JOIN `user` as u
                   ON c.user_id=u.id
                   WHERE c.problem_id=%s AND c.parent_id=0;
                """
        cursor.execute(query, (problem_id,))
        return cursor.fetchall()

@retry_query(tries=3, delay=1)
def get_subcomments_by_parent_id(parent_id):
    """Get all subcomments of parent comment.
       :params: parent_id - id of parent comment
       :return: tuple of comments (id, content, problem id,
                                   parent_id, created date, user id,
                                   user first name, user last name)
    """
    with pool_manager(READ_ONLY).manager() as conn:
        cursor = conn.cursor()
        query = """SELECT c.id, c.content, c.problem_id,
                          c.parent_id, c.created_date, c.user_id,
                          u.nickname, u.first_name, u.last_name
                   FROM `comment` AS c LEFT JOIN `user` as u
                   ON c.user_id=u.id
                   WHERE c.parent_id=%s;
                """
        cursor.execute(query, (parent_id,))
        return cursor.fetchall()

@retry_query(tries=3, delay=1)
def get_count_of_parent_subcomments(parent_id):
    """Get count of subcomments of parent comment.
       :params: parent_id - id of parent comment
       :return: count of subcomments
    """
    with pool_manager(READ_ONLY).manager() as conn:
        cursor = conn.cursor()
        query = """SELECT COUNT(id) FROM `comment`
                   WHERE parent_id=%s;
                """
        cursor.execute(query, (parent_id,))
        return cursor.fetchone()

@retry_query(tries=3, delay=1)
def get_user_comments_count(user_id):
    """Get count of user comments.
       :params: user_id - id of user
       :return: count of user comments
    """
    with pool_manager(READ_ONLY).manager() as conn:
        cursor = conn.cursor()
        query = """SELECT COUNT(id) FROM `comment`
            where `user_id` =%s;"""
        cursor.execute(query, (user_id,))
        return cursor.fetchone()


@retry_query(tries=3, delay=1)
def get_problem_id_for_del(user_id):
    """Query for selecting tuple with problem_id, when
    User profile have to delete.
    :return:tuple with problem_id
    """
    with pool_manager(READ_ONLY).manager() as conn:
        cursor = conn.cursor()
        query = """SELECT `id` FROM `problem` WHERE `user_id`=%s;"""
        cursor.execute(query, (user_id,))
        return cursor.fetchall()


@retry_query(tries=3, delay=1)
def change_problem_to_anon(problem_id):
    """Query for change user_id in problem table to id of Anonimus User,
    when we deleting User-owner of this problem.
    """
    with pool_manager(READ_WRITE).transaction() as conn:
        query = """UPDATE `problem` SET `user_id`=%s WHERE `id`=%s;"""
        conn.execute(query, (ANONYMOUS_ID, problem_id))


@retry_query(tries=3, delay=1)
def change_comments_to_anon(user_id):
    """Query for change user_id in comment table to id of Anonimus User,
    when we deleting User-owner of this comment.
    """
    with pool_manager(READ_WRITE).transaction() as conn:
        query = """UPDATE `comment` SET `user_id`=%s WHERE `user_id`=%s;"""
        conn.execute(query, (ANONYMOUS_ID, user_id))\


@retry_query(tries=3, delay=1)
def change_comment_by_id(comment_id, content):
    """Query for change content in comment table.
    """
    with pool_manager(READ_WRITE).transaction() as conn:
        query = """UPDATE `comment` SET `content`=%s WHERE `id`=%s;"""
        conn.execute(query, (content, comment_id))



@retry_query(tries=3, delay=1)
def change_comment_by_id(comment_id, content):
    """Query for change content in comment table.
    """
    with pool_manager(READ_WRITE).transaction() as conn:
        query = """UPDATE `comment` SET `content`=%s WHERE `id`=%s;"""
        conn.execute(query, (content, comment_id))


@retry_query(tries=3, delay=1)
def change_activity_to_anon(problem_id):
    """Query for change user_id in problem_activity
    table to id of Anonimus User,
    when we deleting User-owner of this problem.
    """
    with pool_manager(READ_WRITE).transaction() as conn:
        query = """UPDATE `problem_activity` SET `user_id`=%s
                    WHERE `problem_id`=%s;
                """
        conn.execute(query, (ANONYMOUS_ID, problem_id))


@retry_query(tries=3, delay=1)
def delete_user(user_id):
    """Deletes user_id by id from JSON.
    """
    with pool_manager(READ_WRITE).transaction() as conn:
        query = """DELETE FROM `user` WHERE id=%s;"""
        conn.execute(query, (user_id,))


@retry_query(tries=3, delay=1)
def get_problem_type():
    """Get problem type.
       :return: tuple with problem type name, picture and radius.
    """
    with pool_manager(READ_ONLY).manager() as conn:
        cursor = conn.cursor()
        query = """SELECT * FROM `problem_type`;"""
        cursor.execute(query)
        return cursor.fetchall()


@retry_query(tries=3, delay=1)
def get_problem_type_for_filtration():
    """Get problem type.
       :return: tuple with problem type name and id.
    """
    with pool_manager(READ_ONLY).manager() as conn:
        cursor = conn.cursor()
        query = """SELECT `id`, `picture`, `name` FROM `problem_type`;"""
        cursor.execute(query)
        return cursor.fetchall()


@retry_query(tries=3, delay=1)
def get_problems_by_type(problem_type_id):
    """Get problems by type.
       :return: tuple with problem type name and id.
    """
    with pool_manager(READ_ONLY).manager() as conn:
        cursor = conn.cursor()
        query = """SELECT p.id, p.title, p.latitude, p.longitude, p.problem_type_id,
                           p.status, p.created_date, p.is_enabled,
                           p.severity, pt.name, pt.radius
                           FROM problem AS p INNER JOIN problem_type AS pt ON
                           pt.id=p.problem_type_id WHERE pt.id=%s;"""
        cursor.execute(query, (problem_type_id))
        return cursor.fetchall()


@retry_query(tries=3, delay=1)
def get_problem_type_by_id(problem_type_id):
    """Get problem type.
       :params: problem_type_id - id of problem type.
       :return: tuple with problem type name, picture and radius.
    """
    with pool_manager(READ_ONLY).manager() as conn:
        cursor = conn.cursor()
        query = """SELECT * FROM `problem_type` WHERE `id`=%s;"""
        cursor.execute(query, (problem_type_id))
        return cursor.fetchall()


@retry_query(tries=3, delay=1)
def get_problem_type_by_name(problem_type_name):
    """Get problem type.
       :params: problem_type_name - name of problem type.
       :return: tuple with problem type and radius.
    """
    with pool_manager(READ_ONLY).manager() as conn:
        cursor = conn.cursor()
        query = """SELECT * FROM `problem_type` WHERE `name`=%s;"""
        cursor.execute(query, (problem_type_name))
        return cursor.fetchall()


@retry_query(tries=3, delay=1)
def get_problem_type_picture(problem_type_id):
    """Get problem type.
       :params: problem_type_id - id of problem type.
       :return: tuple with problem type picture.
    """
    with pool_manager(READ_ONLY).manager() as conn:
        cursor = conn.cursor()
        query = """SELECT `picture` FROM `problem_type` WHERE `id`=%s;"""
        cursor.execute(query, (problem_type_id))
        return cursor.fetchone()


@retry_query(tries=3, delay=1)
def delete_problem_type(problem_type_id):
    """Delete problem type.
       :params: problem_type_id - id of problem type.
    """
    with pool_manager(READ_WRITE).transaction() as conn:
        query = """DELETE FROM `problem_type`
                   WHERE `id`=%s;
                """
        conn.execute(query, (problem_type_id,))


@retry_query(tries=3, delay=1)
def update_problem_type(problem_type_id, picture, name, radius):
    """Update problem type.
       :params: problem_type_id - id of problem type,
                     picture - picture of problem type,
                     name - name of problem type,
                     radius - radius of problem type.
    """
    with pool_manager(READ_WRITE).transaction() as conn:
        query = """UPDATE `problem_type` SET `picture`=%s,
                                         `name`=%s, `radius`=%s
                          WHERE `id`=%s;
                      """
        conn.execute(query, (picture, name, radius, problem_type_id))


@retry_query(tries=3, delay=1)
def add_problem_type(picture, name, radius):
    """Insert problem type.
       :params: picture - picture of problem type,
                     name - name of problem type,
                     radius - radius of problem type.
    """
    with pool_manager(READ_WRITE).transaction() as conn:
        query = """INSERT  INTO `problem_type` (`picture`,
                                         `name`, `radius`)
                          VALUES (%s, %s, %s);
                      """
        conn.execute(query, (picture, name, radius))


@retry_query(tries=3, delay=1)
def get_subscription_by_user_id(user_id, problem_id):
    """Function retrieves user's subscriptions'.
    :param user_id: id of user (int)
    :param problem_id: id of problem (int)
    :return: tuple with user info.
    """
    with pool_manager(READ_ONLY).manager() as conn:
        cursor = conn.cursor()
        query = """SELECT * FROM `subscription`
                WHERE `user_id`=%s AND `problem_id`=%s;
                """
        cursor.execute(query, (user_id, problem_id))
        return cursor.fetchone()


@retry_query(tries=3, delay=1)
def check_exist_subscriptions(user_id, problem_id):
    """Function checks if there is some user's subscription into db.
    :return: true or false.
    """ 
    return bool(get_subscription_by_user_id(user_id, problem_id))


@retry_query(tries=3, delay=1)
def subscription_post(problem_id, user_id, date_subscriptions):
    """Function adds problem into db.
    :param user_id: id of user (int)
    :param problem_id: id of problem (int)
    :param date_subscriptions: date when user subscribed to a problem.
    """
    with pool_manager(READ_WRITE).transaction() as conn:
        if (check_exist_subscriptions(user_id, problem_id) == False):
            query = """INSERT INTO `subscription`
                       (`problem_id`, `user_id`, `date_subscriptions`)
                       VALUES (%s, %s, %s);
                    """
            conn.execute(query, (problem_id, user_id, date_subscriptions))
        last_id = conn.lastrowid
        return last_id


@retry_query(tries=3, delay=1)
def subscription_delete(user_id, problem_id):
    """Function deletes subscription from db.
    :param user_id: id of user (int)
    :param problem_id: id of problem (int).
    """
    with pool_manager(READ_WRITE).transaction() as conn:
        query = """DELETE FROM `subscription`                   
                   WHERE `user_id`=%s AND `problem_id`=%s;
                """
        conn.execute(query, (user_id, problem_id))
        last_id = conn.lastrowid


@retry_query(tries=3, delay=1)
def count_user_subscriptions(user_id):
    """Function counts user's subscriptions.
    :param user_id: id of user (int)
    :return: count.
    """
    with pool_manager(READ_ONLY).manager() as conn:
        cursor = conn.cursor()
        query = """SELECT COUNT(id) FROM `subscription`
                where `user_id` =%s;"""
        cursor.execute(query, (user_id,))
        return cursor.fetchone()


@retry_query(tries=3, delay=1)
def count_all_subscriptions():
    """Function counts user's subscriptions.
    :param user_id: id of user (int)
    :return: count.
    """
    with pool_manager(READ_ONLY).manager() as conn:
        cursor = conn.cursor()
        query = """SELECT COUNT(id) FROM `subscription`;"""
        cursor.execute(query)
        return cursor.fetchone()


@retry_query(tries=3, delay=1)
def get_subscriptions(user_id, offset, per_page):
    """Function retrieves all user's subscriptions from db.
    :param id: id of problem (int)
    :param title: title of problem ('problem with rivers')
    :param problem_type_id: id of problem type (int)
    :param status: status of problem (solved or unsolved)
    :param created_date: date when problem was creared
    :param date_subscriptions: date when user subscribed to a problem
    :return: tuples with user info.
    """
    with pool_manager(READ_ONLY).manager() as conn:
        cursor = conn.cursor()
        query = """SELECT pr.id, pr.title, pr.problem_type_id, pr.status,
                   pr.created_date, sub.date_subscriptions, pt.name
                   FROM  `subscription` as sub
                   INNER JOIN `problem` as pr ON sub.problem_id=pr.id
                   INNER JOIN `problem_type` AS pt ON pr.problem_type_id=pt.id
                   WHERE sub.user_id=%s LIMIT %s,%s;
                """
        cursor.execute(query, (user_id, offset, per_page))
        return cursor.fetchall()


@retry_query(tries=3, delay=1)
def get_all_subscriptions(offset, per_page):
    """Function retrieves all user's subscriptions from db.
    :param id: id of problem (int)
    :param title: title of problem ('problem with rivers')
    :param problem_type_id: id of problem type (int)
    :param status: status of problem (solved or unsolved)
    :param created_date: date when problem was creared
    :param date_subscriptions: date when user subscribed to a problem
    :return: tuples with user info.
    """
    with pool_manager(READ_ONLY).manager() as conn:
        cursor = conn.cursor()
        query = """SELECT pr.id, pr.title, pr.problem_type_id, pr.status,
                   pr.created_date, sub.date_subscriptions, pt.name,
                   u.last_name, u.first_name, u.nickname
                   FROM  `subscription` as sub
                   INNER JOIN `problem` as pr ON sub.problem_id=pr.id
                   INNER JOIN `problem_type` AS pt ON pr.problem_type_id=pt.id
                   INNER JOIN `user` AS u ON sub.user_id=u.id LIMIT %s,%s;
                """
        cursor.execute(query, (offset, per_page))
        return cursor.fetchall()


@retry_query(tries=3, delay=1)
def get_subscriptions_by_nickname(nickname, offset, per_page):
    """Function retrieves all user's subscriptions from db by nickname.
    :param nickname: nickname of problem.
    :param title: title of problem ('problem with rivers').
    :param problem_type_id: id of problem type (int).
    :param status: status of problem (solved or unsolved).
    :param created_date: date when problem was creared.
    :param date_subscriptions: date when user subscribed to a problem.
    :param last_name: user last_name.
    :param first_name: user first_name.
    :return: tuples with user info.
    """
    with pool_manager(READ_ONLY).manager() as conn:
        cursor = conn.cursor()
        query = """SELECT pr.id, pr.title, pr.problem_type_id, pr.status,
                   pr.created_date, sub.date_subscriptions, pt.name,
                   u.last_name, u.first_name, u.nickname
                   FROM  `subscription` as sub
                   INNER JOIN `problem` as pr ON sub.problem_id=pr.id
                   INNER JOIN `problem_type` AS pt ON pr.problem_type_id=pt.id
                   INNER JOIN `user` AS u ON sub.user_id=u.id
                   WHERE u.nickname LIKE '%{}%' LIMIT {},{};
                """
        cursor.execute(query.format(nickname, offset, per_page))
        return cursor.fetchall()


@retry_query(tries=3, delay=1)
def count_subscriptions_by_nickname(nickname):
    """Function counts user's subscriptions.
    :param nickname: nickname of user.
    :return: count.
    """
    with pool_manager(READ_ONLY).manager() as conn:
        cursor = conn.cursor()
        query = """SELECT COUNT(s.id)
                FROM `subscription`as s
                INNER JOIN `user` as u ON s.user_id=u.id
                WHERE u.nickname LIKE '%{}%';
                """
        cursor.execute(query.format(nickname))
        return cursor.fetchone()


@retry_query(tries=3, delay=1)
def get_all_users_comments(offset, per_page):
    """Get all comments of all users.
       :params: - offset - pagination option
                - per_page - pagination option
       :return: tuples with comments info
    """
    with pool_manager(READ_ONLY).manager() as conn:
        cursor = conn.cursor()
        query = """SELECT cm.id, cm.content, cm.problem_id,
                   cm.created_date, us.nickname, us.first_name, us.last_name
                   FROM  `comment` as cm
                   LEFT JOIN `user` as us ON cm.user_id=us.id
                   WHERE cm.parent_id=0 LIMIT {},{};
                """
        cursor.execute(query.format(offset, per_page))
        return cursor.fetchall()


@retry_query(tries=3, delay=1)
def get_user_comments(offset, per_page, user_id):
    """Get all comments of user.
       :params: - offset - pagination option
                - per_page - pagination option
       :return: tuples with comments info
    """
    with pool_manager(READ_ONLY).manager() as conn:
        cursor = conn.cursor()
        query = """SELECT cm.id, cm.content, cm.problem_id,
                   cm.created_date, us.nickname, us.first_name, us.last_name
                   FROM  `comment` as cm
                   LEFT JOIN `user` as us ON cm.user_id=us.id
                   WHERE cm.parent_id=0 AND cm.user_id={} LIMIT {},{};
                """
        cursor.execute(query.format(user_id, offset, per_page))
        return cursor.fetchall()


@retry_query(tries=3, delay=1)
def get_count_comments():
    """Get count of comments.
       :return: count of comments
    """
    with pool_manager(READ_ONLY).manager() as conn:
        cursor = conn.cursor()
        query = """SELECT COUNT(id) FROM `comment`
                   WHERE parent_id=0;
                """
        cursor.execute(query)
        return cursor.fetchone()


@retry_query(tries=3, delay=1)
def get_count_user_comments(user_id):
    """Get count of comments of parent comment.
       :params: parent_id - id of parent comment
       :return: count of subcomments
    """
    with pool_manager(READ_ONLY).manager() as conn:
        cursor = conn.cursor()
        query = """SELECT COUNT(id) FROM `comment`
                   WHERE parent_id=0 AND user_id={};
                """
        cursor.execute(query.format(user_id))
        return cursor.fetchone()


@retry_query(tries=3, delay=1)
def get_count_comments_by_nickname(nickname):
    """Get count of comments of parent comment.
       :params: parent_id - id of parent comment
       :return: count of subcomments
    """
    with pool_manager(READ_ONLY).manager() as conn:
        cursor = conn.cursor()
        query = """SELECT COUNT(c.id)
                FROM `comment` AS c
                INNER JOIN `user` AS u ON c.user_id = u.id
                WHERE c.parent_id=0 AND u.nickname LIKE '%{}%';
                """
        cursor.execute(query.format(nickname))
        return cursor.fetchone()


@retry_query(tries=3, delay=1)
def get_comments_by_nickname(nickname, offset, per_page):
    """Function retrieves all user's comments from db by nickname.
    :param nickname: nickname of problem.
    :param offset: pagination option.
    :param per_page: pagination option.
    :return: tuples with user comments info.
    """
    with pool_manager(READ_ONLY).manager() as conn:
        cursor = conn.cursor()
        query = """SELECT  cm.id, cm.content, cm.problem_id,
                   cm.created_date, us.nickname, us.first_name, us.last_name
                   FROM  `comment` as cm
                   INNER JOIN `user` AS us ON cm.user_id=us.id
                   WHERE cm.parent_id=0 AND us.nickname LIKE '%{}%'
                   LIMIT {},{};
                """
        cursor.execute(query.format(nickname, offset, per_page))
        return cursor.fetchall()

@retry_query(tries=3, delay=1)
def get_subscriptions(user_id, offset, per_page):
    """Function retrieves all user's subscriptions from db.
    :param id: id of problem (int)
    :param title: title of problem ('problem with rivers')
    :param problem_type_id: id of problem type (int)
    :param status: status of problem (solved or unsolved)
    :param created_date: date when problem was creared
    :param date_subscriptions: date when user subscribed to a problem
    :return: tuples with user info.
    """
    with pool_manager(READ_ONLY).manager() as conn:
        cursor = conn.cursor()
        query = """SELECT pr.id, pr.title, pr.problem_type_id, pr.status,
                   pr.created_date, sub.date_subscriptions, pt.name
                   FROM  `subscription` as sub
                   INNER JOIN `problem` as pr ON sub.problem_id=pr.id
                   INNER JOIN `problem_type` AS pt ON pr.problem_type_id=pt.id
                   WHERE sub.user_id=%s LIMIT %s,%s;
                """
        cursor.execute(query, (user_id, offset, per_page))
        return cursor.fetchall()

@retry_query(tries=3, delay=1)
def get_all_user_operations(offset, per_page):
    """Function retrieves all user's operation from db.
    :param id: id of user_activity (int)
    :param count id: count of user_activity (int)
    :param user_first_name: user's first_name ('Ivan')
    :param user_last_name: user's last_name ('Ivanenko')
    :param user_nickname: user's nickname ('Ivan89')
    :param creation_date: date when activity created
    :param type: type of operation(delete or password)
    :return: tuples with user info.
    """
    with pool_manager(READ_ONLY).manager() as conn:
        cursor = conn.cursor()
        query = """SELECT uoper.id, u.first_name, u.last_name, u.nickname, 
                   uoper.creation_date, uoper.type
                   FROM  `user` as u
                   INNER JOIN `user_operation` as uoper ON u.id=uoper.user_id
                   LIMIT %s,%s;
                """
        cursor.execute(query, (offset, per_page))
        return cursor.fetchall()

@retry_query(tries=3, delay=1)
def delete_user_operation(user_operation_id):
    """Delete problem type.
       :params: user_operation_id - id of user_operation.
    """
    with pool_manager(READ_WRITE).transaction() as conn:
        query = """DELETE FROM `user_operation`
                   WHERE `id`=%s;
                """
        conn.execute(query, (user_operation_id))

@retry_query(tries=3, delay=1)
def delete_all_users_operations():
    """Delete all data from table user_operation.
    """
    with pool_manager(READ_WRITE).transaction() as conn:
        #cursor = conn.cursor()
        query = """DELETE FROM `user_operation`;
                """
        conn.execute(query)


@retry_query(tries=3, delay=1)
def get_problems_title(problem_ids):
    """Get dictionary with problem id as key and
        problem title as value.
       :params: problems_id - list of problem_ids.
    """
    with pool_manager(READ_ONLY).manager() as conn:
        cursor = conn.cursor()
        query = """SELECT id, title from `problem`
                WHERE id IN ({});
                """
        cursor.execute(query.format(', '.join(map(str, problem_ids))))
        return dict(cursor.fetchall())


@retry_query(tries=3, delay=1)
def get_problems_title(problem_ids):
    """Get dictionary with problem id as key and
        problem title as value.
       :params: problems_id - list of problem_ids.
    """
    with pool_manager(READ_ONLY).manager() as conn:
        cursor = conn.cursor()
        query = """SELECT id, title from `problem`
                WHERE id IN ({});
                """
        cursor.execute(query.format(', '.join(map(str, problem_ids))))
        return dict(cursor.fetchall())

@retry_query(tries=3, delay=1)
def count_subscriptions_by_problem_id():
    """Count of problems created by user with special nickname.
    :return: count of problems.
    """
    with pool_manager(READ_ONLY).manager() as conn:
        cursor = conn.cursor()
        query = """SELECT count(s.problem_id), p.title 
                   FROM `subscription` AS s 
                   INNER JOIN `problem` AS p ON s.problem_id = p.id 
                   GROUP BY s.problem_id;
                """
        cursor.execute(query)
        return cursor.fetchall()

def count_all_type(problem_type_id):
    """Get dictionary with problem id as key and
        problem title as value.
       :params: problems_id - list of problem_ids.
    """
    with pool_manager(READ_ONLY).manager() as conn:
        cursor = conn.cursor()
        query = ("""SELECT COUNT(problem.id), problem_type.name from `problem`
                                INNER JOIN `problem_type`
                                ON problem.problem_type_id = problem_type.id
                WHERE problem_type_id = {};
                """).format(problem_type_id)
        cursor.execute(query)
        return cursor.fetchone()


@retry_query(tries=3, delay=1)
def count_type(problem_type_id, date_format, posted_date):
    """Get dictionary with problem id as key and
        problem title as value.
       :params: problems_id - list of problem_ids.
    """
    with pool_manager(READ_ONLY).manager() as conn:
        cursor = conn.cursor()
        query = ("""SELECT COUNT(problem.id), problem_type.name from `problem`
                                INNER JOIN `problem_type`
                                ON problem.problem_type_id = problem_type.id
                WHERE problem_type_id = '{}' AND
                FROM_UNIXTIME(created_date, '{}') = '{}';
                """).format(problem_type_id, date_format, posted_date)
        cursor.execute(query)
        return cursor.fetchone()

@retry_query(tries=3, delay=1)
def count_problem_types():
    """Count of all problem types
    """
    with pool_manager(READ_ONLY).manager() as conn:
        cursor = conn.cursor()
        query = """SELECT COUNT(id) FROM `problem_type`;"""
        cursor.execute(query)
        return cursor.fetchone()

@retry_query(tries=3, delay=1)
def count_photo():
    """Count of all problem types
    """
    with pool_manager(READ_ONLY).manager() as conn:
        cursor = conn.cursor()
        query = """SELECT COUNT(photo.id) FROM `photo`;"""
        cursor.execute(query)
        return cursor.fetchone()
