"""This module contains functions for interacting with Database."""
import logging

from db_pool import db_pool, retry_query
from ecomap.utils import get_logger


get_logger()
logger = logging.getLogger('util')


@retry_query(tries=3, delay=1)
def get_user_by_email(email):
    """Function which returns full user data by unique email.

        returns tuple of rows(id, password) from db.
    """
    user = None
    with db_pool().manager() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, first_name, last_name, email, password \
                        FROM user WHERE email=%s", email)
        user = cursor.fetchone()
    return user


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


@retry_query(tries=3, delay=1)
def change_user_password(uid, new_pass):
    """Changes users password
    :input: uid - id of user
            new_pass - new password
    """
    with db_pool().manager() as conn:
        cursor = conn.cursor()
        query = """UPDATE `user` SET `password`=%s WHERE `id`=%s;"""
        cursor.execute(query, (new_pass, uid))
        conn.commit()

if __name__ == "__main__":
    change_user_password(27, "test")
