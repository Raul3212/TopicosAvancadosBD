#!/usr/bin/env python
# -*- coding: utf-8 -*-

from database.TaxistaDAO import *
from model.Taxista import *
from sets import Set
from math import pow,sqrt

#iniciando valores globais
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

	#iniciando valores globais de acordo com os parâmetros recebidos 
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
	#para cada taxista p
	for p in range(n): 
		#print "No " + str(p) + " - Clusters " + str(len(clusters))
		if visited[p]:
			continue
		visited[p] = True
		neighborPts,distinctNeighbors = regionQueryMultipleTaxis(p)
		if distinctNeighbors >= minPts: #Considera apenas taxistas distintos para iniciar um cluster
			qtdClusters+=1
			#expandindo cluster
			expandCluster(p, neighborPts, qtdClusters)
	#retorna tupla com informações dos clusters e quantidade de clusters
	return (clusters, qtdClusters)		

#Função que expande um cluster a partir de um taxista p, seus vizinhos
# e o id do cluster corrente
def expandCluster(p, neighborPts, clusterId):
	global clusters
	global dataset
	global visited
	global inCluster
	global eps
	global minPts

	#coloca o ponto no cluster
	clusters[p] = (clusterId, True)
	inCluster[p] = True
	#inicia o tamanho como 1
	tamanho = 1
	for i in neighborPts:
		isCore = False
		if visited[i] is not True: 
			visited[i] = True
			#busca vizinhos
			neighborPtsNew, distinctNeighbors = regionQueryMultipleTaxis(i)
			if len(neighborPtsNew) >= minPts:
				#marca como core se a quantidade de vizinhos é maior que minPts
				isCore = True
				for neighbor in neighborPtsNew: 
					if neighbor not in neighborPts:
						neighborPts.append(neighbor)
		#adiciona valor no cluster caso ele não esteja em nenhum cluster
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
	
	'''
	for taxistaIndexNew in range(len(dataset)):
		taxistaNew = dataset[taxistaIndexNew]
		if taxista.distance(taxistaNew) <= eps:
			neighborPts.append(taxistaIndexNew)
			distinctTaxis.add(taxistaNew.id)

	'''
	# Coloca um ponto como vizinho dele próprio començando a busca pelo índice do próprio taxista		
	# Faz um corte movendo o taxista a partir do índice dele
	taxistaIndexNew = taxistaIndex
	while taxistaIndexNew >= 0: 
		taxistaNew = dataset[taxistaIndexNew]
		if taxista.distance(taxistaNew) <= eps:
			neighborPts.append(taxistaIndexNew)
			distinctTaxis.add(taxistaNew.id)
		#utilização do corte
		elif abs(taxista.longitude - taxistaNew.longitude) > eps:
			break
		taxistaIndexNew = taxistaIndexNew - 1

	taxistaIndexNew = taxistaIndex + 1
	while taxistaIndexNew < len(dataset): 
		taxistaNew = dataset[taxistaIndexNew]
		if taxista.distance(taxistaNew) <= eps:
			neighborPts.append(taxistaIndexNew)
			distinctTaxis.add(taxistaNew.id)
		#utilização do corte
		elif abs(taxista.longitude - taxistaNew.longitude) > eps:
			break
		taxistaIndexNew = taxistaIndexNew + 1

	return neighborPts, len(distinctTaxis) 
			
#def joinList(mainList, secondaryList):
#	for i in secondaryList:
#		if i not in mainList:
#				mainList.append(i)