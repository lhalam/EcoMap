"""Module which contains Test of Config class. """

import os
import ConfigParser

import unittest2

from ecomap.config import Config

class TestConfig(unittest2.TestCase):
    """ Class for test Config parser"""

    def setUp(self):
        """ Setting up for the test """
        self.config = Config()
        self.config.path = os.path.join(os.environ['PRODROOT'], 'unittest/data/ecomap.conf')

    def tearDown(self):
        """Cleaning up after the test"""
        del self.config

    def test_return_dictionary(self):
        """ testing if config parser return a dictionary"""
        return_type = type(self.config.get_config())
        expected = dict
        self.assertEqual(return_type, expected, "get_config() return not dictionary type")

    def test_return_empty_dictionary(self):
        """testing if config parser return not empty dictionary"""
        self.assertTrue(self.config.get_config(), "get_config() return empty dictionary")

    def test_wronge_extension(self):
        """testing if config file has extension conf"""
        path = self.config.path.split(".")
        expected = "conf"
        self.assertEqual(path[1], expected, "wronge extension of config file")

    def test_wronge_file(self):
        """testing if config file is in directory"""
        config_test = os.path.exists(self.config.path)
        self.assertTrue(config_test, "there are no such file in this directory ")

    def test_incorrect_config_file(self):
        """testing if config file is correct"""
        config = ConfigParser.SafeConfigParser()
        try:
            config.readfp(open(self.config.path))
        except (ConfigParser.MissingSectionHeaderError, ConfigParser.ParsingError):
            self.assertTrue(config.sections(), "incorrect config file")

if __name__ == '__main__':
    unittest2.main()


