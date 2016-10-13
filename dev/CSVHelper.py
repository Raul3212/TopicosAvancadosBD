#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv

# seguindo formato da descrição do trabalho
matricula = "358307"

def writeFile(filename, clusters, dataset, weekday):
	global matricula
	with open(filename, 'wb') as csvfile:		
		spamwriter = csv.writer(csvfile, delimiter=';')
		# seguindo formato da descrição do trabalho
		# escrevendo cabeçalho
		header = ['student_id', 'id_taxista', 'weekday', 'latitude', 'longitude', 'cluster', 'iscore']
		spamwriter.writerow(header)
		# escrevendo os dados em um csv
		for taxistaIndex in range(len(clusters)):
			clusterId, isCore = clusters[taxistaIndex]
			taxista = dataset[taxistaIndex]
			row = []
			row.append(matricula) # Colocar como variável global
			row.append(taxista.id)
			row.append(weekday)
			row.append(taxista.latitude)
			row.append(taxista.longitude)
			row.append(clusterId)
			row.append(isCore)
			spamwriter.writerow(row)
