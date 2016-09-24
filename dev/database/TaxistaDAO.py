from model.Taxista import *

class TaxistaDAO:
	
	def __init__(self, __conn):
		self.__conn = __conn
        
	def selectAll(self):
		cur = self.__conn.cursor()
		cur.execute("""SELECT id_driver, tempo, longitude, latitude from taxistas""")
		rows = cur.fetchall()
		taxistas = []
		for row in rows:
			taxista = Taxista(row[0], row[1], row[2], row[3])
			taxistas.append(taxista)
		return taxistas

	def executeMany(self, vertices):
		cur = self.__conn.cursor()
		cur.executemany("""INSERT INTO taxistas (id_driver, tempo, longitude, latitude) VALUES (%s, %s, %s,%s)""", vertices)
		self.__conn.commit()