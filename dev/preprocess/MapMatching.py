#!/usr/bin/env python
# -*- coding: utf-8 -*-

from math import pow,sqrt

# Função que cálculo a distância de um ponto qualquer (taxista) e um vértice
def distancia(ponto, vertice):
	return sqrt (pow((vertice.latitude - ponto.latitude),2.0) + pow((vertice.longitude - ponto.longitude),2.0))


# Algoritmo de mapmathing utilizando distãncia euclidiana 
# parâmetro pontos (ordenado por longitude)
# parâmetro vertices (ordenado por longitude)
def mapMatchingTaxistas(taxistas, vertices):
	qtdVertices = len(vertices)
	qtdTaxistas = len(taxistas)
	if(qtdVertices == 0 or qtdTaxistas == 0): 
		return	
	indexTaxistas = range(1, qtdVertices-1, 1) #excluindo o vértice inicial e final
	indexTaxistasInvertido = range(qtdVertices-2, 0, -1) #excluindo o vértice inicial e final - colocando a lista invertida  
	for taxista in taxistas:
		verticeInicial = vertices[0] 
		verticeFinal = vertices[qtdVertices-1]
		distVerticeInicial = distancia(taxista, verticeInicial)
		distVerticeFinal = distancia(taxista, verticeFinal)
		minDist = distVerticeInicial
		taxista.setVertice(verticeInicial.id)
		#Verificação se o taxista está mais próximo do vértice inicial ou final
		#O iterador começa do vértice mais próximo
		#Essa informação é utilizada para a aplicação do corte
		if(distVerticeFinal < distVerticeInicial):
			#Mudando iterador para começar no vértice final
			iterator = indexTaxistasInvertido
			minDist = distVerticeFinal
			taxista.setVertice(verticeFinal.id)
		else:
			#Mudando iterador para começar no vértice inicial
			iterator = indexTaxistas
		for verticeIndex in iterator:
			vertice = vertices[verticeIndex]
			dist = distancia(taxista, vertice)
			if(dist < minDist):
				minDist = dist
				taxista.setVertice(vertice.id)	
			elif (abs(vertice.longitude - taxista.longitude) > minDist): 
				# a lista deve estar ordenada pela longitude
				# corte utilizando a longitude para saber se todos os 
				# pontos seguintes terão pelo menos uma distância maior que a minDist corrente
				break
		#print str(taxista.longitude) + " - " + str(taxista.latitude) + " - " + str(taxista.vertice)
	return taxistas

# Algoritmo de mapmathing utilizando distãncia euclidiana 
# parâmetro pontos (ordenado por longitude)
# parâmetro vertices (ordenado por longitude)
# Retorna os dados no formato para serem atualizados no banco
def mapMatching(pontos, vertices):
	qtdVertices = len(vertices)
	qtdPontos = len(pontos)
	if(qtdVertices == 0 or qtdPontos == 0): 
		return
	batchPoints = []
	for ponto in pontos:
		verticeInicial = vertices[0] 
		verticeFinal = vertices[qtdVertices-1]
		iterator = range(qtdVertices)
		distVerticeInicial = distancia(ponto, verticeInicial)
		distVerticeFinal = distancia(ponto, verticeFinal)
		minDist = distVerticeInicial
		ponto.setVerticeProximo(verticeInicial.id)
		if(distVerticeFinal < distVerticeInicial):
			iterator.reverse()
			minDist = distVerticeFinal
			ponto.setVerticeProximo(verticeFinal.id)
		iterator.pop(0) #remove primeiro elemento
		iterator.pop() #remove último elemento
		for verticeIndex in iterator:
			vertice = vertices[verticeIndex]
			dist = distancia(ponto, vertice)
			if(dist < minDist):
				minDist = dist
				ponto.setVerticeProximo(vertice.id)	
			elif (abs(vertice.longitude - ponto.longitude) > minDist): #caso a lista esteja ordenada pela longitude
				# a lista deve estar ordenada pela longitude
				# corte utilizando a longitude para saber se todos os 
				# pontos seguintes terão pelo menos uma distância maior que a minDist corrente
				break
		batchPoints.append((ponto.verticeProximo,ponto.latitude,ponto.longitude), )
		#print str(ponto.longitude) + " - " + str(ponto.latitude) + " - " + str(ponto.verticeProximo)
	return batchPoints
