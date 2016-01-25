"""Module which contains Test of Utils functions. """

import re
import unittest2

from ecomap import utils


#input data
PASSWORD_LENGTH = 20
URL = "path/to/string/to/test"


class TestUtils(unittest2.TestCase):

    """ Class for test utils.py"""

    def setUp(self):
        """Setting up for the test."""

    def tearDown(self):
        """Cleaning up after the test."""

    def test_length_of_random_password(self):
        """Testing random_password for string length."""
        password = utils.random_password(PASSWORD_LENGTH)
        self.assertEqual(len(password), PASSWORD_LENGTH)

    def test_password_upper_lowercases(self):
        """Testing random_password for lower-& uppercases."""
        password = utils.random_password(PASSWORD_LENGTH)
        lower = any(c.islower() for c in password)
        upper = any(c.isupper() for c in password)
        self.assertTrue(lower, "Test failed:no lowercases")
        self.assertTrue(upper, "Test failed:no uppercases")

    def test_if_instance_singleton(self):
        """Testing if instance is Singleton."""
        class ChildFirst(utils.Singleton):
            """child singleton """
            pass
        class ChildSecond(utils.Singleton):
            """child singleton """
            pass
        first_instance = ChildFirst(type)
        second_instance = ChildSecond(type)
        self.assertIs(first_instance, second_instance)

    def test_url_parse_with_agr_true(self):
        """Check function parse_url when get_arg true."""
        split_path = "".join(re.findall(r"\w+$", URL))
        self.assertEqual(utils.parse_url(URL, True, False), split_path)

    def test_url_parse_with_path_true(self):
        """Check function parse_url when get_path true."""
        split_path = '/'.join(URL.split('/')[:-1])
        self.assertEqual(utils.parse_url(URL, False, True), split_path)

    def test_url_parse_args_true(self):
        """Check function parse_url get_arg and get_path true."""
        split_path = "".join(re.findall(r"\w+$", URL))
        self.assertEqual(utils.parse_url(URL, True, True), split_path)

    def test_url_parse_agrs_none(self):
        """Check function parse_url get_arg and get_path none."""
        self.assertEqual(utils.parse_url(URL, False, False), URL)


if __name__ == "__main__":
    unittest2.main()