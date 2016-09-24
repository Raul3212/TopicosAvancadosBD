from preprocess.preprocess import *
from database.TaxistaDAO import *
from analysis.DBScan import *

#preprocessVertices("data/table_vertices.csv")
#preprocessTaxistas("data/teste_drive.csv")
#preprocessRotas("data/table_roads.csv")

connectionFactory = ConnectionFactory()
taxistaDAO = TaxistaDAO(connectionFactory.getConnection())

data = taxistaDAO.selectAll()


result = DBSCAN(data, 0.05, 5)

clusters = result[0]
for cluster in clusters:
	for t in cluster:
		print data[t].id
	print "###############################" 

for i in range(len(data)):
	if result[1][i]:
		print str(i) + " - " + str(data[i].id)
