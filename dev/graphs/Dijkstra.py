from Graph import *
from heapq import *


# 'heap' is a heap at all indices >= startpos, except possibly for pos.  pos
# is the index of a leaf with a possibly out-of-order value.  Restore the
# heap invariant.
def siftdown(heap, startpos, pos):
    newitem = heap[pos]
    # Follow the path to the root, moving parents down until finding a place
    # newitem fits.
    while pos > startpos:
        parentpos = (pos - 1) >> 1
        parent = heap[parentpos]
        if newitem < parent:
            heap[pos] = parent
            pos = parentpos
            continue
        break
    heap[pos] = newitem

class DijkstraModificado:
    def __init__(self, graph, s, eps = float('inf')):
        self.graph = graph
        self.p = {}   
        self.d = {}
        self.eps = eps
        self.vizinhos = set()
        self.visitados = [False] * graph.getNumVertices()
        self.heap = []
        for n in graph.getVertices():
            self.p[n] = -1
            self.d[n] = float('inf')
        self.d[s] = 0
        self.visitados[s] = True
        heappush(self.heap, (self.d[s], s))

    def relax(self, u, v, w):
        if self.d[v] > self.d[u] + w:
            indexV = self.heap.index((self.d[v], v))
            self.d[v] = self.d[u] + w
            if self.d[v] <= self.eps:
                self.vizinhos.add(v)
            self.p[v] = u
            self.heap[indexV] = (self.d[v], v)
            siftdown(self.heap, 0, indexV)

    def run(self):
        while len(self.heap) != 0:
            priority, u = heappop(self.heap)
            if self.d[u] > self.eps: 
                continue
            for (v, w) in self.graph.getAdj(u):
                if not self.visitados[v]:
                    heappush(self.heap, (self.d[v], v))
                    self.visitados[v] = True                        
                self.relax(u, v, w)
        return (self.p, self.d, self.vizinhos)

