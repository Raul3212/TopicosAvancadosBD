#!/usr/bin/env python
# -*- coding: utf-8 -*-
class Ponto:

    def __init__(self, latitude, longitude):
        self.latitude = latitude
        self.longitude = longitude
        self.verticeProximo = None

	#Seta o valor para o vértice mais próximo ao ponto    
    def setVerticeProximo(self, verticeProximo):
    	self.verticeProximo = verticeProximo