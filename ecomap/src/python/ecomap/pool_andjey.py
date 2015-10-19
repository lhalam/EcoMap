import MySQLdb
import sys

# CONNECTION_LIFETIME = 5
HOST = "localhost"
PORT = 13306
USER = 'root'
PASSWD = 'root'
DB_NAME = 'ecomap_db'

# TODO
# turn on logging
# docs here


class Singleton(type):

    """
    Metaclass which implements singleton pattern.
    """
    def __call__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            cls._instance = super(
                Singleton, cls).__call__(*args, **kwargs)
        return cls._instance


class Pool(object):
    """Class which describes pool of connections.
    This class organises and controles the work with DB.
    It takes number max_size as the parameter. This
    number is limit of connections, which can be created"""
    __metaclass__ = Singleton

    def __init__(self, max_size=10):
        self.connections = []
        self.MAX_SIZE = max_size
        self.active_conn = 0

    def get_conn(self):
        """This method returnes PooledConnection instance.
        If pool is empty and number of active connections is
        below max_size than it will create and return new connection.
        If there are connections in pool, it will pop and return
        connection from the pool."""
        if not self.connections:  # work on it
            if self.active_conn < self.MAX_SIZE:
                self.active_conn += 1
                return PooledConnection(self)
            else:
                raise Exception("There is limited number of connections")
        else:
            self.active_conn += 1
            return self.connections.pop()

    def return_conn(self, conn):
        """This method accepts used connection back to pool."""
        self.connections.append(conn)

    def _clean_pool(self):
        """This method cleans up the pool before the
        end of the work of pool."""
        for conn in self.connections:
            conn.kill_conn()

    def __exit__(self):
        self._clean_pool()


class PooledConnection(object):
    """This class is wrapper for standart MySQLdb connection.
    It takes the reference on pool as it's first argument.
    """
    def __init__(self, pool):
        try:
            self.conn = MySQLdb.connect(host=HOST, port=PORT,
                                        user=USER, passwd=PASSWD, db=DB_NAME)
        except:
            print "Unexpected error: ", sys.exc_info()[0]
            raise
        self.pool = pool

    def kill_conn(self):
        """This method closes the PooledConnection."""
        try:
            self.conn.close()
        except:
            print "Unexpected error: ", sys.exc_info()[0]
            raise

    def return_to_pool(self):
        """This method returns the connection to the pool"""
        self.pool.return_conn(self)

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.return_to_pool()


if __name__ == "__main__":
    # working with connection
    db_pool = Pool(2)
    conn1 = db_pool.get_conn()
    conn2 = db_pool.get_conn()
    # conn3 = db_pool.get_conn() # raises exception of limit

    # is it okay???
    # solutions: remap methods or overload them in wrapper class
    cursor = conn1.conn.cursor()
    cursor.execute("SELECT * FROM user;")
    print cursor.fetchall()
    cursor.close()
    conn1.return_to_pool()

    with db_pool.get_conn() as conn:
        print conn

    conn2.return_to_pool()
