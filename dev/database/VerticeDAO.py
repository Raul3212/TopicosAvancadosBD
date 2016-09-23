class VerticeDAO:
	
	def __init__(self, __conn):
		self.__conn = __conn
        
	def selectAll(self):
		cur = self.__conn.cursor()
		cur.execute("""SELECT * from vertices""")
		vertices = cur.fetchall()
		cur.close()
		return vertices

	def executeMany(self, vertices):
		cur = self.__conn.cursor()
		cur.executemany("""INSERT INTO vertices (id_vertice, longitude, latitude) VALUES (%s,%s,%s)""", vertices)
		self.__conn.commit()