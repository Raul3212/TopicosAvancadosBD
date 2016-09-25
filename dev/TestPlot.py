from plotter.plotter import *
import numpy as np

data = np.genfromtxt("data/teste_drive.csv", delimiter=";")
plot(data)