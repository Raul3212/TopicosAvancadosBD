class Graph:
    #inicia grafo com uma mapa de vértices
    def __init__(self, vertices):
        self.numVertices = len(vertices)
        self.adjList = {}
        #para cada vértice é criada uma lista de adjacência
        for vertice in vertices:
            self.adjList[vertice.id] = []

    #adiciona vértice no grafo
    def addVertex(self, vertice):
        self.numVertices += 1
        self.adjList[vertice] = []

    #adiciona aresta no grafo    
    def addEdge(self, u, v, w = 0):
        self.adjList[u].append((v,w))

    #retorna número de vértices
    def getNumVertices(self):
        return self.numVertices

    #retorna id dos vértices
    def getVertices(self):
        return self.adjList.keys()

    #pega lista de adjacência do vértice com id u
    def getAdj(self, u):
        try:
            return self.adjList[u]
        except:
            return {}
