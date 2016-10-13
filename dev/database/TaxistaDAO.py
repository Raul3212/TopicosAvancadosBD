#!/usr/bin/env python
# -*- coding: utf-8 -*-

from model.Taxista import *
from model.Ponto import *

import numpy as np

class TaxistaDAO:
	
	def __init__(self, __conn):
		self.__conn = __conn
    
    #Retorna a lista de todos os taxistas cadastrados no banco
	def selectAll(self, timeMin, timeMax):
		cur = self.__conn.cursor()
		sql = """SELECT id_driver, tempo, latitude, longitude from taxistas where tempo >= '{0}' and tempo < '{1}' and (longitude > 0 and latitude > 0)  order by longitude"""
		sql = sql.format(timeMin, timeMax)
		cur.execute(sql)
		rows = cur.fetchall()
		cur.close()
		taxistas = []
		for row in rows:
			taxista = Taxista(row[0], row[1], row[2], row[3])
			taxistas.append(taxista)
		return taxistas

	
	#Pega pontos distintos de cada taxista. 
	#Caso um taxista tenho duas entradas com a mesma localização, será considerada apenas uma delas e o maior valor da coluna tempo
	def selectAllDistinct(self, timeMin, timeMax):
		cur = self.__conn.cursor()
		sql = """SELECT id_driver, max(tempo), latitude, longitude from taxistas where tempo >= '{0}' and tempo < '{1}' and (longitude > 0 and latitude > 0)  group by id_driver, longitude, latitude order by longitude"""
		sql = sql.format(timeMin, timeMax)
		cur.execute(sql)
		rows = cur.fetchall()
		cur.close()
		taxistas = []
		for row in rows:
			taxista = Taxista(row[0], row[1], row[2], row[3])
			taxistas.append(taxista)
		return taxistas

	#Insere uma lista de tuplas na tabela taxistas	
	def executeMany(self, vertices):
		if(vertices == None):
			return 
		cur = self.__conn.cursor()
		cur.executemany("""INSERT INTO taxistas (id_driver, tempo, longitude, latitude) VALUES (%s, %s, %s,%s)""", vertices)
		self.__conn.commit()
		cur.close()

	#Atualiza um conjunto de tuplas da tabela de taxistas
	def updatePontos(self, pontos):
		if(pontos == None):
			return
		cur = self.__conn.cursor()
		cur.executemany("""UPDATE taxistas set id_vertice=%s where latitude=%s and longitude=%s""", pontos)
		self.__conn.commit()
		cur.close()

	#Retorna uma lista de pontos (latitude, longitude) da tabela de taxistas
	def selectPositions(self, timeMin, timeMax):
		cur = self.__conn.cursor()

		sql = """SELECT latitude, longitude from taxistas where tempo >= '{0}' and tempo < '{1}' and (longitude > 0 and latitude > 0)  group by longitude, latitude order by longitude"""
		sql = sql.format(timeMin, timeMax)
		cur.execute(sql)
		rows = cur.fetchall()
		cur.close()
		positions = []
		for row in rows:
			position = Ponto(row[0], row[1])
			positions.append(position)
		return positions