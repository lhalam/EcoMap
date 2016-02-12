"""Module contains class for test config_builder functions. """

import unittest2
import __builtin__

from StringIO import StringIO
from ecomap import config_builder


CONF_VARS = """
[db_name]
help=Ecomap database name
default=ecomap
type=str
"""

PARSED_DICT = {
'db_name':{
    'help':'Ecomap database name',
    'default':'ecomap',
    'type':'str'}
}

USER_DATA = 'ecomap'

RESULT = {'db_name':'ecomap'}

CONF_VARS_FILE = {'open_file':CONF_VARS}

INPUT_DATA = {'type_config': USER_DATA}

VALUE_CORRECT = 'test_value'

VALUE_INCORRECT = 'test@value'

REGEXP_TO_TEST = r'\w+'


class ContextStringIO(StringIO):

    """Creating a context manager for StringIO"""

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()


def open_mock(fpath):
    """This function mocks path to the file."""
    return ContextStringIO(CONF_VARS_FILE['open_file'])


def raw_input_mock(raw_input_user):
    """This function mocks raw_input_user."""
    return INPUT_DATA['type_config']


def check_regex_mock(first_arg, second_arg):
    """This function mocks check_regex."""
    return True


class ConfigBuilderTestCase(unittest2.TestCase):

    """Class for test config_builder."""

    def setUp(self):
        """Mock initialization."""
        self.raw_input_original = __builtin__.raw_input
        __builtin__.raw_input = raw_input_mock

        self.open_original = __builtin__.open
        __builtin__.open = open_mock

    def tearDown(self):
        """"Mock termination and cleaning up."""
        __builtin__.raw_input = self.raw_input_original

        __builtin__.open = self.open_original

    def test_varsparser_returns_dict(self):
        """Tests if a configuration parsers returns a dictionary."""
        self.assertIsInstance(config_builder.configvars_parser(), dict)

    def test_check_regex_returns_true(self):
        """Tests check_regex returns true value."""
        self.assertTrue(config_builder.check_regex(REGEXP_TO_TEST,
            VALUE_CORRECT))

    def test_check_regex_returns_false(self):
        """Tests check_regex returns false value."""
        self.assertTrue(config_builder.check_regex(REGEXP_TO_TEST,
            VALUE_INCORRECT))

    def test_parse_configvars(self):
        """Tests check configvars_parser returns correct value."""
        self.assertEqual(config_builder.configvars_parser(), PARSED_DICT)

    def test_input_user_data(self):
        """Tests check input_user_data returns correct value."""
        self.check_original = config_builder.check_regex
        config_builder.check_regex = check_regex_mock
        self.assertEqual(config_builder.input_user_data(PARSED_DICT), RESULT)
        config_builder.check_regex = self.check_original


if __name__ == "__main__":
    unittest2.main()
