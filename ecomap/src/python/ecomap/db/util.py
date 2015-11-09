"""This module contains functions for interacting with Database."""
import logging

from db_pool import db_pool, retry_query


logger = logging.getLogger('util')


@retry_query(tries=3, delay=1)
def get_user_by_email(email):
    # todo add roles SQL reference to user model???
    """Function which returns full user data by unique email.
        returns tuple of rows(id, password) from db.
    """
    # user = None
    # with db_pool().manager() as conn:
    #     cursor = conn.cursor()
    #     cursor.execute("SELECT id, first_name, last_name, email, password \
    #                     FROM user WHERE email=%s", email)
    #     user = cursor.fetchone()
    # return user

    logger.info(email)
    with db_pool().manager() as conn:
        logger.info('log from GET USER user by mail')
        q1 = conn.cursor()
        sql = """SELECT user.id, user.first_name, user.last_name,
                 user.email, user.password,
                 user_role.role_id FROM `user` LEFT JOIN `user_role` ON
                 user.id = user_role.user_id WHERE user.email=%s;"""
        q1.execute(sql, (email,))
        db_userid = q1.fetchone()
        if db_userid:
            # logger.warning('log from GET USER user by mail')
            logger.info('DB.UTIL result!! %s %s %s %s %s' % (db_userid[0],
                                                             db_userid[1],
                                                             db_userid[2],
                                                             db_userid[3],
                                                             db_userid[4]))
            return (db_userid[0], db_userid[1], db_userid[2], db_userid[3],
                    db_userid[4])
    return None


@retry_query(tries=3, delay=1)
def get_user_by_id(uid):
    """Function which returns user by uid.
        returns tuple of rows(uid, password) from db.
    """
    user = None
    with db_pool().manager() as conn:
        cursor = conn.cursor()
        sql = """SELECT user.first_name, user.last_name, user.email,
                 user.password, user_role.role_id FROM `user`
                 LEFT JOIN `user_role` ON user.id = user_role.user_id
                 WHERE user.id=%s;"""
        cursor.execute(sql, (uid,))
        user = cursor.fetchone()
    return user


@retry_query(tries=3, delay=1)
def insert_user(first_name, last_name, email, password):
    """Adds new user into db.
    :params: first_name - first name of user
             last_name - last name of user
             email - email of user
             password - hashed password of user
    """
    with db_pool().manager() as conn:
        cursor = conn.cursor()
        cursor.connection.autocommit(True)
        sql = """START TRANSACTION;
                 INSERT INTO `user` (`first_name`, `last_name`, `email`,
                 `password`) VALUES (%s, %s, %s, %s);
                 INSERT INTO `user_role` (`user_id`, `role_id`)
                 VALUES ((SELECT `id` FROM `user` WHERE `email`=%s),
                 (SELECT `id` FROM `role` WHERE `name`="user"));
                 COMMIT;"""
        cursor.execute(sql, (first_name, last_name, email, password,
                             email))
    return True


# todo put,delete for resources
@retry_query(tries=3, delay=1)
def get_all_resources():
    """Gets all resources from db.
    :return: list of jsons
    """
    parsed_data = {}
    with db_pool().manager() as conn:
        cursor = conn.cursor()
        sql = """SELECT `resource_name` FROM `resource`;"""
        cursor.execute(sql)
        sql_response = cursor.fetchall()
        if sql_response:
            resource_list = [x[0] for x in sql_response]
            parsed_data = [{"resource_name": name} for name in
                           [res for res in resource_list]]
    return parsed_data


@retry_query(tries=3, delay=1)
def add_resource(resource_name):
    """Adds new resource in db.
    :params: res_name - name of new resource
    """
    with db_pool().manager() as conn:
        cursor = conn.cursor()
        sql = """INSERT INTO `resource` (`resource_name`) VALUES (%s);"""
        cursor.execute(sql, (resource_name,))
        conn.commit()
        add_permission(resource_name)
    return True


@retry_query(tries=3, delay=1)
def edit_resource(res_name, res_id):
    """ modify resource name in db.
    :params: res_name - name of resource that had to be modifed
             res_id - key for searching resource name in DB
    """
    with db_pool().manager() as conn:
        cursor = conn.cursor()
        sql = """UPDATE `resource` SET `resource_name` = %s WHERE id = %s;"""
        cursor.execute(sql, (res_name, res_id))
        conn.commit()
    return True


@retry_query(tries=3, delay=1)
def del_resource(res_name, res_id):
    """ modify resource name in db.
    :params: res_name - name of resource that had to be deleted
             res_id - key for searching resource name in DB for deleting
    """
    with db_pool().manager() as conn:
        cursor = conn.cursor()
        sql = """DELETE FROM `resource` WHERE `resource_name`=%s AND
                 `id`=%s;"""
        cursor.execute(sql, (res_name, res_id))
        conn.commit()
    return True


@retry_query(tries=3, delay=1)
def get_roles():
    """Gets all roles from db.
    :return: list of tuples
    """
    parsed_data = {}
    with db_pool().manager() as conn:
        cursor = conn.cursor()
        sql = """SELECT `id`, `name` FROM `role`;"""
        cursor.execute(sql)
        sql_response = cursor.fetchall()
        if sql_response:
            parsed_data = [x for x in sql_response]
    return parsed_data


@retry_query(tries=3, delay=1)
def get_all_resource_id():
    """Return all resources id's.
    :return: list if id's
    """
    with db_pool().manager() as conn:
        cursor = conn.cursor()
        sql = """SELECT `id` FROM `resource`;"""
        cursor.execute(sql)
        return [x[0] for x in cursor.fetchall()]


# todo  DELETE for roles
@retry_query(tries=3, delay=1)
def add_role(role_name):
    """Adds new role in db.
    :params: role_name - name of new role
    """
    with db_pool().manager() as conn:
        cursor = conn.cursor()
        sql = """INSERT INTO `role` (`name`) VALUES (%s);"""
        cursor.execute(sql, (role_name,))
        conn.commit()
        role_id = get_role_id(role_name)

        for resource_id in get_all_resources():
            for action in ['POST', 'GET', 'PUT', 'DELETE']:
                sql = """INSERT INTO `permission` (`action`, `modifier`,
                         `resource_id`, `role_id`) VALUES (%s, %s, %s, %s)"""
                cursor.execute(sql, (action, 'None', resource_id, role_id))
                conn.commit()

    return True


@retry_query(tries=3, delay=1)
def edit_role(role_name, role_id):
    """ modify resource name in db.
    :params: role_name - name of role that had to be modifed
             role_id - key for searching role name in DB
    """
    with db_pool().manager() as conn:
        cursor = conn.cursor()
        sql = """UPDATE `role` SET `name` = %s WHERE id = %s;"""
        cursor.execute(sql, (role_name, role_id))
        conn.commit()
    return True


@retry_query(tries=3, delay=1)
def del_role(role_name, role_id):
    """ modify resource name in db.
    :params: role_name - name of role that had to be deleted
             role_id - key for searching role name in DB for deleting
    """
    with db_pool().manager() as conn:
        cursor = conn.cursor()
        sql = """DELETE FROM `role` WHERE `name` = %s AND `id` = %s;"""
        cursor.execute(sql, (role_name, role_id))
        conn.commit()
    return True


@retry_query(tries=3, delay=1)
def get_permissions():
    """Gets all permissions from db.
    :return: list of permissions[id, action, modifier, resource]
    """
    parsed_data = {}
    with db_pool().manager() as conn:
        cursor = conn.cursor()
        sql = """SELECT p.id, p.action, p.modifier, r.resource_name
                  FROM permission AS p right JOIN
                  resource AS r ON p.resource_id=r.id;"""
        cursor.execute(sql)
        sql_response = cursor.fetchall()
        if sql_response:
            parsed_data = [x for x in sql_response]
    return parsed_data


# todo PUT(?), DELETE for permissions

@retry_query(tries=3, delay=1)
def add_permission(resource_name):
    # def add_action_for_resource!
    """Adds new permission(ACTION FOR RESOURCE) in db BY_RESOURCE_NAME.
    :params: action - method (POST/GET etc.)
             modifier - any/own/None
             resource_name - name of resource
             we select to add permission.
    """
    with db_pool().manager() as conn:
        cursor = conn.cursor()
        cursor.connection.autocommit(True)
        roles = [x[0] for x in get_roles()]
        resource_id = get_resource_id(resource_name)
        sql = """INSERT INTO `permission` (`resource_id`, `action`,
                 `modifier`, `role_id`) VALUES (%s, %s, %s, %s);"""

        for action in ['GET', 'POST', 'PUT', 'DELETE']:
            for role in roles:
                cursor.execute(sql, (resource_id, action, 'None',
                                     role))

        conn.commit()
    return True


@retry_query(tries=3, delay=1)
def bulk_insert(role_name, action, modifier, res_name):
    """ALTERNATIVE some big insert
    """
    with db_pool().manager() as conn:
        cursor = conn.cursor()
        cursor.connection.autocommit(False)
        sql = """START TRANSACTION;
        BEGIN;
        INSERT INTO `permission` (`resourse_id`, `action`,
                 `modifier`) VALUES ((SELECT `id` FROM `resource`
                 WHERE resource_name="{0}"), "{1}", "{2}");
        insert into role_permission
                    (role_id, permission_id)
                values (
                    (select id from role where name="{3}"),
                    (LAST_INSERT_ID()));
        COMMIT;""".format(res_name, action, modifier, role_name)
        cursor.execute(sql)
        # conn.commit()
    return True


@retry_query(tries=3, delay=1)
def default_insert(role_name, action, res_name):
    """ADD ACTION TO RESOURCE WITH DEFAULT MODIFIER
    """
    with db_pool().manager() as conn:
        cursor = conn.cursor()
        cursor.connection.autocommit(False)
        sql = """START TRANSACTION;
        BEGIN;
        INSERT INTO `permission` (`resourse_id`, `action`,
                 `modifier`) VALUES ((SELECT `id` FROM `resource`
                 WHERE resource_name="{0}"), "{1}", "None");
        insert into role_permission
                    (role_id, permission_id)
                values (
                    (select id from role where name="{2}"),
                    (LAST_INSERT_ID()));
        COMMIT;""".format(res_name, action, role_name)
        cursor.execute(sql)
        # conn.commit()
    return True


@retry_query(tries=3, delay=1)
def select_all():
    """Gets resources with permissions and role_permissions.
    :return: list of permissions
    """
    parsed_data = {}
    with db_pool().manager() as conn:
        cursor = conn.cursor()
        sql = """SELECT r.id, r.resource_name, p.action, p.modifier,
             role.id, role.name FROM `resource` AS r LEFT JOIN
             `permission` AS p ON r.id=p.resource_id LEFT JOIN
             `role` AS role ON p.role_id=role.id ORDER BY r.resource_name;"""
        cursor.execute(sql)
        sql_response = cursor.fetchall()
        if sql_response:
            parsed_data = [x for x in sql_response]
    return parsed_data


# add controller
@retry_query(tries=3, delay=1)
def change_user_password(uid, new_pass):
    """Changes users password
    :input: uid - id of user
            new_pass - new password
    """
    with db_pool().manager() as conn:
        cursor = conn.cursor()
        cursor.connection.autocommit(True)
        sql = """UPDATE `user` SET `password`=%s WHERE `id`=%s;"""
        cursor.execute(sql, (new_pass, uid))


@retry_query(tries=3, delay=1)
def get_resource_id(resource_name):
    """Gets resource id.
    :params: resource_name - name of resource
    :return: id - type int
    """
    with db_pool().manager() as conn:
        cursor = conn.cursor()
        sql = """SELECT `id` FROM `resource` WHERE `resource_name`=%s;"""
        cursor.execute(sql, (resource_name, ))
        return cursor.fetchone()[0]


@retry_query(tries=3, delay=1)
def get_role_id(role_name):
    """Gets role id.
    :params: role_name - name of role
    :return: id - type int
    """
    with db_pool().manager() as conn:
        cursor = conn.cursor()
        sql = """SELECT `id` FROM `role` WHERE `name`=%s;"""
        cursor.execute(sql, (role_name, ))
        return cursor.fetchone()[0]


@retry_query(tries=3, delay=1)
def get_permission_id(resource_id, role_id, action):
    """Gets permission id.
    :params: resource_id - id of resource
             role_id - id of role
             action - http method('POST', 'GET', 'PUT', 'DELETE')
    :return: id - type int
    """
    with db_pool().manager() as conn:
        cursor = conn.cursor()
        sql = """SELECT `id` FROM `permission` WHERE `resource_id`=%s AND
                 `role_id`=%s AND `action`=%s;"""
        cursor.execute(sql, (resource_id, role_id, action))
        return cursor.fetchone()[0]


@retry_query(tries=3, delay=1)
def update_role_permission(resource_name, action, modifier,
                           role_name):
    """Updates permission.
    :params: resource_name - name of resource
             action - http method('POST', 'GET', 'PUT', 'DELETE')
             modifier - permission modifier('Any', 'Own', 'None')
             role_name - name of role
    """
    with db_pool().manager() as conn:
        cursor = conn.cursor()

        resource_id = get_resource_id(resource_name)
        role_id = get_role_id(role_name)
        permission_id = get_permission_id(resource_id, role_id, action)

        sql = """UPDATE `permission` SET `modifier`=%s WHERE `id`=%s;"""
        cursor.execute(sql, (action, permission_id))
        conn.commit()
