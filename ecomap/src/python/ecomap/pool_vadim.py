# coding=utf-8
import time
import MySQLdb
from utils import logger, passw

MAX_POOL_SIZE = 3
CONNECTTION_LIFETIME = 1
USER = 'root'
DB_NAME = 'ecomap_db'


class Singleton(type):
    """
    using a singleton pattern to work with only one possible instance of Pool
    """
    def __call__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            cls._instance = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instance


class Connection(MySQLdb.connection):
# class Connection(object):
    """
    Class returns an instance of MySQLdb connection object.
    This is main interface for work with sql queries.
    Has reference on parent Pool object. Connection lifetime can vary.
    uses constants variables(username,password,db_name) to log-in to specific database.
    """
    def __init__(self, parent_pool, *args, **kwargs):
        # super(Connection, self).__init__(*args, **kwargs)
        self.time_limit = CONNECTTION_LIFETIME
        self.created_time = time.time()
        try:
            self.connection = MySQLdb.connect(user=USER, passwd=passw, db=DB_NAME)
        except Exception, e:
            logger.critical('Error during connection to database > %s' % e)
            raise
        # self.cursor = self.connection.cursor()
        self._pool = parent_pool

    def close(self, *args, **kwargs):
        """
        closes connection if work is finished and returns connection to pool.
        """
        self.connection.commit()
        self.created_time = time.time()
        self._pool.return_to_pool(self)

    def execute(self, sql):
        """
        :param sql: query in SQL syntax
        :return: sql response from database
        """
        self.cursor = self.connection.cursor()
        self.cursor.execute(sql)
        return self.cursor.fetchall()


class Pool(object):
    __metaclass__ = Singleton

    def __init__(self):
        '''

        :return:
        '''
        self.max_size = MAX_POOL_SIZE
        self.CONNECTIONS = []
        self.OUTPUT = []
        self.QUEUE = []
        self.used = len(self.OUTPUT)
        self.actual_conn = len(self.CONNECTIONS)
        self.limit = self.max_size - self.actual_conn - self.used

    def _create_connection(self):
        """
        protected method which creates a Connection instance and returns a full list of active connections
        """
        created_connection = Connection(self)  # creating an instance of connection
        self.CONNECTIONS.append(created_connection)
        self.actual_conn += 1
        return self.CONNECTIONS

    def return_to_pool(self, connection):
        if connection not in self.CONNECTIONS:
            self.CONNECTIONS.append(connection)
            self.OUTPUT.remove(connection)
            self.actual_conn += 1
            self.used -= 1
            logger.info('connection RETURNED to pool and ready to use.'
                        ' STATUS: actual= %s, used = %s, max = %s, limit = %s'
                        % (self.actual_conn, self.used, self.max_size, self.limit))

    def queue(self, user_data):
        return self.QUEUE.append(user_data)

    def _pool_generator(self):
        """
        main generator engine. running in endless loop since generator is started.
        handling connection creating and managing process,
        checks status after each action and making queue from users in a case of pool overflow.
        """
        logger.info('*INITIAL STATUS: actual= %s, used = %s, max = %s, limit = %s'
                    % (self.actual_conn, self.used, self.max_size, self.limit))

        while self.actual_conn < self.max_size:

            if self.actual_conn == 0 and self.used == 0:
                self._create_connection()
                logger.debug('creating an INITIAL connection %s'
                             % self.CONNECTIONS[-1])
                logger.info('STATUS: actual=%s used =%s, limit = %s'
                            % (self.actual_conn, self.used, self.limit))

            elif self.actual_conn == 0 and self.used < self.max_size:
                self._create_connection()
                logger.warning('creating a new connection %s'
                               % self.CONNECTIONS[-1])
                logger.info('STATUS: actual=%s used =%s, limit = %s'
                            % (self.actual_conn, self.used, self.limit))

            elif self.actual_conn > 0 and self.used < self.max_size:
                logger.debug('gave to user an actual free connect.')
                self.actual_conn -= 1
                self.used += 1
                self.limit = self.max_size - self.actual_conn - self.used
                logger.info('*FINISH STATUS: actual=%s used =%s, limit = %s'
                            % (self.actual_conn, self.used, self.limit))
                yield self.OUTPUT.append(self.CONNECTIONS.pop())

            else:
                logger.warning('SORRY! ALL %s CONNECTIONS ARE USED AT THE MOMENT!' % self.used)
                print '|RETRY in 1 second|'
                print '|loop is waiting time to close timed-out connections'
                time.sleep(3)
                gc = [x for x in self.CONNECTIONS if time.time() - x.created_time > x.time_limit]
                print gc
                try:
                    gc = (x.close() for x in self.CONNECTIONS if time.time() - x.created_time > x.time_limit)
                    logger.warning('KILLED %f' % gc.next().created_time)
                    gc.next()

                except StopIteration:
                    logger.info('all connection are busy, retry in .. sec ')
                yield self.queue('putting user data(reference) to queue')

    def get_connection(self):
        """
        starts the loop through generator.
        returns to a user an actual instance of Mysql_DB connection object.
        """
        self._pool_generator().next()
        return self.OUTPUT[-1]


pool = Pool()
c = pool.get_connection()
c2 = pool.get_connection()

print '*' * 80
logger.info('%s>-connection instance_1 created at %f' % (c.connection, c.created_time))
logger.info('%s>-connection instance_2 created at %f' % (c2, c2.created_time))

print c2.connection, '<- OPEN'

print c.execute('show tables;'), '<- execute sql_1'
c.close()
print c2.execute('select * from user;'), '<- execute sql_2'
c2.close()

c3 = pool.get_connection()
c4 = pool.get_connection()
c5 = pool.get_connection()

logger.info('%s>-connection instance_3 created at %f' % (c3.connection, c3.created_time))
logger.info('%s>-connection instance_4 created at %f' % (c4.connection, c4.created_time))
print c3.execute('show tables;')
c3.close()
c4.execute('show tables;')
c4.close()
print '*' * 80

print pool.OUTPUT, '<- output'
print pool.CONNECTIONS, '<- actual free connections'
print pool.actual_conn, '<- actual quantity'
print pool.used, '<- used connections'
print pool.QUEUE, '<- users in QUEUE'

