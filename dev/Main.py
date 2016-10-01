#!/usr/bin/env python
# -*- coding: utf-8 -*-

from preprocess.PreProcess import *
from preprocess.MapMatching import *
from database.TaxistaDAO import *
from database.VerticeDAO import *
import numpy as np
from analysis.DBScan import *
from plotter.plotter import *
from CSVHelper import *

#preprocessVertices("data/table_vertices.csv")
#preprocessTaxistas("data/teste_drive.csv")
#preprocessRotas("data/table_roads.csv")

connectionFactory = ConnectionFactory()
taxistaDAO = TaxistaDAO(connectionFactory.getConnection())
verticeDAO = VerticeDAO(connectionFactory.getConnection())

days = [(1, '2008-02-04 12:00:00', '2008-02-04 12:00:00'), 
		(2, '2008-02-05 12:00:00', '2008-02-05 12:00:00'), 
		(3, '2008-02-06 12:00:00', '2008-02-06 12:00:00'), 
		(4, '2008-02-07 12:00:00', '2008-02-07 12:00:00'), 
		(5, '2008-02-08 12:00:00', '2008-02-08 12:00:00')]

for day in days: 

	'''
	Pegar pontos distintos de cada taxista. 
	Caso um taxista tenho duas entradas com a mesma localização, será considerada apenas uma delas e o maior valor da coluna tempo
	'''
	positions = taxistaDAO.selectPositions(day[1], day[2])
	vertices = verticeDAO.selectAll()

	batchPoints = mapMatching(positions, vertices)

	print "MapMatching finalizado!"
	print batchPoints
	taxistaDAO.updatePontos(batchPoints)

	#taxistas = taxistaDAO.selectAllDistinct(day[1], day[2])

	#Atualizar pontos no banco	

	'''
	result = DBSCAN(taxistas, 0.01, 50)
	clusters = result[0]

	print result[1]

	writeFile("resultado-" + str(day[0]) + ".csv", clusters, taxistas, day[0])
	'''

	'''
	p1 = [116.0,39.0]
	p2 = [117.0,40.500]

	plot(taxistas, clusters, p1, p2)
	'''