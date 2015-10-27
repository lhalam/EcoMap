"""
This module contains class for creating database connection pool.
Class DBPool generates new connections if needed, else returns
connections from Pool._connection_pool. After connection is closed
it returns to Pool._connection_pool.
"""
import MySQLdb
from contextlib import contextmanager

from ecomap.config import Config
from ecomap.utils import logger

CONFIG = Config().get_config()

HOST = CONFIG['db.host']
PORT = CONFIG['db.port']
USER = CONFIG['db.user']
PASSWD = CONFIG['db.password']
DB_NAME = CONFIG['db.db_name']
USING_POOL = CONFIG['db.using_pool']
POOL_SIZE = CONFIG['db.pool_size']


class DBPool(object):
    """
    DBPool class represents DB pool, which
    handles and manages work with database
    connections.
    """
    def __init__(self, host, port, user, passwd,
                 db_name, using_pool, pool_size):
        self._connection_pool = []
        self._outer_connections = 0
        self._pool_size = pool_size
        self._host = host
        self._port = port
        self._user = user
        self._passwd = passwd
        self._db_name = db_name
        self.using_pool = using_pool
        self._log = logger

    def __del__(self):
        for conn in self._connection_pool:
            self._close_conn(conn)

    def _create_conn(self):
        """
        Method _create_conn creates connection object.
            :returns opened connection
            :raises MySQLdb.OperationalError
        """
        try:
            conn = MySQLdb.connect(user=self._user, passwd=self._passwd,
                                   db=self._db_name, host=self._host,
                                   port=self._port)
            self._log.info('Created connection object: {0}'.format(conn))
            return conn
        except MySQLdb.OperationalError, error:
            self._log.info('Wrong connection parameters. Detailed: {0}'
                           .format(error))
            raise

    def _get_conn(self):
        """
        Method _get_conn gets connection from the pool or from
        method _create_conn if pool is empty.
            :returns opened connection
            :raises Exception if all connectionsare busy
        """
        if not self._connection_pool:
            if self._outer_connections < self._pool_size:
                conn = self._create_conn()
                self._outer_connections += 1
                return conn
            else:
                self._log.info('Out of connections')
                raise Exception('Out of connections')
        else:
            conn = self._connection_pool.pop()
            self._outer_connections += 1
            self._log.info('Popped connection {0} from the pool'
                           .format(conn))
            return conn

    @contextmanager
    def manager(self):
        """
        Generator manager manages work with connections.
            :yeilds opened connection
        """
        conn = self._get_conn()
        yield conn
        if not self.using_pool:
            self._close_conn(conn)
        else:
            self._push_conn(conn)

    def _close_conn(self, conn):
        """
        Method _close_conn closes connection.
            params:
            - conn - connection that has to be closed
        """
        self._log.info('Closed connection {0}'.format(conn))
        self._outer_connections -= 1
        conn.close()

    def _push_conn(self, conn):
        """
        Method _push_conn pushes connection to pool.
            params:
            - conn - connection that has to be pushed to pool
        """
        self._log.info('Returning connection {0} to pool'.format(conn))
        self._outer_connections -= 1
        self._connection_pool.append(conn)
