#!/usr/bin/env python
# -*- coding: utf-8 -*-

from database.TaxistaDAO import *
from model.Taxista import *
from sets import Set
from math import pow,sqrt

clusters = []
n = 0
visited = []
inCluster = []
dataset = None
eps = 0
minPts = 0

def DBSCAN(paramDataset, paramEps, paramMinPts):
	global clusters
	global dataset
	global visited
	global inCluster
	global eps
	global minPts

	dataset = paramDataset
	eps = paramEps
	minPts = paramMinPts

	clusters = []
	n = len(dataset)
	visited = [False] * n
	inCluster = [False] * n
	#Marca todos como outliers no início. Ao ser colocado em um cluster, ele é marcado com o id do cluster e True (é core) ou False (não core)
	# -1 outlier (noise), 1 ... id do cluster
	clusters = [(-1, False)] * n
	qtdClusters = 0
	for p in range(n): 
		#print "No " + str(p) + " - Clusters " + str(len(clusters))
		if visited[p]:
			continue
		visited[p] = True
		neighborPts,distinctNeighbors = regionQueryMultipleTaxis(p)
		if distinctNeighbors >= minPts: #Considera apenas taxistas distintos para iniciar um cluster
			qtdClusters+=1
			expandCluster(p, neighborPts, qtdClusters)
	return (clusters, qtdClusters)		

def expandCluster(p, neighborPts, clusterId):
	global clusters
	global dataset
	global visited
	global inCluster
	global eps
	global minPts

	clusters[p] = (clusterId, True)
	inCluster[p] = True
	tamanho = 1
	#aux = 0
	for i in neighborPts:
		#aux += 1
		#print "Vizinho " + str(i) + " - Clusters " + str(len(clusters))
		#print "Indice " + str(aux) + " - tamanho vizinhos " + str(len(neighborPts))
		isCore = False
		if visited[i] is not True: 
			visited[i] = True
			neighborPtsNew, distinctNeighbors = regionQueryMultipleTaxis(i)
			if len(neighborPtsNew) >= minPts:
				isCore = True
				for neighbor in neighborPtsNew: 
					if neighbor not in neighborPts:
						neighborPts.append(neighbor)
		if inCluster[i] is not True:
			clusters[i] = (clusterId, isCore)
			inCluster[i] = True
			tamanho += 1
	print "Novo cluster com tamanho : " + str(tamanho)

# global dataset precisa estar ordenado pela longitude para o método funcionar devidamente
def regionQueryMultipleTaxis (taxistaIndex):
	
	global dataset
	global eps
	
	neighborPts = []
	distinctTaxis =  Set()
	taxista = dataset[taxistaIndex]
	taxistaIndexNew = taxistaIndex - 1
	while taxistaIndexNew >= 0: 
		taxistaNew = dataset[taxistaIndexNew]
		if taxista.distance(taxistaNew) <= eps:
			neighborPts.append(taxistaIndexNew)
			distinctTaxis.add(taxistaNew.id)
		elif abs(taxista.longitude - taxistaNew.longitude) > eps:
			break
		taxistaIndexNew = taxistaIndexNew - 1

	taxistaIndexNew = taxistaIndex + 1
	while taxistaIndexNew < len(dataset): 
		taxistaNew = dataset[taxistaIndexNew]
		if taxista.distance(taxistaNew) <= eps:
			neighborPts.append(taxistaIndexNew)
			distinctTaxis.add(taxistaNew.id)
		elif abs(taxista.longitude - taxistaNew.longitude) > eps:
			break
		taxistaIndexNew = taxistaIndexNew + 1
	return neighborPts, len(distinctTaxis) 
			
#def joinList(mainList, secondaryList):
#	for i in secondaryList:
#		if i not in mainList:
#				mainList.append(i)