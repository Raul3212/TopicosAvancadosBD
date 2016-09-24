from math import pow,sqrt

class Taxista:
    def __init__(self, id, time, latitude, longitude):
        self.id = id
        self.latitude = latitude
        self.longitude = longitude
        self.time = time    

    def distance(self, taxista):
    	return sqrt (pow((self.latitude - taxista.latitude),2.0) + pow((self.longitude - taxista.longitude),2.0))