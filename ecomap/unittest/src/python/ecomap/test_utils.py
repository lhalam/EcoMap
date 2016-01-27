"""Module which contains Test of Utils functions. """

import unittest2

from ecomap import utils
from urlparse import urlparse


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
        self.assertTrue(lower)
        self.assertTrue(upper)

    def test_if_instance_singleton(self):
        """Testing if instance is Singleton."""
        class SingleChild(object):
            """metaclass singleton"""
            __metaclass__ = utils.Singleton
        first_instance = SingleChild()
        second_instance = SingleChild()
        self.assertIs(first_instance, second_instance)

    def test_url_parse_with_agr_true(self):
        """Check function parse_url when get_arg true."""
        split_path = urlparse(URL).path.split('/')[-1]
        self.assertEqual(utils.parse_url(URL, True, False), split_path)

    def test_url_parse_with_path_true(self):
        """Check function parse_url when get_path true."""
        split_path = '/'.join(urlparse(URL).path.split('/')[:-1])
        self.assertEqual(utils.parse_url(URL, False, True), split_path)

    def test_url_parse_args_true(self):
        """Check function parse_url get_arg and get_path true."""
        split_path = urlparse(URL).path.split('/')[-1]
        self.assertEqual(utils.parse_url(URL, True, True), split_path)

    def test_url_parse_agrs_none(self):
        """Check function parse_url get_arg and get_path none."""
        self.assertEqual(utils.parse_url(URL, False, False), URL)


if __name__ == "__main__":
    unittest2.main()

