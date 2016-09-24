from database.TaxistaDAO import *
from model.Taxista import *
from sets import Set
from math import pow,sqrt


def DBSCAN(dataset, eps, minPts):
	clusters = []
	n = len(dataset)
	visited = [False] * n
	noise = [False] * n
	inCluster = [False] * n
	for p in range(n):
		#print "taxista: " + str(p) + " : " +  str(dataset[p].id) 
		if visited[p]:
			continue
		visited[p] = True
		neighborPts,distinctNeighbors = regionQueryMultipleTaxis(p, eps, dataset)
		#print "vizinhos: " + str(len(neighborPts))
		if distinctNeighbors < minPts:
			noise[p] = True
		else: 
			newCluster = []
			clusters.append(newCluster)
			expandCluster(p, neighborPts, newCluster, eps, minPts, dataset, visited, noise, inCluster)
			#print len(newCluster)
	return (clusters, noise)		

def expandCluster(p, neighborPts, cluster, eps, minPts, dataset, visited, noise, inCluster):
	cluster.append(p)
	inCluster[p] = True
	#inThisCluster = {}
	#inThisCluster[dataset[p].id] = True
	for i in neighborPts:
		#print "Vizinho: " + str(i)
		if visited[i] is not True: 
			visited[i] = True
			neighborPtsNew, distinctNeighbors = regionQueryMultipleTaxis(i, eps, dataset)
			if len(neighborPtsNew) >= minPts:
				joinList(neighborPts, neighborPtsNew)
			#print "Vizinhos: " + str (len (neighborPts))
		#if dataset[i].id in inThisCluster: # retirar repeticao de taxistas
		#	inCluster[i] = True
		if inCluster[i] is not True:
			cluster.append(i)
			inCluster[i] = True
			#inThisCluster[dataset[i].id] = True
		#print "Cluster: " + str(len(cluster))	

def regionQueryMultipleTaxis (taxistaIndex, eps, dataset):
	neighborPts = []
	distinctTaxis =  Set()
	taxista = dataset[taxistaIndex]
	taxistaIndexNew = taxistaIndex - 1
	for taxistaIndexNew in range (len(dataset)):
		taxistaNew = dataset[taxistaIndexNew]
		if taxista.distance(taxistaNew) <= eps: # and taxistaNew.id != taxista.id and taxistaNew.id not in distinctTaxis:
			neighborPts.append(taxistaIndexNew)
			distinctTaxis.add(taxistaNew.id)
	return neighborPts, len(distinctTaxis) 	
			
def joinList(mainList, secondaryList):
	for i in secondaryList:
		if i not in mainList:
			mainList.append(i)