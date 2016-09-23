from Graph import *
from Dijkstra import *

g = Graph(6)
g.addEdge(0, 1, 10)
g.addEdge(0, 2, 5)
g.addEdge(1, 2, 3)
g.addEdge(1, 3, 1)
g.addEdge(2, 1, 2)
g.addEdge(2, 3, 9)
g.addEdge(2, 4, 2)
g.addEdge(3, 4, 4)
g.addEdge(3, 5, 3)
g.addEdge(4, 0, 7)
g.addEdge(4, 3, 6)
g.addEdge(4, 5, 5)

dijkstra = Dijkstra(g, 0)
r = dijkstra.run()

print r
