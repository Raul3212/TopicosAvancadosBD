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

#def generate_text_file(length=1e6, ncols=20):
#    data = np.random.random((length, ncols))
#    np.savetxt('large_text_file.csv', data, delimiter=',')

TDRIVELINES = 18000000
TVERTICESLINES = 40463
TROADSLINES = 56332

def date_condition(row):
    return dateutil.parser.parse(str(row[1])).hour == 12

def default_condition(arg):
    return True        

def convert_date(date):
    dataISO = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
    return np.datetime64(dataISO)

def group(lst, n):
  for i in range(0, len(lst), n):
    val = lst[i:i+n]
    if len(val) == n:
      yield tuple(val)

#limit default -1 : lê todas as linhas
#skiprows default 1: tira a linha de cabeçalho, caso a linha não exista colocar 0
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

def preprocessVertices(pathCsv):
    dtypes = [int, float, float];
    dtype = [('', int), ('', float), ('',float)];

    data = iter_loadcsv(pathCsv, dtypes, dtype, default_condition)
    #print data
    connectionFactory = ConnectionFactory()
    verticeDAO = VerticeDAO(connectionFactory.getConnection())
    if(len(data) > 0):
        verticeDAO.executeMany(data)

def preprocessTaxistas(pathCsv):

    dtypes = [int, str, float, float];
    dtype = [('', int), ('', '|S20'), ('', float), ('',float)];
    
    connectionFactory = ConnectionFactory()
    taxistaDAO = TaxistaDAO(connectionFactory.getConnection())
    
    data = iter_loadcsv(pathCsv, dtypes, dtype, date_condition)
    if(len(data) > 0):
        taxistaDAO.executeMany(data)
    skiprows += step
    

def preprocessRotas(pathCsv):
    
    dtypes = [int, int, int, float];
    dtype = [('', int), ('', int), ('', int), ('',float)];

    connectionFactory = ConnectionFactory()
    rotasDAO = RotasDAO(connectionFactory.getConnection())
    data = iter_loadcsv(pathCsv, dtypes, dtype, default_condition)
    if(len(data) > 0):
        rotasDAO.executeMany(data)
    