import threading
import MySQLdb

CONNECTION_LIFETIME = 10


class Singleton(type):

    def __call__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            cls._instance = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instance


class Pool(object):

    __metaclass__ = Singleton

    def __init__(self):
        self.connection_pool = []
        self.max_size = 10
        self.outer_connections = 0

    def get_connection(self):
        if len(self.connection_pool) == 0:
            if self.outer_connections < self.max_size:
                self.outer_connections += 1
                return Connection(self)
            else:
                print 'wait'
        else:
            self.outer_connections += 1
            return self.connection_pool.pop()

    def return_to_pool(self, connection):
        if connection not in self.connection_pool:
            self.connection_pool.append(connection)
            self.outer_connections -= 1
            threading.Timer(CONNECTION_LIFETIME, connection.remove).start()


class Connection(object):

    def __init__(self, pool):
        self._pool = pool
        self.cursor = None
        self.connection = MySQLdb.connect(user='root', passwd='Phones_13',
                                          db='ecomap_db')

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.connection.close()
        self.return_to_pool()

    def execute(self, sql):
        self.cursor = self.connection.cursor()
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def return_to_pool(self):
        self._pool.return_to_pool(self)

    def remove(self):
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
