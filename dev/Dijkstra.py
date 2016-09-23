from Graph import *
import Queue as Q

class Dijkstra:
    def __init__(self, graph, s):
        self.graph = graph
        self.p = []
        self.d = []
        self.heap = Q.PriorityQueue()
        for n in graph.getVertices():
            self.p.append(-1)
            self.d.append(float('inf'))
            self.heap.put(n)
        self.d[s] = 0

    def relax(self, u, v, w):
        if self.d[v] > self.d[u] + w:
            self.d[v] = self.d[u] + w
            self.p[v] = u

    def run(self):
        while not self.heap.empty():
            u = self.heap.get()
            for (v, w) in self.graph.getAdj(u):
                self.relax(u, v, w)
        return self.p
