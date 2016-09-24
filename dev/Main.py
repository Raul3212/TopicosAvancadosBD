from preprocess.preprocess import *
from database.TaxistaDAO import *


#preprocessVertices("data/table_vertices.csv")
#preprocessTaxistas("data/tdrive.csv")
#preprocessRotas("data/table_roads.csv")

connectionFactory = ConnectionFactory()
taxistaDAO = TaxistaDAO(connectionFactory.getConnection())

print len(taxistaDAO.selectAll())