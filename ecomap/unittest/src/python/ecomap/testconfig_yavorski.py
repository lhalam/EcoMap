"""Module containing a class for testing Config class"""
import os
import unittest2
from ecomap.config import Config
import ConfigParser



class ConfigParserTestCase(unittest2.TestCase):
    """This class contains methods for testing configuration parser """

    def setUp(self):
        """This method is for receiving configurations to test"""
        print "\n In setUp()"
        self.configs = Config()
        self.configs.test_path = os.path.join(os.environ['PRODROOT'],'unittest/data/ecomap.conf')

    def test_is_dict(self):
        """Testing if configuration parsers return a dictionary"""
        self.assertEqual(type(self.configs.get_config()), type({}))

    def test_is_configuration_file(self):
        """Testing whether a file is a config file"""
        path = self.configs.path.split('.')
        self.assertEqual(path[1], 'conf',msg="This is not a configuration file")

    def test_opening_the_file(self):
        """Test for opening the file"""
        config =ConfigParser.SafeConfigParser()
        try:
            config.readfp(open(self.configs.test_path))
        except IOError:
            self.assertTrue(False, msg="Can't open the file. IOError excepted")

    def test_is_not_empty_dict(self):
        """Test if returning dictionary is empty"""
        parsed_configs = self.configs.get_config()
        self.assertTrue(parsed_configs, msg="Parser returned an empty dictionary")

    def test_if_file_exists(self):
        """Testing whether a file exists"""
        path_to_test = os.path.exists(self.configs.test_path)
        self.assertTrue(path_to_test, msg="File doesn't exist")

    def tearDown(self):
        """"This method is for cleaning up after testing is done"""
        print 'In tearDown()\n'
        del self.configs

if __name__ == '__main__':
    unittest2.main()
