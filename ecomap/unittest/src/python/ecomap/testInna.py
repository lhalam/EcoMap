import os
import unittest2
from ConfigParser import SafeConfigParser

import ecomap.config 


class TestConfig(unittest2.TestCase):
    def setUp(self):
    	""" 
        Setting up for the test 
        """
        self.config = ecomap.config.Config()
        self.config.path = os.path.join(os.environ['PRODROOT'], 'unittest/data/ecomap.conf')
        self.parse_config = ecomap.config.Config().get_config() 
        
 
    def tearDown(self):
    	"""
        Cleaning up after the test
        """
        del self.config
 
    def test_return_dictionary(self):
    	return_type = type(self.parse_config)
        self.assertEqual(return_type, type({}), "get_config() return not dictionary type")

    def test_return_not_empty_dictionary(self):
        self.assertTrue(self.parse_config, "get_config() return empty dictionary")

    def test_wronge_extension(self):
    	path = self.config.path .split(".")
    	self.assertEqual(path[1], "conf", "wronge extension of config file")

    def test_wronge_file(self):
        config_test = os.path.exists(self.config.path)
        self.assertTrue(config_test, "there are no such file in this directory ")

    def test_incorrect_config_file(self):
        try:
            config = SafeConfigParser()
            config.readfp(open(self.config.path))
            sections = config.sections()
        except MissingSectionHeaderError or ParsingError:
            print "The file does not exist, exiting gracefully"
            self.assertTrue(False, "incorrect config file")

if __name__ == '__main__':
    unittest2.main()


