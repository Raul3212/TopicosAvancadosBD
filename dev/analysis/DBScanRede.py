#!/usr/bin/env python
# -*- coding: utf-8 -*-

from database.TaxistaDAO import *
from model.Taxista import *
from sets import Set
from graphs.Graph import *
from graphs.Dijkstra import *

#iniciando valores globais
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

	cache = {} #limpando a cache
	
	#iniciando valores globais de acordo com os parâmetros recebidos 
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
	#para cada taxista p
	for p in range(n): 
		#print "No " + str(p) + " - Clusters " + str(qtdClusters)
		if visited[p]:
			continue
		visited[p] = True
		neighborPts,distinctNeighbors = regionQueryRede(p)
		#print distinctNeighbors
		if distinctNeighbors >= minPts: #Considera apenas taxistas distintos para iniciar um cluster
			#expandindo cluster
			isNew = expandClusterRede(p, neighborPts, qtdClusters)
			if isNew:
				qtdClusters+=1
	return (clusters, qtdClusters)		


#Função que expande um cluster a partir de um taxista p, seus vizinhos
# e o id do cluster corrente
def expandClusterRede(p, neighborPts, clusterId):
	global clusters
	global dataset
	global visited
	global inCluster
	global eps
	global minPts

	currentClusterIndexes = []

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
			neighborPtsNew, distinctNeighbors = regionQueryRede(i)
			if len(neighborPtsNew) >= minPts:
				#marca como core se a quantidade de vizinhos é maior que minPts
				isCore = True
				for neighbor in neighborPtsNew: 
					if neighbor not in neighborPts:
						neighborPts.append(neighbor)
		#adiciona valor no cluster caso ele não esteja em nenhum cluster
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
	#utlização de cache para vértices com vizinhos já calculados
	if taxista.vertice not in cache:
		#calcula vértices vizinhos
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
			#se o vértice do taxista estiver nos vizinhos, então ele é vizinho
			if taxistaNew.vertice in vizinhos:
				neighborPts.append(taxistaIndexNew)
				distinctTaxis.add(taxistaNew.id)
			#utilizando corte
			elif abs(taxista.longitude - taxistaNew.longitude) > eps:
				break
			taxistaIndexNew = taxistaIndexNew - 1

		taxistaIndexNew = taxistaIndex + 1
		while taxistaIndexNew < len(dataset): 
			taxistaNew = dataset[taxistaIndexNew]
			if taxistaNew.vertice in vizinhos:
				neighborPts.append(taxistaIndexNew)
				distinctTaxis.add(taxistaNew.id)
			#utilizando corte
			elif abs(taxista.longitude - taxistaNew.longitude) > eps:
				break
			taxistaIndexNew = taxistaIndexNew + 1
			
		cache[taxista.vertice] = (neighborPts, len(distinctTaxis))
	return cache[taxista.vertice]
			
#def joinList(mainList, secondaryList):
#	for i in secondaryList:
#		if i not in mainList:
#				mainList.append(i)