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
    #generate_text_file()
    #dtypes = [int, convert_date, float, float];
    #dtype = [('', int), ('', 'datetime64[us]' ), ('', float), ('',float)];
    dtypes = [int, float, float];
    dtype = [('', int), ('', float), ('',float)];

    data = iter_loadcsv(pathCsv, dtypes, dtype, default_condition)
    #print data
    connectionFactory = ConnectionFactory()
    verticeDAO = VerticeDAO(connectionFactory.getConnection())
    verticeDAO.executeMany(data)

def preprocessTaxistas(pathCsv):
    #generate_text_file()
    #dtypes = [int, convert_date, float, float];
    #dtype = [('', int), ('', 'datetime64[us]' ), ('', float), ('',float)];

    dtypes = [int, str, float, float];
    dtype = [('', int), ('', '|S20'), ('', float), ('',float)];
    

    connectionFactory = ConnectionFactory()
    taxistaDAO = TaxistaDAO(connectionFactory.getConnection())
    
    #inicie o skiprows com a ultima linha lida ate o momento
    skiprows = 1
    step = 100000
    while(skiprows < TDRIVELINES):
        data = iter_loadcsv(pathCsv, dtypes, dtype, date_condition, skiprows = skiprows, limit = step)
        print data
        taxistaDAO.executeMany(data)
        skiprows += step
    

def preprocessRotas(pathCsv):
    
    dtypes = [int, int, int, float];
    dtype = [('', int), ('', int), ('', int), ('',float)];
    

    connectionFactory = ConnectionFactory()
    rotasDAO = RotasDAO(connectionFactory.getConnection())

    skiprows = 1
    step = 10000
    while(skiprows < TROADSLINES):
        data = iter_loadcsv(pathCsv, dtypes, dtype, default_condition, skiprows = skiprows, limit = step)
        print data
        rotasDAO.executeMany(data)
        skiprows += step
    