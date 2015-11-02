"""This module contains functions for interacting with Database."""
from db_pool import db_pool


def get_user_by_username(username):
    """Function which returns user by username.

        :returns tuple of rows(id, password) from db.
    """
    user = None
    with db_pool().manager() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, password FROM user \
                        WHERE first_name=%s", username)
        user = cursor.fetchall()
    return user


def get_user_by_userid(userid):
    """Function which returns user by userid.

        :returns tuple of rows(id, password) from db.
    """
    user = None
    with db_pool().manager() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, password FROM user \
                        WHERE id=%s", userid)
        user = cursor.fetchall()
    return user

if __name__ == "__main__":
    print get_user_by_username("admin")
    print get_user_by_username("rand")
    print get_user_by_userid(1)
    print get_user_by_userid(12)
