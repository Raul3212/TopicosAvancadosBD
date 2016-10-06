from model.Vertice import *

class VerticeDAO:
	
	def __init__(self, __conn):
		self.__conn = __conn
        
	def selectAll(self):
		cur = self.__conn.cursor()
		cur.execute("""SELECT id_vertice, latitude, longitude from vertices order by longitude""")
		rows = cur.fetchall()
		cur.close()
		vertices = []
		for row in rows:
			vertice = Vertice(row[0], row[1], row[2])
			vertices.append(vertice)
		return vertices

	def executeMany(self, vertices):
		if(vertices == None):
			return 
		cur = self.__conn.cursor()
		cur.executemany("""INSERT INTO vertices (id_vertice, longitude, latitude) VALUES (%s,%s,%s)""", vertices)
		self.__conn.commit()
		cur.close()

	def selectVerticesId(self):
		cur = self.__conn.cursor()
		cur.execute("""SELECT id_vertice from vertices order by longitude""")
		rows = cur.fetchall()
		cur.close()
		return rows