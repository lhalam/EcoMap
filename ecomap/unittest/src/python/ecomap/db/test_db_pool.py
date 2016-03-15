"""Module which contains Test of DBPool."""

import time
import unittest2

from ecomap.db import db_pool
from inspect import isfunction


CONN = {'connection':'mocked connection',
        'last_update': 0,
        'creation_date': 2.0}


class MySQLdbMock(object):

    """Creating class for mock MySQLdb lib."""

    def __init__(self):
        pass


class ConnectionMock(MySQLdbMock):

    """Creating class for mock Connection to db."""

    def connect(self, user, host, port, passwd, db, charset, init_command):
        return 'mocked connection'


class TestCase(unittest2.TestCase):

    """Class for test db_pool.py."""

    def setUp(self):
        """Setting up for the test."""
        self.original_MySQLdb = db_pool.MySQLdb
        db_pool.MySQLdb = ConnectionMock()

    def tearDown(self):
        """Cleaning up after the test."""
        db_pool.MySQLdb = self.original_MySQLdb

    def test_retry_query(self):
        """Tests decorator retry_query success."""
        @db_pool.retry_query()
        def retry_success():
            return "SUCCESS"
        self.assertEqual(retry_success(), "SUCCESS")
        self.assertTrue(isfunction(retry_success))

    def test_retry_query_errors(self):
        """Tests decorator retry_query errors."""
        self.assertRaises(TypeError, db_pool.retry_query(0, 1))

    def test_create_conn(self):
        """Tests check if connection was created."""
        POOL = db_pool.DBPool('root', 'root', 'ecomap_db',
                                   'localhost', 3306, 5, 3)
        self.assertEqual(POOL._create_conn()['connection'],
                                        CONN['connection'])
        self.assertIsInstance(POOL._create_conn(), dict)

    def test_get_conn_add(self):
        """Tests get conn to add conn."""
        POOL = db_pool.DBPool('root', 'root', 'ecomap_db',
                                   'localhost', 3306, 5, 3)
        POOL._connection_pool = []
        POOL.connection_pointer = 0
        self.assertTrue(POOL._get_conn)

    def test_get_conn_pop(self):
        """Tests get conn to pop conn."""
        POOL = db_pool.DBPool('root', 'root', 'ecomap_db',
                                   'localhost', 3306, 5, 3)
        POOL._connection_pool = [CONN]
        self.assertTrue(POOL._get_conn())

    def test_get_conn_error(self):
        """Tests get_conn error."""
        POOL = db_pool.DBPool('root', 'root', 'ecomap_db',
                                   'localhost', 3306, 5, 0)
        POOL._connection_pool = []
        POOL.connection_pointer = 5
        self.assertRaises(TypeError, POOL._get_conn,
            POOL.connection_pointer, POOL._connection_pool)

    def test_push_conn(self):
        """Tests push_conn."""
        POOL = db_pool.DBPool('root', 'root', 'ecomap_db',
                                   'localhost', 3306, 5, 3)
        POOL._connection_pool = []
        conn = POOL._create_conn()
        POOL._push_conn(conn)
        self.assertTrue(POOL._connection_pool)

    def test_close_conn(self):
        """Tests close_conn."""
        POOL = db_pool.DBPool('root', 'root', 'ecomap_db',
                                   'localhost', 3306, 5, 0)
        POOL.connection_pointer = 0
        self.assertTrue(POOL._close_conn)

    def test_manager_close_conn(self):
        """Tests manager for close conn."""
        POOL = db_pool.DBPool('root', 'root', 'ecomap_db',
                                   'localhost', 3306, 1, 1)
        POOL._connection_pool = [CONN]
        POOL.connection_pointer = 0
        try:
            with POOL.manager():
                time.sleep(2)
        except:
            raise
        self.assertListEqual([CONN], POOL._connection_pool)
    
    def test_transaction_close_conn(self):
        """Tests transaction for close conn."""
        POOL = db_pool.DBPool('root', 'root', 'ecomap_db',
                                   'localhost', 3306, 1, 1)
        POOL._connection_pool = [CONN]
        POOL.connection_pointer = 0
        try:
            with POOL.manager():
                time.sleep(2)
        except:
            raise
        self.assertListEqual([CONN], POOL._connection_pool)


if __name__ == "__main__":
    unittest2.main()


