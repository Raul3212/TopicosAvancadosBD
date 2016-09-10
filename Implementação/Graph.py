class Graph:
    def __init__(self, numVertices):
        self.numVertices = numVertices
        self.adjList = []
        for i in range(numVertices):
            self.adjList.append([])

    def addVertex(self):
        self.numVertices += 1
        self.adjList.append([])

    def addEdge(self, u, v, w = 0):
        self.adjList[u].append((v,w))

    def getNumVertices(self):
        return self.numVertices

    def getVertices(self):
        return range(self.numVertices)

    def getAdj(self, u):
        try:
            return self.adjList[u]
        except:
            return []
