import os
import unittest2
import ecomap.config
from mock import Mock


class TestConfig(unittest2.TestCase):
    def setUp(self):
    	""" Setting up for the test """
    	print "TestConfig:setUp: begin"

    	self.return_dictionary = ecomap.config.Config().get_config() 

    	testName = self.shortDescription()
    	if testName == "Test routine is_return_dictionary":
            print "setting up for test is_return_dictionary"
        if testName == "Test routine is_return_not_empty_dictionary":
            print "setting up for test is_return_not_empty_dictionary"
        if testName == "Test routine wronge_path":
            print "setting up for test wronge_path"

        print "TestConfig:setUp: end"
 
    def tearDown(self):
    	"""Cleaning up after the test"""
        print "TestConfig:tearDown: begin"

    	testName = self.shortDescription()
    	if testName == "Test routine is_return_dictionary":
            print "cleaning up after test is_return_dictionary"
        if testName == "Test routine is_return_not_empty_dictionary":
            print "cleaning up after test is_return_not_empty_dictionary"
        if testName == "Test routine wronge_path":
            print "cleaning up after test wronge_path"

        del self.return_dictionary

        print "TestConfig:tearDown: end"
 
    def test_is_return_dictionary(self):
    	"""Test routine is_return_dictionary"""
    	self.return_type = type(self.return_dictionary)
        self.assertEqual(self.return_type, type({}), "get_config() return not dictionary type")

    def test_is_return_not_empty_dictionary(self):
    	"""Test routine is_return_not_empty_dictionary"""
        self.assertTrue(self.return_dictionary, "get_config() return empty dictionary")

    def test_wronge_path(self):
    	"""Test routine wronge_path"""
    	test_path = ecomap.config.CONFIG_PATH
    	path = test_path.split(".")
    	self.assertEqual(path[1], "conf", "wronge path to config file")

 
 
if __name__ == '__main__':
    unittest2.main()


