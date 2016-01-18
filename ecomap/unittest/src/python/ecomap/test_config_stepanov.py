import os
import unittest2

from ecomap.config import Config

 
class Test(unittest2.TestCase):
     
    def setUp(self):
        """Setting up for the test"""
        expected_type = dict
        expected_extention = "conf"
        self.config = Config()
        self.config.path = os.path.join(os.environ['PRODROOT'], 'unittest/data/ecomap.conf')

    def tearDown(self):
        """Cleaning up after the test"""
        del self.config

    def test_return_dictionary(self):
        """Testing if config parser return a dictionary"""
        return_config_type = type(self.config.get_config())
        self.assertEqual(return_config_type, expected_type, "get_config() return not dictionary type")

    def test_return_not_empty_dictionary(self):
        """Testing if config parser return not empty dictionary"""
        self.assertTrue(self.config.get_config(), "get_config() return empty dictionary")

    def test_incorrect_extension(self):
        """
        Testing if config file has extension conf
        """
        path = self.config.path.split(".")
        self.assertEqual(path[1], expected_extention, "incorrect extension of config file")

    def test_if_file_exists(self):
        """
        Testing if config file is in directory
        """
        config_test = os.path.exists(self.config.path)
        self.assertTrue(config_test, "there are no such file in this directory ")

if __name__ == "__main__":
    unittest2.main()