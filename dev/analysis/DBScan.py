from database.TaxistaDAO import *
from model.Taxista import *

def DBSCAN(dataset, eps, minPts):
	clusters = []
	n = len(dataset)
	visited = [False] * n
	noise = [False] * n
	inCluster = [False] * n
	for p in range(n):
		#print "taxista: " + str(p) 
		if visited[p]:
			continue
		visited[p] = True
		neighborPts = regionQuery(p, eps, dataset, inCluster)
		if len(neighborPts) < minPts:
			noise[p] = True
		else: 
			newCluster = []
			clusters.append(newCluster)
			expandCluster(p, neighborPts, newCluster, eps, minPts, dataset, visited, noise, inCluster)
			#print newCluster
	return (clusters, noise)		

def expandCluster(p, neighborPts, cluster, eps, minPts, dataset, visited, noise, inCluster):
	cluster.append(p)
	inCluster[p] = True
	thisCluster = {}
	thisCluster[dataset[p].id] = True
	for i in neighborPts:
		#print "Vizinho: " + str(i)
		if visited[i] is not True: 
			visited[i] = True
			neighborPtsNew = regionQueryInCluster(i, eps, dataset)
			if len(neighborPtsNew) >= minPts:
				joinList(neighborPts, neighborPtsNew)
			#print "Vizinhos: " + str (len (neighborPts))
		if dataset[i].id in thisCluster:
			inCluster[i] = True
		if inCluster[i] is not True and dataset[i].id not in thisCluster:
			cluster.append(i)
			inCluster[i] = True
			thisCluster[dataset[i].id] = True
		#print "Cluster: " + str(len(cluster))	

def regionQuery (taxistaIndex, eps, dataset, inCluster, thisCluster = {}):
	neighborPts = []
	taxista = dataset[taxistaIndex]
	for taxistaIndexNew in range(len(dataset)):
		taxistaNew = dataset[taxistaIndexNew]
		if taxistaNew.id != taxista.id:
			if (taxistaNew.id not in thisCluster) and inCluster[taxistaIndexNew] is not True:
				if taxista.distance(taxistaNew) <= eps: 
					neighborPts.append(taxistaIndexNew)
	return neighborPts 		

def regionQueryInCluster (taxistaIndex, eps, dataset):
	neighborPts = []
	taxista = dataset[taxistaIndex]
	for taxistaIndexNew in range(len(dataset)):
		taxistaNew = dataset[taxistaIndexNew]
		if taxistaNew.id != taxista.id:
			if taxista.distance(taxistaNew) <= eps: 
				neighborPts.append(taxistaIndexNew)
	return neighborPts 	
			
def joinList(mainList, secondaryList):
	for i in secondaryList:
		if i not in mainList:
			mainList.append(i)	
'''
DBSCAN(D, eps, MinPts) {
   C = 0
   for each point P in dataset D {
      if P is visited
         continue next point
      mark P as visited
      NeighborPts = regionQuery(P, eps)
      if sizeof(NeighborPts) < MinPts
         mark P as NOISE
      else {
         C = next cluster
         expandCluster(P, NeighborPts, C, eps, MinPts)
      }
   }
}

expandCluster(P, NeighborPts, C, eps, MinPts) {
   add P to cluster C
   for each point P' in NeighborPts { 
      if P' is not visited {
         mark P' as visited
         NeighborPts' = regionQuery(P', eps)
         if sizeof(NeighborPts') >= MinPts
            NeighborPts = NeighborPts joined with NeighborPts'
      }
      if P' is not yet member of any cluster
         add P' to cluster C
   }
}

regionQuery(P, eps)
   return all points within P's eps-neighborhood (including P)

'''