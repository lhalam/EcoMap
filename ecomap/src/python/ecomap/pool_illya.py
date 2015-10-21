"""
This module contains classes to create database connection pool.
Class Pool generates new connections if needed, else returns
connections from Pool.connection_pool. After connection is closed
it returns to Pool.connection_pool.
"""
import MySQLdb
from contextlib import contextmanager
from ecomap.config import Config
from ecomap.utils import logger

CONFIG = Config().get_config()


class DBPool(object):

    def __init__(self):
        self.close = CONFIG['db.close']
        self.connection_pool = []
        self.db_name = CONFIG['db.db_name']
        self.host = CONFIG['db.host']
        self.log = logger
        self.outer_connections = 0
        self.pswd = CONFIG['db.password']
        self.pool_size = CONFIG['db.pool_size']
        self.port = CONFIG['db.port']
        self.user = CONFIG['db.user']

    def __del__(self):
        for conn in self.connection_pool:
            self.close_conn(conn)

    def create_conn(self):
        self.log.info('Creating connection')
        try:
            connection = MySQLdb.connect(user=self.user, passwd=self.pswd,
                                         db=self.db_name, host=self.host,
                                         port=self.port)
            return connection.cursor()
        except MySQLdb.OperationalError, error:
            self.log.info('Wrong connection parameters')
            print error
            raise

    def get_conn(self):
        self.log.info('Getting connection')
        if not self.connection_pool:
            if self.outer_connections < self.pool_size:
                connection = self.create_conn()
                self.outer_connections += 1
                return connection
            else:
                self.log.info('Out of connections')
                raise Exception
        else:
            self.log.info('Getting connection from pool')
            self.outer_connections += 1
            return self.connection_pool.pop()

    @contextmanager
    def manager(self):
        connection = self.get_conn()
        yield connection
        if self.close:
            self.close_conn(connection)
        else:
            self.push_conn(connection)

    def close_conn(self, connection):
        self.log.info('Close connection')
        self.outer_connections -= 1
        connection.close()

    def push_conn(self, connection):
        self.log.info('Returning connection to pool')
        self.outer_connections -= 1
        self.connection_pool.append(connection)
