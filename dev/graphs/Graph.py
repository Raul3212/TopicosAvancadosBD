class Graph:
    def __init__(self, vertices):
        self.numVertices = len(vertices)
        self.adjList = {}
        for vertice in vertices:
            self.adjList[vertice] = []

    def addVertex(self, vertice):
        self.numVertices += 1
        self.adjList[vertice] = []

    def addEdge(self, u, v, w = 0):
        self.adjList[u].append((v,w))

    def getNumVertices(self):
        return self.numVertices

    def getVertices(self):
        return self.adjList.keys()

    def getAdj(self, u):
        try:
            return self.adjList[u]
        except:
            return {}
