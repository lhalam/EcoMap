"""Module contains a class for testing Config class"""

import time
import StringIO
import unittest2
import __builtin__

from mock import patch

from ecomap.config import Config


ECOMAP_CONF = """
# Configs for email server.
[email]
user_name = noreply.ecomap
app_password = cmlgeypsicepfbkj
from_email = admin@ecomap.com
admin_email = 'example@example.com'

#Configs for database pool.
[db]
host = localhost
port = 3306
db_name = ecomap_db
user = root
password = max123
"""

CONFIG = {'email.user_name': 'noreply.ecomap',
          'db.db_name': 'ecomap_db',
          'email.from_email': 'admin@ecomap.com',
          'db.password': 'max123',
          'db.user': 'root',
          'email.admin_email': 'example@example.com',
          'db.port': 3306, 'db.host': 'localhost',
          'email.app_password': 'cmlgeypsicepfbkj'}

KEYS = ['email.user_name', 'db.db_name',
        'email.from_email', 'db.password',
        'db.user', 'email.admin_email', 'db.port',
        'db.host', 'email.app_password']

VALUES = ['noreply.ecomap', 'ecomap_db',
          'admin@ecomap.com', 'max123',
          'root', 'example@example.com', 3306,
          'localhost', 'cmlgeypsicepfbkj']


def open_mock(fpath):

    """This function mocks path to the file """

    return StringIO.StringIO(ECOMAP_CONF)


class ConfigParserTestCase(unittest2.TestCase):

    """This class contains methods for testing configuration parser."""

    def setUp(self):

        """In this method we replace builtin open() wth open_mock."""

        self.open_original = __builtin__.open
        __builtin__.open = open_mock

    def tearDown(self):

        """"This method is for returning builtin open()."""

        __builtin__.open = self.open_original

    def test_is_dict(self):

        """Tests if a configuration parsers returns a dictionary."""

        configs = Config()
        test_configs = configs.get_config()
        self.assertIsInstance(test_configs, dict)

    def test_is_Singletone(self):

        """Tests if isinstance of Config class is a Singleton."""

        test_configs_1 = Config()
        test_configs_2 = Config()
        self.assertIs(test_configs_1, test_configs_2)

    def test_get_configs(self):

        """Tests whether we receive resulting correct parsed configurations."""

        configs = Config()
        test_configs = configs.get_config()
        self.assertEqual(test_configs, CONFIG)

    def test_parse_password(self):

        """Tests if a password is received as a string."""

        configs = Config()
        test_configs = configs.get_config()
        self.assertEqual(test_configs['db.password'], 'max123')

    def test_key(self):

        """Test if correct keys are received"""

        configs = Config()
        test_configs = configs.get_config()
        self.assertEqual(test_configs.keys(), KEYS)

    def test_value(self):

        """Test if correct values are received"""

        configs = Config()
        test_configs = configs.get_config()
        self.assertEqual(test_configs.values(), VALUES)

    @patch('ecomap.config.REFRESH_TIME', 1)
    def test_refresh_time(self):

        """Tests if get_configs is called every 15 minutes."""

        configs = Config()
        configs.get_config()
        before_refresh = configs.update_time
        time.sleep(2)
        configs.get_config()
        after_refresh = configs.update_time
        self.assertNotEqual(before_refresh, after_refresh)


if __name__ == '__main__':
    unittest2.main()
