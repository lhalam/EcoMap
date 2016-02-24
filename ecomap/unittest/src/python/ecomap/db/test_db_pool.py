"""Module which contains Test of DBPool."""

import MySQLdb
import unittest2

from ecomap.db.db_pool import retry_query, DBPool, DBPoolError, \
MySQLPoolSizeError


TRIES = 3

COUNT_TRIES = 1

CONDITION_RAISE = True


class ConnectionDB(object):

    """Creating class for connection to db."""

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()


def connect_mock(user, host, port, passwd, db, charset, init_command):
    """This function mocks connect."""
    return ConnectionDB()


@retry_query(TRIES, delay=1)
def retry_func():
    """Decorator function handling reconnection issues to DB."""
    global CONDITION_RAISE
    if CONDITION_RAISE == True:
        global COUNT_TRIES
        COUNT_TRIES += 1
        if COUNT_TRIES == 3:
            CONDITION_RAISE = False
        raise MySQLPoolSizeError()
    return COUNT_TRIES


@retry_query(TRIES, delay=1)
def PoolSizeError(Error):
    """Function raise error"""
    raise MySQLPoolSizeError()


class TestCase(unittest2.TestCase):

    """Class for test db_pool.py."""

    def setUp(self):
        """Setting up for the test."""
        global POOL
        global MySQLdb
        self.original_db = MySQLdb.connect
        MySQLdb.connect = connect_mock
        POOL = DBPool('root', 'root', 'ecomap_db', 'localhost', 3306, 5, 3)

    def tearDown(self):
        """Cleaning up after the test."""
        global POOL
        MySQLdb.connect = self.original_db
        del POOL

    def test_retry_query(self):
        """Tests decorator retry_query."""
        self.assertEqual(TRIES, retry_func())

    def test_create_conn(self):
        """Tests check if connection was created."""
        self.assertTrue(DBPool._create_conn(POOL))
        self.assertIsInstance(DBPool._create_conn(POOL), dict)

    def test_retry_query_error(self):
        """Tests retry query error."""
        CONDITION = False
        try:
            PoolSizeError(True)
        except DBPoolError:
            CONDITION = True
        self.assertTrue(CONDITION)

    def test_get_conn_add(self):
        """Tests get conn to add conn."""
        POOL._connection_pool = []
        POOL.pool_size = 5
        POOL.connection_pointer = 0
        self.assertTrue(POOL._create_conn)

    def test_get_conn_pop(self):
        """Tests get conn to pop conn."""
        POOL._push_conn(POOL._create_conn())
        connection = POOL._get_conn()
        self.assertTrue(connection)

    def test_get_conn_error(self):
        """Tests get_conn error."""
        POOL._connection_pool = []
        POOL.connection_pointer = 5
        POOL.pool_size_error = 0
        with self.assertRaises(MySQLdb.DatabaseError):
            POOL._get_conn()

    def test_push_conn(self):
        """Tests push_conn."""
        conn = POOL._create_conn()
        POOL._push_conn(conn)
        self.assertTrue(POOL._connection_pool)

    def test_manager(self):
        """Tests manager for push_conn."""
        POOL._connection_pool = []
        POOL.connection_pointer = 0
        POOL.pool_size_error = 5
        conn = POOL._get_conn()
        conn['creation_date'] = 0
        POOL._push_conn(conn)
        self.assertFalse(POOL._push_conn(conn))


if __name__ == "__main__":
    unittest2.main()