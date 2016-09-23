import numpy as np

#def generate_text_file(length=1e6, ncols=20):
#    data = np.random.random((length, ncols))
#    np.savetxt('large_text_file.csv', data, delimiter=',')

def iter_loadtxt(filename, delimiter=';', skiprows=0, dtype=str):
    def iter_func():
        with open(filename, 'r') as infile:
            for _ in range(skiprows):
                next(infile)
            for line in infile:
                line = line.rstrip().split(delimiter)
                for item in line:
                    yield dtype(item)
                    #print item
        iter_loadtxt.rowlength = len(line)

    data = np.fromiter(iter_func(), dtype='|S20')
    data = data.reshape((-1, iter_loadtxt.rowlength))
    return data

#generate_text_file()
data = iter_loadtxt('data/tdrive.csv')
print len(data)