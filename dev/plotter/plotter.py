import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap

def plot(dataset, clusters, qtdClusters, p1, p2):

	cores = []
	for name, code in matplotlib.colors.cnames.iteritems():
		cores.append(name)

	fig = plt.figure()

	themap = Basemap(projection='gall',
              llcrnrlon = p1[0],              # lower-left corner longitude
              llcrnrlat = p1[1],               # lower-left corner latitude
              urcrnrlon = p2[0],               # upper-right corner longitude
              urcrnrlat = p2[1],               # upper-right corner latitude
              resolution = 'l',
              area_thresh = 10000.0,
              )
              
	themap.drawcoastlines()
	themap.drawcountries()
	themap.fillcontinents(color = 'gainsboro')
	themap.drawmapboundary(fill_color='steelblue')


	for indexTaxista in range(len(clusters)): 
		taxista = dataset[indexTaxista]
		clusterValue = clusters[indexTaxista]
		if clusterValue[0] != -1:
			x,y = themap(taxista.longitude, taxista.latitude) 
			themap.plot(x,y, 
	            'o',                    # marker shape
	            color=cores[clusterValue[0] % qtdClusters],         # marker colour
	            markersize=4            # marker size
	            )

	themap.llcrnrlon = p1[0]
	themap.llcrnrlat = p1[1]
	themap.urcrnrlon = p2[0]
	themap.urcrnrlon = p2[1]	
	
	plt.show()
