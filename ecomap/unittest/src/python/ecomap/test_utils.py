import unittest2

from ecomap import utils


#input data
TEST_LINE = 20

URL = "stackoverflow.com/questions/34908353/jquery-adding-removing-classes-on-a-button-to-hide-elements"


class TestUtils(unittest2.TestCase):

    """ Class for test utils.py"""
     
    def setUp(self):
        """Setting up for the test."""
        self.test_line = TEST_LINE
        self.url = URL

    def tearDown(self):
        """Cleaning up after the test."""

    def test_return_length_of_random_password(self):
        """Testing if random_password returns a string sum of letters equals length."""
        password = utils.random_password(self.test_line)
        self.assertEqual(len(password),20,"random_password() return not valid password")

    def test_check_password_for_uppercases_lowercases(self):
        """Testing if random_password return a string with lowercases and uppercases."""
        password = utils.random_password(self.test_line)
        test_lower = any(c.islower() for c in password)
        test_upper = any(c.isupper() for c in password)
        self.assertTrue(test_lower, "Test failed:no lowercases")
        self.assertTrue(test_upper, "Test failed:no uppercases")

    def test_if_instance_Singleton(self):
        """Testing if instance is Singleton."""
        self.instance_A = utils.Singleton(int)
        self.instance_B = utils.Singleton(int)
        self.assertTrue(self.instance_A)
        self.assertTrue(self.instance_B)
        self.assertIs(self.instance_A, self.instance_B)

    def test_url_parse_with_agr_true_and_path_none(self):
        """Check function parse_url when get_arg true."""
        arg = True
        path = None
        split_path = "jquery-adding-removing-classes-on-a-button-to-hide-elements" 
        result_url = utils.parse_url(self.url,arg,path)
        self.assertEqual(split_path,result_url)

    def test_url_parse_with_path_true_and_arg_none(self):
        """Check function parse_url when get_path true."""
        arg = None
        path = True
        split_path = "stackoverflow.com/questions/34908353" 
        result_url = utils.parse_url(self.url,arg,path)
        self.assertEqual(split_path,result_url)

    def test_url_parse_with_agr_true_and_path_true(self):
        """Check function parse_url when get_arg true and get_path true."""
        arg = True
        path = True
        split_path = "jquery-adding-removing-classes-on-a-button-to-hide-elements" 
        result_url = utils.parse_url(self.url,arg,path)
        self.assertEqual(split_path,result_url)

    def test_url_parse_with_agr_none_and_path_none(self):
        """Check function parse_url when get_arg none and get_path none."""
        arg = None
        path = None
        split_path = "stackoverflow.com/questions/34908353/jquery-adding-removing-classes-on-a-button-to-hide-elements" 
        result_url = utils.parse_url(self.url,arg,path)
        self.assertEqual(split_path,result_url)

    
if __name__ == "__main__":
    unittest2.main()

