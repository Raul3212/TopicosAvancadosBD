import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap



def plot(dataset, clusters, p1, p2):
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
	cores = ['Green', 'Blue', 'Red', 'Indigo', 'Black']
	i = 0
	for cluster in clusters: 
		for indexTaxista in cluster:
			taxista = dataset[indexTaxista]
			x,y = themap(taxista.longitude, taxista.latitude) 
			themap.plot(x,y, 
	            'o',                    # marker shape
	            color=cores[i % len(cores)],         # marker colour
	            markersize=4            # marker size
	            )
		i=i+1

	themap.llcrnrlon = p1[0]
	themap.llcrnrlat = p1[1]
	themap.urcrnrlon = p2[0]
	themap.urcrnrlon = p2[1]	
	
	plt.show()
