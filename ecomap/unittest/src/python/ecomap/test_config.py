"""Module contains a class for testing config.Config class"""

import time
import unittest2
import __builtin__

from StringIO import StringIO

from ecomap import config


CONFIG_STRING = """
# ecomap.config.Configs for email server.
[email]
user_name = noreply.ecomap
app_password = cmlgeypsicepfbkj
from_email = admin@ecomap.com
admin_email = 'example@example.com'

# ecomap.config.Configs for database pool.
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

CONFIG_TO_ADD = """
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
          'db.port': 3306,
          'db.host': 'localhost',
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

CONFIG_DICT = {'config': CONFIG_STRING}


class ContextualStringIO(StringIO):

    """Creating a context manager for StringIO"""

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()


def open_mock(fpath, second=None):
    """This function mocks path to the file."""
    return ContextualStringIO(CONFIG_DICT['config'])


class ConfigParserTestCase(unittest2.TestCase):

    """This class contains methods for testing configuration parser."""

    def setUp(self):
        """Mock initialization."""
        if hasattr(config.Config, '_instance'):
            del config.Config._instance
        self.open_original = __builtin__.open
        __builtin__.open = open_mock

    def tearDown(self):
        """"Mock termination and cleaning up."""
        __builtin__.open = self.open_original
        del config.Config._instance

    def test_is_dict(self):
        """Tests if a configuration parsers returns a dictionary."""
        configs = config.Config()
        self.assertIsInstance(configs.get_config(), dict)

    def test_is_singletone(self):
        """Tests if isinstance of config.Config class is a Singleton."""
        test_configs_1 = config.Config()
        test_configs_2 = config.Config()
        self.assertIs(test_configs_1, test_configs_2)

    def test_get_config(self):
        """Tests whether we receive resulting correct parsed configurations."""
        configs = config.Config()
        self.assertEqual(configs.get_config(), CONFIG)

    def test_parse_password(self):
        """Tests if a password is received as a string."""
        configs = config.Config()
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
        configs = config.Config()
        test_configs = configs.get_config()
        self.assertEqual(test_configs.keys(), KEYS)

    def test_value(self):
        """Test if correct values are received."""
        configs = config.Config()
        test_configs = configs.get_config()
        self.assertEqual(test_configs.values(), VALUES)

    def test_refresh_time(self):
        """Tests if get_configs is called every 15 minutes."""
        ecomap_original = CONFIG_STRING
        config.REFRESH_TIME = 1
        configs = config.Config()
        before_refresh = configs.get_config()
        CONFIG_DICT['config'] += CONFIG_TO_ADD
        time.sleep(2)
        after_refresh = configs.get_config()
        CONFIG_DICT['config'] = ecomap_original
        self.assertNotEqual(before_refresh, after_refresh)


if __name__ == '__main__':
    unittest2.main()
