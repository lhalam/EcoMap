"""This module contains functions for interacting with Database."""
import logging

from db_pool import db_pool, retry_query
from ecomap.utils import get_logger


get_logger()
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

    logger.warning(email)
    with db_pool().manager() as conn:
        q1 = conn.cursor()
        sql = """SELECT `id`, `first_name`, `last_name`, `email`, `password`
                        FROM `user` WHERE `email`=%s;"""
        q1.execute(sql, (email, ))
        db_userid = q1.fetchone()
        if db_userid:
            logger.warning('log from GET USER user by mail')
            logger.warning('DB.UTIL result!! %s %s %s %s %s' % (db_userid[0], db_userid[1],
                          db_userid[2], db_userid[3], db_userid[4]))
            return (db_userid[0], db_userid[1], db_userid[2], db_userid[3], db_userid[4])
    return None


@retry_query(tries=3, delay=1)
def get_user_by_id(uid):
    """Function which returns user by uid.

        returns tuple of rows(uid, password) from db.
    """
    user = None
    with db_pool().manager() as conn:
        cursor = conn.cursor()
        sql = """SELECT `id`, `first_name`, `last_name`, `email`, `password`
                        FROM `user` WHERE `id`=%s;"""
        cursor.execute(sql, (uid, ))
        user = cursor.fetchone()
    return user


def insert_user(first_name, last_name, email, password):
    with db_pool().manager() as conn:
        cursor = conn.cursor()
        sql = """INSERT INTO `user` (`first_name`, `last_name`, `email`, `password`)
                        VALUES (%s, %s, %s, %s);"""
        cursor.execute(sql, (first_name, last_name, email, password))
        conn.commit()
    return True

#todo put,delete for resources
def get_all_resources():
    """

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
            parsed_data = [{"resource_name": name} for name in [res for res in resource_list]]
    return parsed_data


def add_resource(res_name):
    with db_pool().manager() as conn:
        cursor = conn.cursor()
        sql = """INSERT INTO `resource` (`resource_name`) VALUES (%s);"""
        cursor.execute(sql, (res_name,))
        conn.commit()
    return True



def get_roles():
    """

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
def add_role(role_name):
    with db_pool().manager() as conn:
        cursor = conn.cursor()
        sql = """INSERT INTO `role` (`name`) VALUES (%s);"""
        cursor.execute(sql, (role_name,))
        conn.commit()
    return True


def get_permissions():
    parsed_data = {}
    with db_pool().manager() as conn:
        cursor = conn.cursor()
        sql = """SELECT p.id, p.action, p.modifier, r.resource_name
                  FROM permission as p LEFT JOIN
                  resource as r ON p.resourse_id=r.id;"""
        cursor.execute(sql)
        sql_response = cursor.fetchall()
        if sql_response:
            parsed_data = [x for x in sql_response]
    return parsed_data


# todo PUT, DELETE for permissions
def add_permission(action, modifier, resource_name):
    with db_pool().manager() as conn:
        cursor = conn.cursor()
        sql = """insert into resource (resource_name) values(%s);
                  """
        cursor.execute(sql, (resource_name,))
        conn.commit()
        sql2 = """insert into permission (resourse_id, action, modifier)
                  values(LAST_INSERT_ID(), %s, %s);"""
        cursor.execute(sql2, (action, modifier))
        conn.commit()
    return True

# TODO reformat sqls!
def make_it():
    parsed_data = {}
    with db_pool().manager() as conn:
        cursor = conn.cursor()
        sql = """select res.resource_name,  p.action, p.modifier, r.name
                from role as r join role_permission
                as rp on r.id = rp.id join permission
                as p on rp.id = p.id join resource
                as res on p.resourse_id = res.id;"""
        cursor.execute(sql)
        sql_response = cursor.fetchall()
        if sql_response:
            parsed_data = [x for x in sql_response]
    return parsed_data

#
# if __name__ == "__main__":
#     # print get_user_by_email("admin@gmail.com")
