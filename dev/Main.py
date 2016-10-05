#!/usr/bin/env python
# -*- coding: utf-8 -*-

from preprocess.PreProcess import *
from preprocess.MapMatching import *
from database.TaxistaDAO import *
from database.VerticeDAO import *
from database.RotasDAO import *
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
rotasDAO = RotasDAO(connectionFactory.getConnection())

days = [(1, '2008-02-04 12:00:00', '2008-02-04 12:00:00'), 
		(2, '2008-02-05 12:00:00', '2008-02-05 12:00:00'), 
		(3, '2008-02-06 12:00:00', '2008-02-06 12:00:00'), 
		(4, '2008-02-07 12:00:00', '2008-02-07 12:00:00'), 
		(5, '2008-02-08 12:00:00', '2008-02-08 12:00:00')]


vertices = verticeDAO.selectAll()
print "Vertices : " + str(len(vertices))
rotas = rotasDAO.selectAll()
print "Rotas : " + str(len(rotas))
for day in days: 

	'''
	Pegar pontos distintos de cada taxista. 
	Caso um taxista tenho duas entradas com a mesma localização, será considerada apenas uma delas e o maior valor da coluna tempo
	-----------------------

	muito custoso para o banco
	utilizando estratégia para manter dados em memória	
	'''
	
	'''
	positions = taxistaDAO.selectPositions(day[1], day[2])
	batchPoints = mapMatching(positions, vertices)

	print "MapMatching finalizado!"
	print batchPoints
	
	taxistaDAO.updatePontos(batchPoints)
	'''

	taxistas = taxistaDAO.selectAllDistinct(day[1], day[2])
	print "Taxistas : " + str(len(taxistas))
	mapMatchingTaxistas(taxistas, vertices)


	
	#result = DBSCAN(taxistas, 0.003, 50)
	#clusters = result[0]

	#print result[1]

	#writeFile("resultado-" + str(day[0]) + ".csv", clusters, taxistas, day[0])
	

	'''
	p1 = [116.0,39.0]
	p2 = [117.0,40.500]

	plot(taxistas, clusters, p1, p2)
	'''