import os
import mock
import  unittest2
#from ConfigParser import SafeConfigParser
from ecomap.config import Config



class TestConfig(unittest2.TestCase):
    def setUp(self):
        '''Settin up for test'''
        self.config_test = Config()
        #self. = os.path.join(os.environ['PRODROOT'], 'unittest/data/ecomap.conf')
    
    def test_is_dictionary(self):
        '''This test is testing type of object'''
        d = type({})
        d_test = type(self.config_test.get_config())
        self.assertEqual(d_test, d, 'false')

    def test_if_extension_is_equal_conf(self):
        '''Test: does file have correct extension'''
        path = self.config_test.path.split('.')
        self.assertEqual(path[1], 'conf', 'File  with incorect extension')

    def test_is_file_exists(self):
        '''Test: does file exist in directory '''
        self.config_test.path = os.path.join(os.environ['PRODROOT'], 'unittest/data/ecomap.conf')
        file_test = os.path.exists(self.config_test.path)
        self.assertTrue(file_test, 'File doesnt exist')

    def test_is_dictionary_not_empty(self):
        '''Test: dictionary not empty '''
        d = {}
        d_test = self.config_test.get_config()
        self.assertNotEqual(d_test, d, "DIctionary is empty")
    def tearDown(self):
        '''Cleaning up after test '''
        del self.config_test

if __name__ == "__main__":
    unittest2.main()

