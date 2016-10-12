#!/usr/bin/env python
# -*- coding: utf-8 -*-

from database.TaxistaDAO import *
from model.Taxista import *
from sets import Set
from graphs.Graph import *
from graphs.Dijkstra import *

clusters = []
n = 0
visited = []
inCluster = []
dataset = None
eps = 0
minPts = 0
rede = None
cache = {}

def DBSCANRede(paramDataset, paramEps, paramMinPts, paramRede):
	global clusters
	global dataset
	global visited
	global inCluster
	global eps
	global minPts
	global rede
	global cache

	print cache
	cache = {}
	print cache

	dataset = paramDataset
	eps = paramEps
	minPts = paramMinPts
	rede = paramRede

	clusters = []
	n = len(dataset)
	visited = [False] * n
	inCluster = [False] * n
	#Marca todos como outliers no início. Ao ser colocado em um cluster, ele é marcado com o id do cluster e True (é core) ou False (não core)
	# -1 outlier (noise), 1 ... id do cluster
	clusters = [(-1, False)] * n
	qtdClusters = 0
	for p in range(n): 
		#print "No " + str(p) + " - Clusters " + str(qtdClusters)
		if visited[p]:
			continue
		visited[p] = True
		neighborPts,distinctNeighbors = regionQueryRede(p)
		#print distinctNeighbors
		if distinctNeighbors >= minPts: #Considera apenas taxistas distintos para iniciar um cluster
			isNew = expandClusterRede(p, neighborPts, qtdClusters)
			if isNew:
				qtdClusters+=1
	return (clusters, qtdClusters)		

def expandClusterRede(p, neighborPts, clusterId):
	global clusters
	global dataset
	global visited
	global inCluster
	global eps
	global minPts

	currentClusterIndexes = []

	clusters[p] = (clusterId, True)
	inCluster[p] = True
	tamanho = 1
	#aux = 0
	for i in neighborPts:
		#aux += 1
		#print "Vizinho " + str(i) + " - Clusters " + str(clusterId)
		#print "Indice " + str(aux) + " - tamanho vizinhos " + str(len(neighborPts))
		isCore = False
		if visited[i] is not True: 
			visited[i] = True
			neighborPtsNew, distinctNeighbors = regionQueryRede(i)
			if len(neighborPtsNew) >= minPts:
				isCore = True
				for neighbor in neighborPtsNew: 
					if neighbor not in neighborPts:
						neighborPts.append(neighbor)
		if inCluster[i] is not True:
			clusters[i] = (clusterId, isCore)
			currentClusterIndexes.append(i)
			inCluster[i] = True
			tamanho += 1
	'''
	if tamanho < minPts: 
		#marcando como noise os clusters que tem menos que minPts
		for index in currentClusterIndexes:
			clusters[index] = (-1, False)
			inCluster[index] = False
		return False
	else:
		print "Novo cluster com tamanho : " + str(tamanho)
		return True
	'''
	print "ClusterId " + str(clusterId) + " - Tamanho " + str(tamanho)
	return True

# global dataset precisa estar ordenado pela longitude para o método funcionar devidamente
def regionQueryRede (taxistaIndex):
	
	global dataset
	global eps
	global rede
	global cache

	neighborPts = []
	distinctTaxis =  Set()
	taxista = dataset[taxistaIndex]
	vizinhos = []
	if taxista.vertice not in cache:
		vizinhos = DijkstraModificado(rede, taxista.vertice, eps).run()
				
		'''
		for taxistaIndexNew in range(len(dataset)):
			taxistaNew = dataset[taxistaIndexNew]
			if taxistaNew.vertice in vizinhos:
				neighborPts.append(taxistaIndexNew)
				distinctTaxis.add(taxistaNew.id)
		'''
		# Utilizando corte
		# Se a distância euclidiana for maior que eps, então a distância em rede também será	
		taxistaIndexNew = taxistaIndex
		while taxistaIndexNew >= 0: 
			taxistaNew = dataset[taxistaIndexNew]
			if taxistaNew.vertice in vizinhos:
				neighborPts.append(taxistaIndexNew)
				distinctTaxis.add(taxistaNew.id)
			elif abs(taxista.longitude - taxistaNew.longitude) > eps:
				break
			taxistaIndexNew = taxistaIndexNew - 1

		taxistaIndexNew = taxistaIndex + 1
		while taxistaIndexNew < len(dataset): 
			taxistaNew = dataset[taxistaIndexNew]
			if taxistaNew.vertice in vizinhos:
				neighborPts.append(taxistaIndexNew)
				distinctTaxis.add(taxistaNew.id)
			elif abs(taxista.longitude - taxistaNew.longitude) > eps:
				break
			taxistaIndexNew = taxistaIndexNew + 1
			
		cache[taxista.vertice] = (neighborPts, len(distinctTaxis))
	return cache[taxista.vertice]
			
#def joinList(mainList, secondaryList):
#	for i in secondaryList:
#		if i not in mainList:
#				mainList.append(i)