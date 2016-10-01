class Ponto:
    def __init__(self, latitude, longitude):
        self.latitude = latitude
        self.longitude = longitude
        self.verticeProximo = None

    def setVerticeProximo(self, verticeProximo):
    	self.verticeProximo = verticeProximo