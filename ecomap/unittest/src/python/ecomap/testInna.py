import os
import unittest2

import ecomap.config


class TestConfig(unittest2.TestCase):
    def setUp(self):
    	""" 
        Setting up for the test 
        """
        self.parse_config = ecomap.config.Config().get_config() 
 
    def tearDown(self):
    	"""
        Cleaning up after the test
        """
        del self.parse_config
 
    def test_return_dictionary(self):
    	return_type = type(self.parse_config)
        self.assertEqual(return_type, type({}), "get_config() return not dictionary type")

    def test_return_not_empty_dictionary(self):
        self.assertTrue(self.parse_config, "get_config() return empty dictionary")

    def test_wronge_extension(self):
    	test_path = ecomap.config.CONFIG_PATH
    	path = test_path.split(".")
    	self.assertEqual(path[1], "conf", "wronge extension of config file")

 
 
if __name__ == '__main__':
    unittest2.main()


