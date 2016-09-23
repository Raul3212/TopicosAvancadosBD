import psycopg2

class ConnectionFactory:
	
	def getConnection(self):
		try:
		    __conn = psycopg2.connect("dbname='taxistas' user='postgres' host='localhost' password='postgres'")
		    return __conn
		except:
		    print "Error connecting database"
		    return None