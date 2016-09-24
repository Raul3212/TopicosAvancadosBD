from database.TaxistaDAO import *
from model.Taxista import *

def DBSCAN(dataset, eps, minPts):
	clusters = []
	n = len(dataset)
	visited = [False] * n
	noise = [False] * n
	inCluster = [False] * n
	for p in range(n): 
		if visited[p]:
			continue
		visited[p] = True
		neighborPts = regionQuery(p, eps, dataset)
		if len(neighborPts) < minPts:
			noise[p] = True
		else: 
			newCluster = []
			c.append(newCluster)
			expandCluster(p, neighborPts, newCluster, eps, minPts, dataset, visited, noise)
	return clusters		

def expandCluster(p, neighborPts, cluster, eps, minPts, dataset, visited, noise, inCluster):
	cluster.append(p)
	inCluster[p] = True
	for i in neighborPts:
		if !visited[i]: 
			visited[i] = True
			neighborPtsNew = regionQuery(i, eps, dataset)
			if len(neighborPtsNew) >= minPts:
				neighborPts = neighborPts + neighborPtsNew
		if !inCluster[i]:
			cluster.append(i)
			inCluster[i] = True

def regionQuery (taxistaIndex, eps, dataset):
	neighborPts = []
	taxista = dataset[taxistaIndex]
	for taxistaIndexNew in range(len(dataset)):
		taxistaNew = taxista[taxistaIndexNew]
		if taxistaNew.id != taxista.id:
			if taxista.distance(taxistaNew) <= eps: 
				neighborPts.append(taxistaIndexNew)
	return neighborPts 		
			
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