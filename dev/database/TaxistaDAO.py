from model.Taxista import *
import numpy as np

class TaxistaDAO:
	
	def __init__(self, __conn):
		self.__conn = __conn
        
	def selectAll(self):
		cur = self.__conn.cursor()
		cur.execute("""SELECT id_driver, tempo, latitude, longitude from taxistas where tempo >= '2008-02-04 12:00:00' and tempo < '2008-02-04 12:00:00' order by longitude""")
		#cur.execute("""SELECT id_driver, tempo, longitude, latitude from taxistas""")
		rows = cur.fetchall()
		cur.close()
		taxistas = []
		for row in rows:
			taxista = Taxista(row[0], row[1], row[2], row[3])
			taxistas.append(taxista)
		return taxistas

	def executeMany(self, vertices):
		cur = self.__conn.cursor()
		cur.executemany("""INSERT INTO taxistas (id_driver, tempo, longitude, latitude) VALUES (%s, %s, %s,%s)""", vertices)
		self.__conn.commit()
		cur.close()

	#retorna [[longitude, latitude)]
	def selectPositions(self):
		cur = self.__conn.cursor()
		cur.execute("""SELECT longitude,latitude FROM taxistas WHERE latitude > 35 AND longitude > 114""")
		rows = cur.fetchall()
		cur.close()
		positions = []
		for row in rows:
			position = [row[0], row[1]]
			positions.append(position)
		return np.matrix(positions)