"""Module contains a class for testing ecomap.config.Config class"""

import time
import StringIO
import unittest2
import __builtin__

import ecomap.config


ECOMAP_CONF = """
# ecomap.config.Configs for email server.
[email]
user_name = noreply.ecomap
app_password = cmlgeypsicepfbkj
from_email = admin@ecomap.com
admin_email = 'example@example.com'

#ecomap.config.Configs for database pool.
[db]
host = localhost
port = 3306
db_name = ecomap_db
user = root
password = max123

# ecomap.config.Configs for facebook authentication.
# use your own facebook id and developer facebook app key
[oauth]
facebook_id = 1525737571082521
facebook_secret = 571c4cf3817358f46097d38ba46bd188
"""

ECOMAP_CONF_TO_ADD = """
[ecomap]
user = adrian
password = adrian_yavorski
"""

CONFIG = {'email.user_name': 'noreply.ecomap',
          'db.db_name': 'ecomap_db',
          'email.from_email': 'admin@ecomap.com',
          'db.password': 'max123',
          'db.user': 'root',
          'email.admin_email': 'example@example.com',
          'db.port': 3306, 'db.host': 'localhost',
          'email.app_password': 'cmlgeypsicepfbkj',
          'oauth.facebook_id': 1525737571082521,
          'oauth.facebook_secret': '571c4cf3817358f46097d38ba46bd188'}

KEYS = ['email.user_name', 'db.db_name', 'email.from_email',
        'db.password', 'db.user', 'email.admin_email',
        'oauth.facebook_id', 'oauth.facebook_secret',
        'db.port', 'db.host', 'email.app_password']

VALUES = ['noreply.ecomap', 'ecomap_db',
          'admin@ecomap.com', 'max123', 'root',
          'example@example.com', 1525737571082521,
          '571c4cf3817358f46097d38ba46bd188', 3306,
          'localhost', 'cmlgeypsicepfbkj']


def open_mock(fpath):
    """This function mocks path to the file."""

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
        del ecomap.config.Config._instance

    def test_is_dict(self):
        """Tests if a configuration parsers returns a dictionary."""

        configs = ecomap.config.Config()
        test_configs = configs.get_config()
        self.assertIsInstance(test_configs, dict)

    def test_is_singletone(self):
        """Tests if isinstance of ecomap.config.Config class is a Singleton."""

        test_configs_1 = ecomap.config.Config()
        test_configs_2 = ecomap.config.Config()
        self.assertIs(test_configs_1, test_configs_2)

    def test_get_configs(self):
        """Tests whether we receive resulting correct parsed configurations."""

        configs = ecomap.config.Config()
        test_configs = configs.get_config()
        self.assertEqual(test_configs, CONFIG)

    def test_parse_password(self):
        """Tests if a password is received as a string."""

        configs = ecomap.config.Config()
        test_configs = configs.get_config()
        self.assertIsInstance(test_configs['db.password'], str)
        self.assertIsInstance(test_configs['oauth.facebook_secret'], str)
        self.assertIsInstance(test_configs['email.app_password'], str)
        self.assertEqual(test_configs['db.password'], 'max123')
        self.assertTrue(test_configs['oauth.facebook_secret'] ==
                        '571c4cf3817358f46097d38ba46bd188')
        self.assertEqual(test_configs['email.app_password'],
                         'cmlgeypsicepfbkj')

    def test_key(self):
        """Test if correct keys are received."""

        configs = ecomap.config.Config()
        test_configs = configs.get_config()
        self.assertEqual(test_configs.keys(), KEYS)

    def test_value(self):
        """Test if correct values are received."""

        configs = ecomap.config.Config()
        test_configs = configs.get_config()
        self.assertEqual(test_configs.values(), VALUES)

    def test_refresh_time(self):
        """Tests if get_configs is called every 15 minutes."""

        global ECOMAP_CONF
        ecomap_original = ECOMAP_CONF
        ecomap.config.REFRESH_TIME = 1
        configs = ecomap.config.Config()
        before_refresh = configs.get_config()
        ECOMAP_CONF += ECOMAP_CONF_TO_ADD
        time.sleep(2)
        after_refresh = configs.get_config()
        ECOMAP_CONF = ecomap_original
        self.assertNotEqual(before_refresh, after_refresh)


if __name__ == '__main__':
    unittest2.main()
