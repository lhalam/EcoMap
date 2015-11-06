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
        sql = """SELECT `id`, `first_name`, `last_name`, `email`, `password`
                 FROM `user` WHERE `email`=%s;"""
        cursor.execute(sql, (email,))
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

if __name__ == "__main__":
    print get_user_by_email("admin@gmail.com")
