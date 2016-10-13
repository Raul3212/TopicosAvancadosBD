#!/usr/bin/env python
# -*- coding: utf-8 -*-

from preprocess.PreProcess import *
from preprocess.MapMatching import *
from database.TaxistaDAO import *
from database.VerticeDAO import *
from database.RotasDAO import *
import numpy as np
from analysis.DBScan import *
from analysis.DBScanRede import *
from plotter.plotter import *
from CSVHelper import *
from graphs.Graph import *
from graphs.Dijkstra import *

#pré-processamento dos vértices, rotas e taxistas
#preprocessVertices("data/table_vertices.csv")
#preprocessRotas("data/table_roads.csv")
#preprocessTaxistas("data/teste_drive.csv")

#abre conexão
connectionFactory = ConnectionFactory()
#cria taxistaDAO
taxistaDAO = TaxistaDAO(connectionFactory.getConnection())
#cria verticeDAO
verticeDAO = VerticeDAO(connectionFactory.getConnection())
#cria rotasDAO
rotasDAO = RotasDAO(connectionFactory.getConnection())

# lista de todos os dias que serão analisados 
'''
days = [(1, '2008-02-04 12:00:00', '2008-02-04 13:00:00'), 
		(2, '2008-02-05 12:00:00', '2008-02-05 13:00:00'), 
		(3, '2008-02-06 12:00:00', '2008-02-06 13:00:00'), 
		(4, '2008-02-07 12:00:00', '2008-02-07 13:00:00'), 
		(5, '2008-02-08 12:00:00', '2008-02-08 13:00:00')]
'''
#lista do dia que será analisado com distância em rede
days = [(1, '2008-02-04 12:00:00', '2008-02-04 13:00:00')]

vertices = verticeDAO.selectAll()
print "Vertices : " + str(len(vertices))
rotas = rotasDAO.selectAll()
print "Rotas : " + str(len(rotas))

#criação da rede a partir dos vértices e das rotas
rede = Graph(vertices)
for rota in rotas:
	#print str(rota.source) + " - " + str(rota.target) + " - " + str(rota.cost)
	rede.addEdge(rota.source, rota.target, rota.cost)

#Para cada dia é feita a clusterização
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
	print "Map Matching realizado!"
	
	#executando DBScan com distância euclidiana
	'''
	result = DBSCAN(taxistas, 0.003, 50)
	clusters = result[0]
	qtdClusters = result[1]
	writeFile("resultados/resultado-distinct" + str(day[0]) + ".csv", clusters, taxistas, day[0])
	'''

	#executando DBScan com distância em rede
	result = DBSCANRede(taxistas, 0.01, 50, rede)
	clusters = result[0]
	print "Finalizado : " + str(result[1])
	
	#salvando resultado em arquivo
	writeFile("resultados/4resultado-rede-distinct" + str(day[0]) + ".csv", clusters, taxistas, day[0])

	#plotando resultado com matplot
	'''
	# PLotando resultado
	p1 = [116.0,39.0]
	p2 = [117.0,40.500]

	plot(taxistas, clusters, qtdClusters,  p1, p2)
	'''