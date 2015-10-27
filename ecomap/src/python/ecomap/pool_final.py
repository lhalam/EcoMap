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

from config import Config
from utils import get_logger, Singleton

CONFIG = Config().get_config()
get_logger()

HOST = CONFIG['db.host']
PORT = CONFIG['db.port']
USER = CONFIG['db.user']
PASSWD = CONFIG['db.password']
DB_NAME = CONFIG['db.db_name']
POOL_SIZE = CONFIG['db.pool_size']
CONNECTION_TTL = CONFIG['db.connection_lifetime']
CONNETION_RETRIES = CONFIG['db.connection_retries']
RETRY_DELAY = CONFIG['db.retry_delay']


class PoolSizeError(Exception):
    """
    Exception raised for errors that are related to the
    pool overflow.
    """
    def __init__(self, *args, **kwargs):
        pass


def retry(retry_quantity=CONNETION_RETRIES, delay=RETRY_DELAY):
    """
    Decorator function handling reconnection issues to DB.
    :param
    - retry_quantity - number of attempts to reconnect.
    - delay - time of reconnect attempt delay in seconds.

    """
    def wrapper(method):
        def inner(self):
            for i in range(retry_quantity):
                try:
                    return method(self)
                except PoolSizeError as error:
                    self._log.warn('OUT of connections right now. \
                    Pool will retry_quantity to connect in %s sec' % delay)
                    if i is not retry_quantity - 1:
                        time.sleep(delay)
                        continue
                    raise error
        return inner
    return wrapper


class DBPool(object):
    """
    DBPool class represents DB pool, which
    handles and manages work with database
    connections.
    """
    __metaclass__ = Singleton

    def __init__(self, user, passwd, db_name, host, port, ttl, pool_size):
        self._connection_pool = []
        self.connection_pointer = 0
        self._pool_size = pool_size
        self._host = host
        self._port = port
        self._user = user
        self._passwd = passwd
        self._db_name = db_name
        self.ttl = ttl
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
        conn = MySQLdb.connect(user=self._user, host=HOST, port=PORT, passwd=PASSWD,
                               db=self._db_name)
        self._log.info('Created connection object: %s.' % conn)
        return {
            'connection': conn,
            'is_used': 0,
            'creation_date': time.time()
        }

    @retry(CONNETION_RETRIES, RETRY_DELAY)
    def _get_conn(self):
        """
        Method _get_conn gets connection from the pool or calls.
        method _create_conn if pool is empty.
            :returns opened connection mysql_object.
            :raises PoolSizeError if all connections are busy.

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
            raise PoolSizeError('Out of connections.')
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
        if not time.time() - conn['creation_date'] > self.ttl:
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
                       % (conn['connection'], (time.time() - conn['creation_date'])))
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

pool_obj = DBPool(USER, PASSWD, DB_NAME, HOST, PORT, CONNECTION_TTL, POOL_SIZE)
