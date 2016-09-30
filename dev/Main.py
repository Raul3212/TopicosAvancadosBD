from preprocess.preprocess import *
from database.TaxistaDAO import *
import numpy as np
from analysis.DBScan import *
from plotter.plotter import *

#preprocessVertices("data/table_vertices.csv")
#preprocessTaxistas("data/teste_drive.csv")
#preprocessRotas("data/table_roads.csv")

connectionFactory = ConnectionFactory()
taxistaDAO = TaxistaDAO(connectionFactory.getConnection())

data = taxistaDAO.selectAll()
print str(len(data)) + " taxistas"

result = DBSCAN(data, 0.0001, 50) #.run()

clusters = result[0]

print len(clusters)

for cluster in clusters:
	print len(cluster)

p1 = [116.217,39.5317]
p2 = [116.873,40.1782]

#plot(data, clusters, p1, p2)