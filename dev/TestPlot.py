from database.TaxistaDAO import *
from database.Connection import *
from plotter.plotter import *
import numpy as np

connectionFactory = ConnectionFactory()
taxistaDAO = TaxistaDAO(connectionFactory.getConnection())

positions = taxistaDAO.selectPositions()

#print positions

plot(positions)