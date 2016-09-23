class TaxistaDAO:
	
	def __init__(self, __conn):
		self.__conn = __conn
        
	def selectAll(self):
		cur = self.__conn.cursor()
		cur.execute("""SELECT * from taxistas""")
		return cur.fetchall()

	def executeMany(self, vertices):
		cur = self.__conn.cursor()
		cur.executemany("""INSERT INTO taxistas (id_driver, tempo, longitude, latitude) VALUES (%s, %s, %s,%s)""", vertices)
		self.__conn.commit()