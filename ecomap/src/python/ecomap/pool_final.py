"""
This module contains class for creating database connection pool.
Class DBPool generates new connections if needed, else returns
connections from Pool._connection_pool. After connection is closed
it returns to Pool._connection_pool.
"""
import logging
import MySQLdb
import time
import threading

from contextlib import contextmanager

from config import Config, Singleton
from utils import get_logger

CONFIG = Config().get_config()
get_logger()

HOST = CONFIG['db.host']
PORT = CONFIG['db.port']
USER = CONFIG['db.user']
PASSWD = CONFIG['db.password']
DB_NAME = CONFIG['db.db_name']
USING_POOL = CONFIG['db.using_pool']
POOL_SIZE = CONFIG['db.pool_size']
CONNECTION_LIFETIME = CONFIG['db.connection_lifetime']
CONNETION_RETRIES = CONFIG['db.connection_retries']
RETRY_DELAY = CONFIG['db.retry_delay']


class OutOfConnectionsError(Exception):
    """
    Exception raised for errors that are related to the
    pool overflow.
    """
    def __init__(self, *args, **kwargs):
        pass


def retry_new(retry=CONNETION_RETRIES, delay=RETRY_DELAY):
    """
    Decorator function handling reconnection issues to DB.
    :param
    - retry - number of attempts to reconnect.
    - delay - time of reconnect attempt delay in seconds.

    """
    def wrapper(method):
        """
        Simple wrapper function
        """
        def temp(self):
            for i in range(retry):
                try:
                    return method(self)
                except OutOfConnectionsError as error:
                    self._log.warn('OUT of connections right now. \
                    Pool will retry to connect in %s sec' % delay)
                    if i is not retry - 1:
                        time.sleep(delay)
                        continue
                    raise error
        return temp
    return wrapper


class DBPool(object):
    """
    DBPool class represents DB pool, which
    handles and manages work with database
    connections.
    """
    __metaclass__ = Singleton

    def __init__(self, user, passwd, db_name, host, port, conn_lifetime, pool_size):
        self._connection_pool = []
        self.connection_pointer = 0
        self._pool_size = pool_size
        self._host = host
        self._port = port
        self._user = user
        self._passwd = passwd
        self._db_name = db_name
        self.connection_open_time = conn_lifetime
        self._log = logging.getLogger('DB_pool')
        self.lock = threading.RLock()

    def __del__(self):
        for conn in self._connection_pool:
            self._close_conn(conn)

    def _create_conn(self):
        """
        Method _create_conn creates connection object.
            :returns dictionary with connection object's properties.

        """
        conn = MySQLdb.connect(user=self._user, passwd=PASSWD,
                               db=self._db_name)
        self._log.info('Created connection object: %s.' % conn)
        return {
            'connection': conn,
            'is_used': 0,
            'TTL': time.time()
        }

    @retry_new(CONNETION_RETRIES, RETRY_DELAY)
    def _get_conn(self):
        """
        Method _get_conn gets connection from the pool or calls.
        method _create_conn if pool is empty.
            :returns opened connection mysql_object.
            :raises OutOfConnectionsError if all connections are busy.

        """
        if [con for con in self._connection_pool if not con['is_used']]:
            connection = self._connection_pool.pop()
            self.connection_pointer += 1
            connection['is_used'] = 1
            self._log.info('Popped connection %s from the pool.'
                           % connection['connection'])
        elif self.connection_pointer < self._pool_size:
            connection = self._create_conn()
            self.connection_pointer += 1
            connection['is_used'] = 1
        else:
            raise OutOfConnectionsError('Out of connections.')
        return connection

    @contextmanager
    def manager(self):
        """
        Generator manager manages work with connections.
            :yeilds opened connection

        """
        with self.lock:
            conn = self._get_conn()
        yield conn
        if not time.time() - conn['TTL'] > self.connection_open_time:
            self._push_conn(conn)
        else:
            self._close_conn(conn)

    def _close_conn(self, conn):
        """
        Protected method _close_conn closes connection
        before returning it to pool.
            params:
            - conn - specific connection object to be closed

        """
        self._log.info('Closed connection %s with lifetime %s.'
                       % (conn['connection'], (time.time() - conn['TTL'])))
        self.connection_pointer -= 1
        conn['connection'].close()

    def _push_conn(self, conn):
        """
        Protected method _push_conn pushes connection to pool.
            params:
            - conn - connection that has to be pushed to pool

        """
        self._log.info('Returning connection %s to pool.' % conn['connection'])
        self.connection_pointer -= 1
        conn['is_used'] = 0
        self._connection_pool.append(conn)
