"""This module holds User class"""
import md5

from flask_login import UserMixin, LoginManager
from itsdangerous import URLSafeSerializer

from ecomap.app import app
from util import get_user_by_email, get_user_by_userid, insert_user


login_serializer = URLSafeSerializer('test')
login_manager = LoginManager(app)


class User(UserMixin):

    """Class which describes User entity"""

    def __init__(self, userid, first_name, last_name, email, password):
        self.userid = userid
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password

    def get_auth_token(self):
        """This method encodes a secure token from a cookie."""
        data = [str(self.userid), self.password]
        return login_serializer.dumps(data)

    def set_password(self, password):
        """
        method needed for generate unique pasword hash to store in db.
        uses built-in flask function
        :param password: clean password
        :return:
        """
        self.password = hash_pass(password)

    def verify_password(self, password):
        """
        method for checking and comparing passwords from db and login form
        :param password:
        :return:
        """
        return self.password == hash_pass(password)      # FIX TRICK

    @staticmethod
    def get(userid=None, username=None):
        """Static method get() searches for user in db.
        If it exists, then method will return user object,
        otherwise it will return None.
        """
        user = None
        if userid:
            user = get_user_by_userid(userid)
        if username:
            user = get_user_by_email(username)
        if user:
            return User(user[0][0], user[0][1], user[0][2],
                        user[0][3], user[0][4])
        return None

    @staticmethod
    def register(first_name, last_name, email, password):
        salted_pass = hash_pass(password)
        return insert_user(first_name, last_name, email, salted_pass)

    def is_active(self):    # fix
        return True

    def is_authenticated(self):     # fix
        return False

    def is_anonymous(self):     # fix
        return False

    def get_id(self):
        return unicode(self.userid)


def hash_pass(password):
    """Returns md5 sum of password+salt"""
    salted_password = password + app.config['SECRET_KEY']
    return md5.new(salted_password).hexdigest()


@login_manager.user_loader
def load_user(userid):
    return User.get(userid=int(userid))


@login_manager.token_loader
def load_token(token):
    """"""
    # max_age = app.config["REMEMBER_COOKIE_DURATION"].total_seconds()
    data = login_serializer.loads(token)

    user = User.get(userid=data[0])

    if user and data[1] == user.password:
        return user
    return None

# Tell the login manager where to redirect users to display the login page
login_manager.login_view = "/"


if __name__ == "__main__":
    User.register('test2', 'test2', 'test2@gmail.com', '1111')
    # usr = User.get(username='admin')
    # print usr
    # print usr.get_auth_token()
    # print usr.get_id()
    # print hash_pass('some_random_password')
    # print login_serializer
