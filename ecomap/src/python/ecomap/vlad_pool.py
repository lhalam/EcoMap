#Constant
import MySQLdb
from contextlib import contextmanager
class Pool(object):
	"""docstring for Pool"""
	def __init__(self):
		self.pool_connect=[]
		self.outer_connections=0
		self.max_connect=10
		

	def get_connect(self):
		if not self.pool_connect:
			if len(self.pool_connect) < self.max_connect:
				print "create_connect"
				connect=self.create_connect()
				self.outer_connections += 1
				return connect
			else :
				print "wait"	
		else :

			return self.pool_connect.pop()
			self.outer_connections+=1
		

	def create_connect(self):
		conn=MySQLdb.connect(host="localhost", user="root", passwd="root",db="ecomap_db")
		
		return conn

	@contextmanager	
	def manager(self):
		connect= self.get_connect()
		yield connect

	def close_connect(self):
		for conn in self.pool_connect:
			conn.close()
			self.outer_connections-=1

	def __del__(self):
		self.close_connect()
				
		
			
p=Pool()
generate_conn = p.manager()
with generate_conn as conn:
	print conn
