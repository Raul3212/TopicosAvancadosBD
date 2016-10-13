#!/usr/bin/env python
# -*- coding: utf-8 -*-

from model.Rota import *

class RotasDAO:
	
	def __init__(self, __conn):
		self.__conn = __conn
       
    #Retorna a lista de todas as rotas cadastrada no banco
	def selectAll(self):
		cur = self.__conn.cursor()
		cur.execute("""SELECT id_edge, id_source, id_target, cost from rotas order by cost""")
		rows = cur.fetchall()
		cur.close()
		rotas = []
		for row in rows:
			rota = Rota(row[0],row[1],row[2],row[3])
			rotas.append(rota)
		return rotas

	#Insere uma lista de tuplas na tabela rotas
	def executeMany(self, rotas):
		if(rotas == None):
			return 
		cur = self.__conn.cursor()
		cur.executemany("""INSERT INTO rotas (id_edge, id_source, id_target, cost) VALUES (%s,%s,%s,%s)""", rotas)
		self.__conn.commit()
		cur.close()