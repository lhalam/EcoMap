"""Module contains class for test config_builder functions."""

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

PARSED_DICT = {'db_name':{'help':'Ecomap database name',
                          'default':'ecomap',
                          'type':'str'}}

USER_DATA = 'ecomap_db'

RESULT = {'db_name':'ecomap_db'}

CONF_VARS_FILE = {'open_file':CONF_VARS}

INPUT_DATA = {'type_config':USER_DATA}

VALUE_CORRECT = 'test_value'

VALUE_INCORRECT = 'test@value'

REGEXP_TO_TEST = r'\w+'

RES_HASH = "ff9830c42660c1dd1942844f8069b74a"

USER_NAME = "root"

PASSWORD_DB = "root"

KEY = "123"

HOST = "localhost"

VALID_USER_ID = "2"

INVALID_USER_ID = "e"

FIRST_NAME = "ABC"

LAST_NAME = "DEF"

NICKNAME = "ABCDEF"

EMAIL = "admin@mail.ua"

USER_PASSWORD = "12345678"


class ContextStringIO(StringIO):

    """Creating a context manager for StringIO."""

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()

class MySQLdbMock(object):

    """Creating class for mock MySQLdb lib."""

    def __init__(self):
        pass

    def connect(self, host, db_user, db_pasword, db_name):
        return ConnectionMock()

    def Error():
        pass 


class MySQLError(Exception):
    pass


class ConnectionMock(MySQLdbMock):

    """Creating class for mock Connection to db."""

    def cursor(self):
        return CursorMock()

    def commit(self):
        pass

    def close(self):
        pass


class CursorMock(object):

    """Creating class for mock Cursor."""

    def execute(self, query, user_id):
        if user_id != VALID_USER_ID:
            raise MySQLError("Error")


def open_mock(fpath):
    """This function mocks path to the file."""
    return ContextStringIO(CONF_VARS_FILE['open_file'])


def raw_input_mock(raw_input_user):
    """This function mocks raw_input_user."""
    return INPUT_DATA['type_config']


class ConfigBuilderTestCase(unittest2.TestCase):

    """Class for test config_builder."""

    def setUp(self):
        """Mock initialization."""
        self.raw_input_original = __builtin__.raw_input
        __builtin__.raw_input = raw_input_mock

        self.open_original = __builtin__.open
        __builtin__.open = open_mock

        self.original_db = config_builder.MySQLdb
        config_builder.MySQLdb = ConnectionMock()

    def tearDown(self):
        """"Mock termination and cleaning up."""
        __builtin__.raw_input = self.raw_input_original

        __builtin__.open = self.open_original

        config_builder.MySQLdb = self.original_db

    def test_varsparser_returns_dict(self):
        """Tests if a configuration parsers returns a dictionary."""
        self.assertIsInstance(config_builder.configvars_parser(), dict)

    def test_check_regex_true_or_false(self):
        """Tests check_regex true value."""
        self.assertTrue(config_builder.check_regex(REGEXP_TO_TEST,
                                                    VALUE_CORRECT))
        self.assertTrue(config_builder.check_regex(REGEXP_TO_TEST,
                                                    VALUE_INCORRECT))

    def test_parse_configvars(self):
        """Tests check configvars_parser returns correct value."""
        self.assertEqual(config_builder.configvars_parser(), PARSED_DICT)

    def test_input_user_data(self):
        """Tests check input_user_data returns correct value."""
        self.assertEqual(config_builder.input_user_data(PARSED_DICT), RESULT)

    def test_hash_pass(self):
        """Tests if hash function returns correct value."""
        self.assertEqual(config_builder.hash_pass(PASSWORD_DB, KEY), RES_HASH)

    def test_insert_user_raise_error(self):
        """Tests if insert_user raises error."""
        self.assertRaises(MySQLError,config_builder.insert_user, 
                         INVALID_USER_ID, FIRST_NAME, LAST_NAME, 
                           NICKNAME, EMAIL, USER_PASSWORD, HOST,
                              USER_NAME, PASSWORD_DB, USER_DATA)


if __name__ == "__main__":
    unittest2.main()