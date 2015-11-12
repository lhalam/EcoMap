"""This module holds User class"""
import hashlib

from flask_login import UserMixin, LoginManager, AnonymousUserMixin
from itsdangerous import URLSafeTimedSerializer

import db.util as util

from ecomap.app import app

login_serializer = URLSafeTimedSerializer(app.secret_key)
login_manager = LoginManager(app)
login_manager.login_view = "login"


class Anonymous(AnonymousUserMixin):
    def __init__(self):
        self.username = 'ANON'

    def __repr__(self):
        return self.username


class User(UserMixin):

    """Class which describes User entity"""

    def __init__(self, uid, first_name, last_name, email, password):
        self.uid = uid
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password

    def __repr__(self):
        return self.first_name

    def get_auth_token(self):
        """This method encodes a secure token from a cookie.
            :returns token
        """

        data = [str(self.uid), self.password]
        return login_serializer.dumps(data)

    def verify_password(self, password):
        """This method compares passwords from db and passed password
        from client side.

            :params
            password - passed password from the client

            :return True if passwords are equa, otherwise it will
            return False
        """
        return self.password == hash_pass(password)

    def change_password(self, new_pass):
        """Method which changes user's password."""
        new_pass_salted = hash_pass(new_pass)
        util.change_user_password(self.uid, new_pass_salted)

    def is_active(self):
        """Overloaded method from UserMixin.
        Since we don't have activation mechanism, we just
        return True.
        """
        return True

    def get_id(self):
        return unicode(self.uid)

    # def get_id(self):
    #     """Return the email address to satisfy Flask-Login's requirements."""
    #     return self.email


def hash_pass(password):
    """This function adds some salt(secret_key)
    to the password.

        :returns hash sum from password + salt
    """
    salted_password = password + app.config['SECRET_KEY']
    return hashlib.md5(salted_password).hexdigest()


def get_user_by_email(email):
    """This function gets user data from db by user email
    and creates User instance if data was retrieved.

        :returns User instance or None if user doesn't
        exist.
    """
    user = None
    if email:
        app.logger.info('USER.PY GET U_BY EMAL initial email %s', email)
        user = util.get_user_by_email(email)
    if user:
        return User(user[0], user[1], user[2],
                    user[3], user[4])
    return None


def get_user_by_id(uid):
    """This function gets user data from db by user id
    and creates User instance if data was retrieved.

        :returns User instance or None if user doesn't
        exist.
    """
    user = None
    if uid:
        user = util.get_user_by_id(uid)
    if user:
        return User(user[0], user[1], user[2],
                    user[3], user[4])

    return None


def register(first_name, last_name, email, password):
    """This function registrates user.
    It will insert user's data via insert_user function
    from util.

        :returns True if transaction finished successfully.
    """
    salted_pass = hash_pass(password)
    return util.insert_user(first_name, last_name, email, salted_pass)


@login_manager.user_loader
def load_user(uid):
    """This method is callback, which is used in
    Login Manager inner logic for loading User
    instance by it's id.

        :returns User instance.
    """
    return get_user_by_id(int(uid))


@login_manager.token_loader
def load_token(token):
    """This metod is callback, which is used in
    the Login Manager inner logic for retrieving
    data from token.

        :returns User instance or None if token
        is invalid.
    """
    max_age = app.config["REMEMBER_COOKIE_DURATION"].total_seconds()
    data = login_serializer.loads(token, max_age=max_age)

    user = get_user_by_id(data[0])

    if user and data[1] == user.password:
        return user
    return None


if __name__ == "__main__":
    get_user_by_id(27).change_password('test_new')
