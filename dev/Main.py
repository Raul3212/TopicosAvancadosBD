#!/usr/bin/env python
# -*- coding: utf-8 -*-

from preprocess.preprocess import *
from database.TaxistaDAO import *
import numpy as np
from analysis.DBScan import *
from plotter.plotter import *
from CSVHelper import *

#preprocessVertices("data/table_vertices.csv")
#preprocessTaxistas("data/teste_drive.csv")
#preprocessRotas("data/table_roads.csv")

connectionFactory = ConnectionFactory()
taxistaDAO = TaxistaDAO(connectionFactory.getConnection())

days = [(1, '2008-02-04 12:00:00', '2008-02-04 13:00:00'), 
		(2, '2008-02-05 12:00:00', '2008-02-05 13:00:00'), 
		(3, '2008-02-06 12:00:00', '2008-02-06 13:00:00'), 
		(4, '2008-02-07 12:00:00', '2008-02-07 13:00:00'), 
		(5, '2008-02-08 12:00:00', '2008-02-08 13:00:00')]

for day in days: 

	data = taxistaDAO.selectAll(day[1], day[2])
	print str(len(data)) + " taxistas"

	result = DBSCAN(data, 0.01, 50)
	clusters = result[0]

	print result[1]

	writeFile("resultado-" + str(day[0]) + ".csv", clusters, data, day[0])
		
	'''
	p1 = [116.0,39.0]
	p2 = [117.0,40.500]

	plot(data, clusters, p1, p2)
	'''