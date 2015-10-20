"""
This module contains classes to create database connection pool.
Class Pool generates new connections if needed, else returns
connections from Pool.connection_pool. After connection is closed
it returns to Pool.connection_pool.
"""
import threading
import MySQLdb
from ecomap.utils import Singleton

CONNECTION_LIFETIME = 5
HOST = 'localhost'
PORT = 13333
USER = 'root'
PASSWD = 'Phones_13'
DB_NAME = 'ecomap_db'


class Pool(object):
    """
    Usage:
    X = Pool() - inits pool
    X.get_connection() - generates, or returns a connection
    X.return_to_pool(self, connection) - connection we want
                                         return to pool
    """

    __metaclass__ = Singleton

    def __init__(self):
        """
        Initialize of pool object
        """
        self.connection_pool = []
        self.max_size = 10
        self.outer_connections = 0

    def get_connection(self):
        """
        Return new connection if there isn't any connections in
        pool
        """
        if len(self.connection_pool) == 0:
            if self.outer_connections < self.max_size:
                self.outer_connections += 1
                return Connection(self)
            else:
                print 'wait'
        else:
            self.outer_connections += 1
            connection = self.connection_pool.pop()
            connection.timer.cancel()
            return connection

    def return_to_pool(self, connection):
        """
        Returns choosen connection to pool
        """
        if connection not in self.connection_pool:
            self.connection_pool.append(connection)
            self.outer_connections -= 1
            connection.timer.start()


class Connection(object):
    """
    Usage:
    execute(sql) - execute sql command
    return_to_pool - return current instance to pool
    remove - delete current instance from pool
    """

    def __init__(self, pool):
        """
        Initialize of connection, added connection to database,
        added reference to Pool instance
        """
        self.connection = MySQLdb.connect(host=HOST, port=PORT,
                                          user=USER, passwd=PASSWD, db=DB_NAME)
        self.cursor = self.connection.cursor()
        self._pool = pool
        self.timer = None

    def __enter__(self):
        """
        Method which automaticaly is called when we use 'with'
        """
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """
        Method which automaticaly is called when 'with' is ended
        """
        self.return_to_pool()

    def execute(self, sql):
        """
        Method to execute sql command
        """
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def return_to_pool(self):
        """
        Return instance to pool
        """
        self.connection.close()
        self.timer = threading.Timer(CONNECTION_LIFETIME, self.remove)
        self._pool.return_to_pool(self)

    def remove(self):
        """
        Remove instance from pool
        """
        try:
            self._pool.connection_pool.remove(self)
        except ValueError:
            pass


if __name__ == '__main__':
    X = Pool()
    A = X.get_connection()
    B = X.get_connection()
    print 'A is B', A is B
    print 'Pool', X.connection_pool
    print 'Outer', X.outer_connections
    A.return_to_pool()
    print 'Pool', X.connection_pool
    print 'Outer', X.outer_connections
    C = X.get_connection()
    print 'Pool', X.connection_pool
    print 'Outer', X.outer_connections
