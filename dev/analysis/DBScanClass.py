#!/usr/bin/env python
# -*- coding: utf-8 -*-
from database.TaxistaDAO import *
from model.Taxista import *
from sets import Set
from math import pow,sqrt

#Implementação mais limpa, porém mais lenta para o python

def joinList(mainList, secondaryList):
	for i in secondaryList:
		if i not in mainList:
			mainList.append(i)

class DBSCAN: 

	def __init__(self, dataset, eps, minPts):
		self.dataset = dataset
		self.eps = eps
		self.minPts = minPts
		self.clusters = []

		self.tamanhoDataset = len(dataset)
		self.visited = [False] * self.tamanhoDataset
		self.noise = [False] * self.tamanhoDataset
		self.inCluster = [False] * self.tamanhoDataset

	def run(self):
		
		for point in range(self.tamanhoDataset): 
			if self.visited[point]:
				continue
			self.visited[point] = True
			neighborPts,distinctNeighbors = self.regionQueryMultipleTaxis(point)
			if distinctNeighbors < self.minPts: #Considera apenas taxistas distintos para iniciar um cluster
				self.noise[point] = True
			else: 
				newCluster = []
				self.clusters.append(newCluster)
				self.expandCluster(point, neighborPts, newCluster)
		return (self.clusters, self.noise)		

	def expandCluster(self, p, neighborPts, cluster):
		cluster.append(p)
		self.inCluster[p] = True
		for point in neighborPts:
			if self.visited[point] is not True: 
				self.visited[point] = True
				neighborPtsNew, distinctNeighbors = self.regionQueryMultipleTaxis(point)
				if len(neighborPtsNew) >= self.minPts:
					joinList(neighborPts, neighborPtsNew)
			if self.inCluster[point] is not True:
				cluster.append(point)
				self.inCluster[point] = True

	def regionQueryMultipleTaxis (self, taxistaIndex):
		neighborPts = []
		distinctTaxis =  Set()
		taxista = self.dataset[taxistaIndex]
		taxistaIndexNew = taxistaIndex - 1
		while taxistaIndexNew >= 0: 
			taxistaNew = self.dataset[taxistaIndexNew]
			if taxista.distance(taxistaNew) <= self.eps:
				neighborPts.append(taxistaIndexNew)
				distinctTaxis.add(taxistaNew.id)
			elif taxista.longitude - taxistaNew.longitude > self.eps:
				break
			taxistaIndexNew = taxistaIndexNew - 1

		taxistaIndexNew = taxistaIndex + 1
		while taxistaIndexNew < self.tamanhoDataset: 
			taxistaNew = self.dataset[taxistaIndexNew]
			if taxista.distance(taxistaNew) <= self.eps:
				neighborPts.append(taxistaIndexNew)
				distinctTaxis.add(taxistaNew.id)
			elif taxista.longitude - taxistaNew.longitude > self.eps:
				break
			taxistaIndexNew = taxistaIndexNew + 1
		return neighborPts, len(distinctTaxis) 
				