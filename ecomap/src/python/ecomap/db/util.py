"""This module contains functions for interacting with Database."""
from db_pool import db_pool, retry_query


@retry_query(tries=3, delay=1)
def get_user_by_email(email):
    """Function which returns full user data by unique email.

        returns tuple of row(user data) from db.
    """
    with db_pool().manager() as conn:
        cursor = conn.cursor()
        query = """SELECT id, first_name, last_name, email, password \
                   FROM user WHERE email=%s"""
        cursor.execute(query, (email,))
        return cursor.fetchone()


@retry_query(tries=3, delay=1)
def get_user_by_id(uid):
    """Function which returns user by uid.

        returns tuple of rows(uid, password) from db.
    """
    with db_pool().manager() as conn:
        cursor = conn.cursor()
        query = """SELECT `id`, `first_name`, `last_name`, `email`, `password`
                 FROM `user` WHERE `id`=%s;"""
        cursor.execute(query, (uid, ))
        return cursor.fetchone()


def insert_user(first_name, last_name, email, password):
    """Function which inserts user raw into db.
    """
    with db_pool().manager() as conn:
        cursor = conn.cursor()
        query = """INSERT INTO `user` (`first_name`, `last_name`, `email`, `password`)
                   VALUES (%s, %s, %s, %s);"""
        cursor.execute(query, (first_name, last_name, email, password))
        conn.commit()
