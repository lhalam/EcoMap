import MySQLdb
import time
import threading
from contextlib import contextmanager

class Pool(object):
	
	def __init__(self):
		self.pool_connect=[]
		self.outer_connections=0
		self.max_connect=10
		self.connect_ttl=1
		

	def get_connect(self):
		print not self.pool_connect
		if not self.pool_connect:
			if len(self.pool_connect) < self.max_connect:
				connect=self.create_connect()
				self.outer_connections += 1
				return connect
			else :
				raise	
		else :

			return self.pool_connect.pop()
			self.outer_connections+=1
		

	def create_connect(self):
		print "create_connect"
		conn=MySQLdb.connect(host="localhost", user="root", passwd="root",db="ecomap_db")
		connection = {
		'connect':conn,
		'isUsed':True,
		'openTime':time.time()
		}
		return connection

	@contextmanager	
	def manager(self):
		connect= self.get_connect()
		yield connect

		if connect["openTime"] +self.connect_ttl < time.time():
			self.pool_connect.append(connect)


	def close_connect(self):
		for conn in self.pool_connect:
			conn['connect'].close()
			self.outer_connections-=1

	def __del__(self):
		print "del"
		self.close_connect()


#TEST	
p=Pool()

generate_conn1 = p.manager()
with generate_conn1 as conn :
	print conn['connect']

generate_conn2 = p.manager()

with generate_conn2 as conn2 :
	time.sleep(2)
	print conn2['connect']

generate_conn3 = p.manager()
with generate_conn3 as conn3 :
	print conn3['connect']	
