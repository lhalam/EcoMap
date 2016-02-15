"""Module which contains Test of DBPool."""

import unittest2

from ecomap.db import db_pool


TEST_INSTANCE = db_pool.DBPool('root', 'root', 'ecomap_db',
                               'localhost', 3306, 5, 3)

CONN_TUPLE = ('root', 'localhost', 3306, 'root',
              'ecomap_db', 'utf8', 'SET NAMES UTF8')


def conn_mock(user, host, port, passwd, db, charset, init_command):
    """This function mocks conn."""
    return CONN_TUPLE


class TestCase(unittest2.TestCase):

    """Class for test db_pool.py"""

    def setUp(self):
        """Setting up for the test"""
        self.conn_original = db_pool.MySQLdb.connect
        db_pool.MySQLdb.connect = conn_mock

    def tearDown(self):
        """Cleaning up after the test"""
        db_pool.MySQLdb.connect = self.conn_original

    def test_create_conn(self):
        """Tests check if connection was created"""
        self.assertEqual(TEST_INSTANCE._create_conn()['connection'],
                         CONN_TUPLE)


if __name__ == "__main__":
    unittest2.main()