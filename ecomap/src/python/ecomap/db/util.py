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
        sql = """SELECT user.id, user.first_name, user.last_name, user.email, user.password,
                 user_role.role_id FROM `user` LEFT JOIN `user_role` ON
                 user.id = user_role.user_id WHERE user.email=%s;"""
        q1.execute(sql, (email, ))
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
        cursor.execute(sql, (uid, ))
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
def add_resource(res_name):
    """Adds new resource in db.
    :params: res_name - name of new resource
    """
    with db_pool().manager() as conn:
        cursor = conn.cursor()
        sql = """INSERT INTO `resource` (`resource_name`) VALUES (%s);"""
        cursor.execute(sql, (res_name,))
        conn.commit()
    return True


def edit_resource(res_name, res_id):
    with db_pool().manager() as conn:
        cursor = conn.cursor()
        sql = """UPDATE `resource` SET `resource_name` = %s WHERE id = %s;"""
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


# todo PUT, DELETE for roles
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
    return True


@retry_query(tries=3, delay=1)
def get_permissions():
    """Gets all permissions from db.
    :return: list of permissions
    """
    parsed_data = {}
    with db_pool().manager() as conn:
        cursor = conn.cursor()
        sql = """SELECT p.id, p.action, p.modifier, r.resource_name
                  FROM permission AS p LEFT JOIN
                  resource AS r ON p.resourse_id=r.id;"""
        cursor.execute(sql)
        sql_response = cursor.fetchall()
        if sql_response:
            parsed_data = [x for x in sql_response]
    return parsed_data


# todo PUT, DELETE for permissions
@retry_query(tries=3, delay=1)
def add_permission(action, modifier, resource_name):
    """Adds new permission in db.
    :params: action - method (POST/GET etc.)
             modifier - any/own/None
             resource_name - name of resource_name we add permission
    """
    with db_pool().manager() as conn:
        cursor = conn.cursor()
        cursor.connection.autocommit(True)
        sql = """INSERT INTO `permission` (`resourse_id`, `action`,
                 `modifier`) VALUES ((SELECT `id` FROM `resource`
                 WHERE `resource_name`=%s), %s, %s);"""
        cursor.execute(sql, (resource_name, action, modifier))
    return True


@retry_query(tries=3, delay=1)
def make_it():
    """Gets resources with permissions and role_permissions.
    :return: list of permissions
    """
    parsed_data = {}
    with db_pool().manager() as conn:
        cursor = conn.cursor()
        sql = """SELECT res.resource_name,  p.action, p.modifier, r.name
                 FROM role AS r join role_permission
                 AS rp ON r.id = rp.id join permission
                 AS p ON rp.id = p.id join resource
                 AS res ON p.resourse_id = res.id;"""
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


# if __name__ == "__main__":
#     # print get_user_by_email("admin@gmail.com")
