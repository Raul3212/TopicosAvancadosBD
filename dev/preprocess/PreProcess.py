#!/usr/bin/env python
# -*- coding: utf-8 -*-

from database.Connection import *
from database.VerticeDAO import *
from database.TaxistaDAO import *
from database.RotasDAO import *
import numpy as np
import pandas as pd
from datetime import datetime
import dateutil.parser

#Quantidade de linhas do csv de drivers
TDRIVELINES = 18000000 
#Quantidade de linhas do csv de vértices
TVERTICESLINES = 40463
#Quantidade de linhas do csv de rotas
TROADSLINES = 56332

#Função que define filtro por data
#Pegando apenas os que estão entre 12:00 e 12:59
def date_condition(row):
    return dateutil.parser.parse(str(row[1])).hour == 12

#Condição default retorna todas as linhas
def default_condition(arg):
    return True        

#Função auxiliar que converte string para data
def convert_date(date):
    dataISO = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
    return np.datetime64(dataISO)

#transforma uma lista em tupla
def group(lst, n):
  for i in range(0, len(lst), n):
    val = lst[i:i+n]
    if len(val) == n:
      yield tuple(val)

#limit default -1 : lê todas as linhas
#skiprows default 1: tira a linha de cabeçalho, caso a linha não exista colocar 0
#Função que lê csv e retorna lista de tuplas com os valores de cada linha
def iter_loadcsv(filename, dtypes, dtype, condition, delimiter=';', skiprows=1, limit = -1):
    def iter_func():
        with open(filename, 'r') as infile:
            for _ in range(skiprows):
                next(infile)
            rows = 0;
            for line in infile:
                line = line.rstrip().split(delimiter)
                list_line = []
                for i in range ( len(dtypes) ):
                    #print dtypes[i](line[i])
                    list_line.append(dtypes[i](line[i]))
                row = list(group(list_line, len(dtypes)))[0]
                if(condition(row)):
                    #print row
                    yield row
                rows=rows+1
                print rows
                if(limit != -1 and rows >= limit):
                    break 
        iter_loadcsv.rowlength = len(dtypes)
           
    data = np.fromiter(iter_func(), dtype=dtype)
    return data

#Função para preprocessamento de vértices salvando os dados no banco
#pathCsv: caminho para arquivo do csv de vértices
def preprocessVertices(pathCsv):
    
    #tipos de acordo com o csv
    dtypes = [int, float, float];
    dtype = [('', int), ('', float), ('',float)];

    data = iter_loadcsv(pathCsv, dtypes, dtype, default_condition)
    #print data
    connectionFactory = ConnectionFactory()
    verticeDAO = VerticeDAO(connectionFactory.getConnection())
    if(len(data) > 0):
        verticeDAO.executeMany(data)

#Função para preprocessamento de taxistas salvando os dados no banco
#pathCsv: caminho para arquivo do csv de taxistas
def preprocessTaxistas(pathCsv):

    #tipos de acordo com o csv
    dtypes = [int, str, float, float];
    dtype = [('', int), ('', '|S20'), ('', float), ('',float)];
    
    connectionFactory = ConnectionFactory()
    taxistaDAO = TaxistaDAO(connectionFactory.getConnection())
    
    data = iter_loadcsv(pathCsv, dtypes, dtype, date_condition)
    if(len(data) > 0):
        taxistaDAO.executeMany(data)    

#Função para preprocessamento de rotas salvando os dados no banco
#pathCsv: caminho para arquivo do csv de rotas
def preprocessRotas(pathCsv):
    
    #tipos de acordo com o csv
    dtypes = [int, int, int, float];
    dtype = [('', int), ('', int), ('', int), ('',float)];

    connectionFactory = ConnectionFactory()
    rotasDAO = RotasDAO(connectionFactory.getConnection())
    data = iter_loadcsv(pathCsv, dtypes, dtype, default_condition)
    if(len(data) > 0):
        rotasDAO.executeMany(data)
    
