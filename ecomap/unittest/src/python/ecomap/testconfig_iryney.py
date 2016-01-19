import os
import unittest2
from ecomap.config import Config

class MockConfig(Config):
    """ Mock Config object inherits Config """

    def __init__(self):
        Config.__init__(self)
        self.path = os.path.join(os.environ['PRODROOT'], 'unittest/data/ecomap.conf')


class ConfigTest(unittest2.TestCase):

    def setUp(self):
        """ Set up data for test """
        self.config = MockConfig()

    def tearDown(self):
        """ Clean up data after test """
        del self.config

    def test_return_type(self):
        """ Check if config parser returns dictionary """
        expected = dict
        actual = type(self.config.get_config())
        self.assertEqual(actual, expected, "Config parser does not return dictionary")

    def test_return_truth_value(self):
        """ Check if config parser returns truth value """ 
        self.assertTrue(self.config.get_config(), "Config parser returns false value")

    def test_config_file_exist(self):
        """ Check if config file exists """
        self.assertTrue(os.path.isfile(self.config.path), "Config file does not exist")

    def test_configfile_extension(self):
        """ Check if file is a config file """
        self.assertEqual(self.config.path.split('.')[1], 'conf', "File is not config file")    

    def test_return_data(self):
        """ Check if db.user is in parser return value """
        self.assertTrue('db.user' in self.config.get_config(), "db.user is not in return value")

if __name__ == '__main__':
    unittest2.main()

