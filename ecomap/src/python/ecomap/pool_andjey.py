"""
This module contains class for creating database connection pool.
Class DBPool generates new connections if needed, else returns
connections from Pool._connection_pool. After connection is closed
it returns to Pool._connection_pool.
"""
import MySQLdb
import time

from contextlib import contextmanager
from threading import RLock

from config import Config
from utils import logger
from utils import Singleton


CONFIG = Config().get_config()

HOST = CONFIG['db.host']
PORT = CONFIG['db.port']
USER = CONFIG['db.user']
PASSWD = CONFIG['db.password']
DB_NAME = CONFIG['db.db_name']
POOL_SIZE = CONFIG['db.pool_size']
TTL = CONFIG['db.ttl']


class PoolSizeError(Exception):
    """Custom error that triggers if db_pool
    is out of free connections.
    """
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


def retry(tries=3, delay=5):
    """
    Decorator function
    """
    def wrapper(method):
        def innerFunc(self):
            for i in range(tries):
                print 'Try #%s' % str(i+1)
                try:
                    return method(self)
                except:
                    if i is not tries - 1:
                        time.sleep(delay)
                        continue
                    raise
                else:
                    break
        return innerFunc
    return wrapper


class Pool(object):
    """Class which describes pool of connections,
    which handles and organises work with db connections."""

    __metaclass__ = Singleton

    def __init__(self, host, port, user, passwd, db_name, pool_size, TTL):
        self._conns = []
        self._pool_size = pool_size
        self._conn_pointer = 0
        self._host = host
        self._port = port
        self._user = user
        self._passwd = passwd
        self._db_name = db_name
        self._TTL = TTL
        self._lock = RLock()
        self._log = logger

    def __del__(self):
        for conn in self._conns:
            self._close_conn(conn)

    def _create_conn(self):
        """Method _create_conn opens conncetion to db.
            :returns dictionary with connection, in_use boolean
            and creation_time
        """
        connection = MySQLdb.connect(user=self._user, passwd=self._passwd,
                                     db=self._db_name, host=self._host,
                                     port=self._port)
        conn = {
            'conn': connection,
            'in_use': False,
            'creation_time': time.time()
        }
        self._conn_pointer += 1
        self._log.info("Created new connection %s." % conn['conn'])
        return conn

    @retry()
    def _get_conn(self):
        """Method _get_conn gets connection from pool
        or gets it from method _create_conn if pool is empty.
            :returns dictionary with connection, in_use boolean
            and creation_time
            :raises PoolSizeError
        """
        conn = None
        if self._conns:
            self._log.info("Popped connection from pool")
            conn = self._conns.pop()
        elif self._conn_pointer < self._pool_size:
            conn = self._create_conn()
        else:
            raise PoolSizeError("Out of free connections.")
        return conn

    # retry - implement
    @contextmanager
    def manager(self):
        """Generator manager manages and handles
        all work with connections to db.
            :yeilds connection dict(conn, in_use,
             creation_time)
        """
        with self._lock:
            conn = self._get_conn()
        conn['in_use'] = True
        yield conn['conn']
        conn['in_use'] = False
        if conn['creation_time'] + self._TTL < time.time():
            self._close_conn(conn)
        else:
            self._push_conn(conn)

    def _close_conn(self, conn):
        """Method _close_conn closes connection.
        """
        self._conn_pointer -= 1
        self._log.info("Closing connection %s." % conn['conn'])
        conn['conn'].close()
        del conn

    def _push_conn(self, conn):
        """Method _push_conn pushes connections back
        to pool.
        """
        self._log.info("Pushing connection %s to the pool." % conn['conn'])
        self._conns.append(conn)

if __name__ == "__main__":
    db_pool = Pool(HOST, PORT, USER, PASSWD, "DB_NAME",
                   POOL_SIZE, TTL)
    with db_pool.manager() as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM user;")
        print cur.fetchall()
