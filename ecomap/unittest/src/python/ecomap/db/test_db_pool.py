"""Module which contains Test of DBPool."""

import time
import unittest2

from ecomap.db import db_pool
from inspect import isfunction 


CONN = {'connection': 'mocked connection', 
        'last_update': 0,
        'creation_date': 200.0}

class Connection_mock:

    """Creating class for mock connection to db."""

    def __init__(self):
        pass
    
    def __repr__(self):
        return "'mocked connection'"
    
    def close(self):
        self.closed = True

class MySQLdb_mock:

    """Creating class for mocking MySQLdb."""

    def __init__(self):
        pass

    def connect(self, user, host, port, passwd, db, charset,init_command):
        return Connection_mock()

class Time_mock:

    """Creating class for mocking time."""

    def timer(self):
        return 200.0

@db_pool.retry_query()
def retry_success():
    return "SUCCESS"

@db_pool.retry_query()
def retry_MySQLPoolSizeError(self):
    raise MySQLPoolSizeError()

@db_pool.retry_query()
def retry_MySQLdbError(self):
    raise MySQLdb.Error()


class TestCase(unittest2.TestCase):

    """Class for test db_pool.py."""

    def setUp(self):
        """Setting up for the test."""
        self.POOL = db_pool.DBPool('root', 'root', 'ecomap_db',
                                   'localhost', 3306, 5, 3)

    def tearDown(self):
        """Cleaning up after the test."""
        del self.POOL

    def test_retry_query(self):
        """Tests decorator retry_query success."""
        self.assertEqual(retry_success(), "SUCCESS")
        self.assertTrue(isfunction(retry_success))

    def test_retry_query_errors(self):
        """Tests decorator retry_query errors."""
        exceptDBErr = False
        try:
            retry_MySQLPoolSizeError()
        except:
            exceptDBErr = True
        exceptMySqlErr = False
        try:
            retry_MySQLdbError(True)
        except:
            exceptMySqlErr = True
        self.assertTrue(exceptDBErr)
        self.assertTrue(exceptMySqlErr)

    def test_create_conn(self):
        """Tests check if connection was created."""
        self.original_MySQLdb = db_pool.MySQLdb
        db_pool.MySQLdb = MySQLdb_mock()
        self.original_time = db_pool.time.time
        db_pool.time.time = Time_mock().timer        
        self.assertEqual(db_pool.DBPool()._create_conn(), CONN)
        self.assertIsInstance(db_pool.DBPool()._create_conn(), dict)
        db_pool.MySQLdb = self.original_MySQLdb
        db_pool.time.time = self.original_time

    def test_get_conn_add(self):
        """Tests get conn to add conn."""
        self.POOL._connection_pool = []
        self.POOL.pool_size = 5
        self.POOL.connection_pointer = 0
        self.assertTrue(self.POOL._create_conn)

    def test_get_conn_pop(self):
        """Tests get conn to pop conn."""
        self.POOL._push_conn(self.POOL._create_conn()) 
        self.assertTrue(self.POOL._get_conn())

    def test_get_conn_error(self):
        """Tests get_conn error."""
        self.POOL._connection_pool = []
        self.POOL.connection_pointer = 5
        self.POOL.pool_size = 0
        self.assertRaises(TypeError, self.POOL._get_conn())

    def test_push_conn(self):
        """Tests push_conn."""
        self.POOL._connection_pool = []
        conn = self.POOL._create_conn()
        self.POOL._push_conn(conn)
        self.assertTrue(self.POOL._connection_pool)

    def test_close_conn(self):
        """Tests close_conn."""
        self.POOL.connection_pointer = 1
        self.assertIsNone(self.POOL._close_conn
                         (db_pool.DBPool()._create_conn()))

    def test_manager_close_conn(self):
        """Tests manager for close conn."""
        self.POOL._connection_pool = []
        self.POOL.connection_pointer = 0
        self.POOL.pool_size = 0
        try:
            with self.POOL.manager():
                time.sleep(2)
        except:
            raise
        self.assertListEqual([], self.POOL._connection_pool)


if __name__ == "__main__":
    unittest2.main()
