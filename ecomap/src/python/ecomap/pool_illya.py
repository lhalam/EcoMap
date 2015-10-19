"""
This module contains classes to create database connection pool.
Class Pool generates new connections if needed, else returns
connections from Pool.connection_pool. After connection is closed
it returns to Pool.connection_pool.
"""
from bin.utils import logger
import MySQLdb

HOST = 'localhost'
PORT = 10080
USER = 'root'
PASSWD = 'root'
DB_NAME = 'ecomap_db'


class Singleton(type):
    """
    Metaclass which implements singleton pattern
    """

    def __call__(cls, *args, **kwargs):
        """
        Checks if there is already instance of Pool class.
        If true: return instance, else: create instance
        """
        if not hasattr(cls, '_instance'):
            logger.info('Create instance of pool')
            cls._instance = super(Singleton, cls).__call__(*args, **kwargs)
        logger.info('Return instance of pool')
        return cls._instance


class OutOfConnections(Exception):
    """
    Exception raised if there isn't any free connections
    """
    pass


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
        try:
            if not self.connection_pool:
                if self.outer_connections < self.max_size:
                    self.outer_connections += 1
                    return Connection(self)
                else:
                    raise OutOfConnections
            else:
                self.outer_connections += 1
                connection = self.connection_pool.pop()
                logger.info("Returned connection from database pool")
                return connection
        except OutOfConnections:
            logger.info('Out of free connections')

    def return_to_pool(self, connection):
        """
        Returns choosen connection to pool
        """
        if connection not in self.connection_pool:
            self.connection_pool.append(connection)
            self.outer_connections -= 1


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
        logger.info('Created new connection')
        try:
            self.connection = MySQLdb.connect(host=HOST, port=PORT,
                                              user=USER, passwd=PASSWD,
                                              db=DB_NAME)
        except MySQLdb.OperationalError:
            logger.debug('Error during connection to database')
        self.cursor = self.connection.cursor()
        self._pool = pool

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
        logger.info('Executed some sql code')
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def return_to_pool(self):
        """
        Return instance to pool
        """
        logger.info('Connection returns to database pool')
        self._pool.return_to_pool(self)
