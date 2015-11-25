"""This module holds User class"""
import hashlib
import time

from flask_login import UserMixin, LoginManager, AnonymousUserMixin
from itsdangerous import URLSafeTimedSerializer

from ecomap.db import util

from ecomap.app import app

LOGIN_SERIALIZER = URLSafeTimedSerializer(app.secret_key)
LOGIN_MANAGER = LoginManager(app)
LOGIN_MANAGER.login_view = "login"


class Anonymous(AnonymousUserMixin):
    def __init__(self):
        self.username = 'ANON'

    def __repr__(self):
        return self.username


class User(UserMixin):

    """Class which describes User entity"""

    def __init__(self, uid, first_name, last_name, email, password, role):
        self.uid = uid
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.role = role

    def __repr__(self):
        return self.first_name

    def get_auth_token(self):
        """This method encodes a secure token from a cookie.
            :returns token
        """

        data = [str(self.uid), self.password]
        return LOGIN_SERIALIZER.dumps(data)

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
        """Returns current user id."""
        return unicode(self.uid)


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
        app.logger.info('USER.PY GET U_BY EMAIL initial email %s', email)
        user = util.get_user_by_email(email)

    if user:
        user_role = util.get_user_role_by_email(email)
        return User(user[0], user[1], user[2],
                    user[3], user[4], user_role[0])
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
        user_role = util.get_user_role_by_id(uid)
        return User(user[0], user[1], user[2],
                    user[3], user[4], user_role[0])

    return None


def get_user_by_oauth_id(uid):
    """This function gets user data from db by oauth id
    and creates User instance if data was retrieved.

        :returns User instance or None if user doesn't
        exist.
    """
    user = None
    if uid:
        user = util.get_user_by_oauth_id(uid)
    if user:
        user_role = util.get_user_role_by_id(user[0])
        return User(user[0], user[1], user[2],
                    user[3], user[4], user_role[0])

    return None


def register(first_name, last_name, email, password):
    """This function registrates user.
    It will insert user's data via insert_user function
    from util.

        :returns True if transaction finished successfully.
    """
    salted_pass = hash_pass(password)
    role_id = util.get_role_id('user')
    return util.insert_user(first_name, last_name, email, salted_pass,
                            role_id)


def facebook_register(first_name, last_name, email, provider, uid):
    """This function registres user through facebook.
    It will insert user's data via insert_user function
    from util.
        :returns True if transaction finished successfully.
    """
    salted_pass = hash_pass(time.ctime())
    role_id = util.get_role_id('user')
    return util.facebook_insert(first_name, last_name, email, salted_pass,
                                role_id, provider, uid)


@LOGIN_MANAGER.user_loader
def load_user(uid):
    """This method is callback, which is used in
    Login Manager inner logic for loading User
    instance by it's id.

        :returns User instance.
    """
    return get_user_by_id(int(uid))


@LOGIN_MANAGER.token_loader
def load_token(token):
    """This metod is callback, which is used in
    the Login Manager inner logic for retrieving
    data from token.

        :returns User instance or None if token
        is invalid.
    """
    max_age = app.config["REMEMBER_COOKIE_DURATION"].total_seconds()
    data = LOGIN_SERIALIZER.loads(token, max_age=max_age)

    user = get_user_by_id(data[0])

    if user and data[1] == user.password:
        return user
    return None
