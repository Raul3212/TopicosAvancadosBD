class RotasDAO:
	
	def __init__(self, __conn):
		self.__conn = __conn
        
	def selectAll(self):
		cur = self.__conn.cursor()
		cur.execute("""SELECT * from rotas""")
		vertices = cur.fetchall()
		cur.close()
		return vertices

	def executeMany(self, rotas):
		cur = self.__conn.cursor()
		cur.executemany("""INSERT INTO rotas (id_edge, id_source, id_target, cost) VALUES (%s,%s,%s,%s)""", rotas)
		self.__conn.commit()