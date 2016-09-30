from database.TaxistaDAO import *
from model.Taxista import *
from sets import Set
from math import pow,sqrt

clusters = []
n = 0
visited = []
noise = []
inCluster = []
dataset = None
eps = 0
minPts = 0

def DBSCAN(paramDataset, paramEps, paramMinPts):
	global clusters
	global dataset
	global visited
	global noise
	global inCluster
	global eps
	global minPts

	dataset = paramDataset
	eps = paramEps
	minPts = paramMinPts

	clusters = []
	n = len(dataset)
	visited = [False] * n
	noise = [False] * n
	inCluster = [False] * n
	for p in range(n): 
		#print "No " + str(p) + " - Clusters " + str(len(clusters))
		if visited[p]:
			continue
		visited[p] = True
		neighborPts,distinctNeighbors = regionQueryMultipleTaxis(p)
		if distinctNeighbors < minPts: #Considera apenas taxistas distintos para iniciar um cluster
			noise[p] = True
		else: 
			newCluster = []
			clusters.append(newCluster)
			expandCluster(p, neighborPts, newCluster)
	return (clusters, noise)		

def expandCluster(p, neighborPts, cluster):
	global dataset
	global visited
	global inCluster
	global eps
	global minPts
	global clusters

	cluster.append(p)
	inCluster[p] = True
	aux = 0
	for i in neighborPts:
		aux += 1
		#print "Vizinho " + str(i) + " - Clusters " + str(len(clusters))
		#print "Indice " + str(aux) + " - tamanho vizinhos " + str(len(neighborPts))
		if visited[i] is not True: 
			visited[i] = True
			neighborPtsNew, distinctNeighbors = regionQueryMultipleTaxis(i)
			if len(neighborPtsNew) >= minPts:
				for neighbor in neighborPtsNew: 
					if neighbor not in neighborPts:
						neighborPts.append(neighbor)
		if inCluster[i] is not True:
			cluster.append(i)
			inCluster[i] = True

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
		elif sqrt(pow(taxista.longitude - taxistaNew.longitude,2.0)) > eps:
			break
		taxistaIndexNew = taxistaIndexNew - 1

	taxistaIndexNew = taxistaIndex + 1
	while taxistaIndexNew < len(dataset): 
		taxistaNew = dataset[taxistaIndexNew]
		if taxista.distance(taxistaNew) <= eps:
			neighborPts.append(taxistaIndexNew)
			distinctTaxis.add(taxistaNew.id)
		elif sqrt(pow(taxista.longitude - taxistaNew.longitude,2.0)) > eps:
			break
		taxistaIndexNew = taxistaIndexNew + 1
	return neighborPts, len(distinctTaxis) 
			
#def joinList(mainList, secondaryList):
#	for i in secondaryList:
#		if i not in mainList:
#				mainList.append(i)