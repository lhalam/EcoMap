"""This module contains functions for interacting with Database."""
from db_pool import db_pool, retry_query
from ecomap.utils import get_logger

import logging

get_logger()


@retry_query(tries=3, delay=1)
def get_user_by_email(email):
    """Function which returns user by email.
        :returns tuple of rows(id, password) from db.
    """
    logger = logging.getLogger('util')
    logger.warning(email)

    with db_pool().manager() as conn:
        q1 = conn.cursor()
        sql = """SELECT `id`, `first_name`, `last_name`, `email`, `password`
                 FROM `user` WHERE `email`=%s;"""
        q1.execute(sql, (email,))
        db_userid = q1.fetchone()
        if db_userid:
            logger.warning('log from GET USER user by mail')
            logger.warning('DB.UTIL result!! %s %s %s %s %s', db_userid[0],
                           db_userid[1], db_userid[2], db_userid[3],
                           db_userid[4])
            return (db_userid[0], db_userid[1], db_userid[2], db_userid[3],
                    db_userid[4])
        return None


@retry_query(tries=3, delay=1)
def get_user_by_id(uid):
    """Function which returns user by uid.
        :returns tuple of rows(uid, password) from db.
    """
    user = None
    with db_pool().manager() as conn:
        cursor = conn.cursor()
        sql = """SELECT `id`, `first_name`, `last_name`, `email`, `password`
                 FROM `user` WHERE `id`=%s;"""
        cursor.execute(sql, (uid,))
        user = cursor.fetchone()
    return user


@retry_query(tries=3, delay=1)
def insert_user(first_name, last_name, email, password):
    with db_pool().manager() as conn:
        cursor = conn.cursor()
        query = """INSERT INTO `user` (`first_name`, `last_name`, `email`,
                   `password`) VALUES (%s, %s, %s, %s);"""
        cursor.execute(query, (first_name, last_name, email, password))
        conn.commit()
    return True

if __name__ == "__main__":
    insert_user('insert_test', 'insert_test', 'insert_test', 'insert_test')
