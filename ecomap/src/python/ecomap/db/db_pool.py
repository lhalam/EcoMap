"""This module contains class for creating database connection pool.
Class DBPool generates new connections if needed, else returns
connections from Pool._connection_pool. After connection is closed
it returns to Pool._connection_pool.
"""
import functools
import logging
import MySQLdb
import time
import threading

from contextlib import contextmanager

import ecomap.utils

from ecomap.config import Config

_CONFIG = Config().get_config()
DEFAULT_DELAY = 1
DEFAULT_TRIES = 3


class MySQLPoolSizeError(MySQLdb.DatabaseError):
    """Out of connections error."""
    pass


class DBPoolError(MySQLdb.Error):
    """Custom error for retry decorator. Raises after all tries"""
    pass


def retry_query(tries=DEFAULT_TRIES, delay=DEFAULT_DELAY):
    """Decorator function handling reconnection issues to DB."""
    def retry_wrapper(func):
        """Wrapper function.
           :params: func - function to call
           :return: wrapper function
        """
        @functools.wraps(func)
        def inner(*args, **kwargs):
            """Inner wrapper function
               :params: *args - list of different arguments
                        *kwargs - dictionary of different arguments
            """
            mtries, mdelay = tries, delay
            while True:
                mtries -= 1

                try:
                    return func(*args, **kwargs)
                except MySQLPoolSizeError:
                    logging.getLogger('retry').warn('Out of free connections.',
                                                    exc_info=True)
                except MySQLdb.Error:
                    logging.getLogger('retry').warn('Error', exc_info=True)

                if mtries:
                    time.sleep(mdelay)
                else:
                    raise DBPoolError('Error message: Got error: '
                                      'wrong sql or database pool is out of '
                                      'connections.')
        return inner
    return retry_wrapper


class DBPool(object):
    """DBPool class represents DB pool, which
    handles and manages work with database
    connections.
    """
    __metaclass__ = ecomap.utils.Singleton

    def __init__(self, user, passwd, db_name, host, port, ttl, pool_size):
        self._connection_pool = []
        self.connection_pointer = 0
        self._pool_size = pool_size
        self._host = host
        self._port = port
        self._user = user
        self._passwd = passwd
        self._db_name = db_name
        self.connection_ttl = ttl
        self.log = logging.getLogger('dbpool')
        self.lock = threading.RLock()

    def __del__(self):
        for conn in self._connection_pool:
            self._close_conn(conn)

    def _create_conn(self):
        """Method _create_conn creates connection object.
            returns: dictionary with connection object's properties.
        """
        conn = MySQLdb.connect(user=self._user, host=self._host,
                               port=self._port, passwd=self._passwd,
                               db=self._db_name)
        self.log.info('Created connection object: %s.', conn)
        return {'connection': conn,
                'last_update': 0,
                'creation_date': time.time()}

    def _get_conn(self):
        """Method _get_conn gets connection from the pool or calls.
        method _create_conn if pool is empty.
            returns: opened connection mysql_object.
            raises: PoolSizeError if all connections are busy.
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
        """Generator manager manages work with connections.
            yeilds: opened connection
        """
        with self.lock:
            conn = self._get_conn()

        try:
            yield conn['connection']
        except:
            self._close_conn(conn)
            raise

        if conn['creation_date'] + self.connection_ttl < time.time():
            self._push_conn(conn)
        else:
            self._close_conn(conn)

    def _close_conn(self, conn):
        """Protected method _close_conn closes connection
        before returning it to pool.
            params:
            - conn - specific connection object to be closed
        """
        self.log.info('Closed connection %s with lifetime %s.',
                      conn['connection'], conn['creation_date'])
        self.connection_pointer -= 1
        conn['connection'].close()

    def _push_conn(self, conn):
        """Protected method _push_conn pushes connection to pool.
            params:
            - conn - connection that has to be pushed to pool
        """
        self.log.info('Returning connection %s to pool.', conn['connection'])
        conn['last_update'] = time.time()
        self._connection_pool.append(conn)


db_pool = lambda: DBPool(user=_CONFIG['db.user'],
                         passwd=_CONFIG['db.password'],
                         db_name=_CONFIG['db.db_name'],
                         host=_CONFIG['db.host'],
                         port=_CONFIG['db.port'],
                         ttl=_CONFIG['db.connection_lifetime'],
                         pool_size=_CONFIG['db.pool_size'])
