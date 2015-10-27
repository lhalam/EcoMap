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
from functools import wraps

from ecomap.config import Config
from ecomap.utils import Singleton

CONFIG = Config().get_config()


class MySQLPoolSizeError(MySQLdb.DatabaseError):

    """
    Out of connections error.
    """
    pass


def retry(func):
    """
    Decorator function handling reconnection issues to DB.
    :param
    - retry_quantity - number of attempts to reconnect.
    - delay - time of reconnect attempt delay in seconds.

    """
    @wraps(func)
    def wrapper(retry, delay):
        for i in range(retry):
            try:
                return func()
            except MySQLPoolSizeError as error:
                if i is not retry - 1:
                    time.sleep(delay)
                    continue
            except MySQLdb.DatabaseError as error:
                if i is not retry - 1:
                    time.sleep(delay)
                    continue
            raise error
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
        self.connection_lifetime = ttl
        self.log = logging.getLogger('db_pool')
        self.lock = threading.RLock()

    def __del__(self):
        for conn in self._connection_pool:
            self._close_conn(conn)

    def _create_conn(self):
        """
        Method _create_conn creates connection object.
            :returns dictionary with connection object's properties.

        """
        conn = MySQLdb.connect(user=self._user, host=self._host,
                               port=self._port, passwd=self._passwd,
                               db=self._db_name)
        self.log.info('Created connection object: %s.', conn)
        return {
            'connection': conn,
            'last_update': 0,
            'creation_date': time.time()
        }

    def _get_conn(self):
        """
        Method _get_conn gets connection from the pool or calls.
        method _create_conn if pool is empty.
            :returns opened connection mysql_object.
            :raises PoolSizeError if all connections are busy.

        """
        if self._connection_pool:
            connection = self._connection_pool.pop()
            self.log.info('Popped connection %s from the pool.',
                          connection['connection'])
        elif self.connection_pointer < self._pool_size:
            connection = self._create_conn()
            self.connection_pointer += 1
        else:
            raise MySQLPoolSizeError('Out of connections.')
        return connection

    @contextmanager
    def manager(self):
        """
        Generator manager manages work with connections.
            :yeilds opened connection

        """
        with self.lock:
            conn = self._get_conn()
        yield conn['connection']
        self._push_conn(conn)

    def _close_conn(self, conn):
        """
        Protected method _close_conn closes connection
        before returning it to pool.
            params:
            - conn - specific connection object to be closed

        """
        self.log.info('Closed connection %s with lifetime %s.',
                      (conn['connection'],
                       (time.time() - conn['creation_date'])))
        self.connection_pointer -= 1
        conn['connection'].close()

    def _push_conn(self, conn):
        """
        Protected method _push_conn pushes connection to pool.
            params:
            - conn - connection that has to be pushed to pool

        """
        self.log.info('Returning connection %s to pool.', conn['connection'])
        conn['last_update'] = time.time()
        self._connection_pool.append(conn)


db_pool = lambda: DBPool(user=CONFIG['db.user'], passwd=CONFIG['db.password'],
                         db_name=CONFIG['db.db_name'], host=CONFIG['db.host'],
                         port=CONFIG['db.port'],
                         ttl=CONFIG['db.connection_lifetime'],
                         pool_size=CONFIG['db.pool_size'])
