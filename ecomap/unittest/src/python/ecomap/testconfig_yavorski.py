import unittest2
from ecomap.config import Config



class ConfigParserTestCase(unittest2.TestCase):

    def setUp(self):
        """This method is for receiving configurations to test"""
        print "\n In setUp()"
        self.configs = Config()

    def test_is_dict(self):
        """Testing if configuration parsers return a dictionary"""
        # print self.configs.get_config()
        self.assertEqual(type(self.configs.get_config()), type({}))

    def test_is_file(self):
        # print self.configs.path
        """Testing whether a file is a config file"""
        path = self.configs.path.split('.')
        self.assertEqual(path[1], 'conf', msg="This is not a configuration file")

    def test_sections(self):
        """Testing if file is divided by sections"""



    def tearDown(self):
        """This method is for cleaning up after testing is done"""
        print 'In tearDown()\n'
        del self.configs

if __name__ == '__main__':
    unittest2.main()
