import numpy as np
import pandas as pd
from datetime import datetime
import dateutil.parser

#def generate_text_file(length=1e6, ncols=20):
#    data = np.random.random((length, ncols))
#    np.savetxt('large_text_file.csv', data, delimiter=',')

def date_condition(tuple):
    return dateutil.parser.parse(str(tuple[1])).hour == 12

def convert_date(date):
    dataISO = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
    return np.datetime64(dataISO)

def group(lst, n):
  for i in range(0, len(lst), n):
    val = lst[i:i+n]
    if len(val) == n:
      yield tuple(val)

def iter_loadcsv(filename, dtypes, dtype, condition, delimiter=';', skiprows=0):
    def iter_func():
        with open(filename, 'r') as infile:
            for _ in range(skiprows):
                next(infile)
            for line in infile:
                line = line.rstrip().split(delimiter)
                list_line = []
                for i in range ( len(dtypes) ):
                    #print dtypes[i](line[i])
                    list_line.append(dtypes[i](line[i]))
                tuple = list(group(list_line, len(dtypes)))[0]
                if(condition(tuple)):
                    #print tuple
                    yield tuple     
        iter_loadcsv.rowlength = len(dtypes)
           
    data = np.fromiter(iter_func(), dtype=dtype)
    return data

#generate_text_file()
dtypes = [int, convert_date, float, float];
dtype = [('', int), ('', 'datetime64[us]' ), ('', float), ('',float)];

data = iter_loadcsv('../data/tdrive.csv', dtypes, dtype, date_condition)
print data