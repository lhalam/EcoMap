"""This module contains functions for interacting with Database."""
import logging

from db_pool import db_pool, retry_query
from ecomap.utils import get_logger


get_logger()
logger = logging.getLogger('util')


@retry_query(tries=3, delay=1)
def get_user_by_email(email):
    # todo add roles SQL reference to user model
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

#todo put,delete
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

#todo PUT, DELETE
def add_role(role_name):
    with db_pool().manager() as conn:
        cursor = conn.cursor()
        sql = """INSERT INTO `role` (`name`) VALUES (%s);"""
        cursor.execute(sql, (role_name,))
        conn.commit()
    return True

#
# if __name__ == "__main__":
#     # print get_user_by_email("admin@gmail.com")
