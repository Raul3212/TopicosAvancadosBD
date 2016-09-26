import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap

def plot(positions):
	fig = plt.figure()

	themap = Basemap(projection='gall',
              llcrnrlon = np.amin(positions[:,0]),              # lower-left corner longitude
              llcrnrlat = np.amin(positions[:,1]),               # lower-left corner latitude
              urcrnrlon = np.amax(positions[:,0]),               # upper-right corner longitude
              urcrnrlat = np.amax(positions[:,1]),               # upper-right corner latitude
              resolution = 'l',
              area_thresh = 100000.0,
              )
              
	themap.drawcoastlines()
	themap.drawcountries()
	themap.fillcontinents(color = 'gainsboro')
	themap.drawmapboundary(fill_color='steelblue')

	x, y = themap(positions[:,0], positions[:,1])
	themap.plot(x, y, 
	            'o',                    # marker shape
	            color='Indigo',         # marker colour
	            markersize=4            # marker size
	            )

	plt.show()
