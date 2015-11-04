"""This module contains functions for interacting with Database."""
from db_pool import db_pool
from ecomap.utils import get_logger

import logging

get_logger()
def get_user_by_email(email):
    """Function which returns user by email.

        :returns tuple of rows(id, password) from db.
    """
    user = None
    logger = logging.getLogger('util')
    logger.warning(email)
    # with db_pool().manager() as conn:
    #     cursor = conn.cursor()
    #     cursor.execute("SELECT id, first_name, last_name, email, password \
    #                     FROM user WHERE email=%s", email)
    #     user = cursor.fetchall()
    #     logger.warning('user')
    # return user

    with db_pool().manager() as conn:
        q1 = conn.cursor()
        try:
            q1.execute('select * from user where email="%s";' % email)
            db_userid = q1.fetchone()
            logger.warning('log from GET USER user by mail')
            logger.warning('DB.UTIL reslt!! %s %s %s %s %s' % (db_userid[0], db_userid[1], db_userid[2], db_userid[3], db_userid[4]))
            return (db_userid[0], db_userid[1], db_userid[2], db_userid[3], db_userid[4])
        except:
            return None


def get_user_by_id(uid):
    """Function which returns user by uid.

        :returns tuple of rows(uid, password) from db.
    """
    user = None
    with db_pool().manager() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, first_name, last_name, email, password \
                        FROM user WHERE id=%s;", uid)
        user = cursor.fetchall()
    return user


def insert_user(first_name, last_name, email, password):
    with db_pool().manager() as conn:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO user \
                        (first_name, last_name, email, password) \
                        VALUES (%s, %s, %s, %s);',
                       (first_name, last_name, email, password))
        conn.commit()
    return True

if __name__ == "__main__":
    insert_user('insert_test', 'insert_test', 'insert_test', 'insert_test')
