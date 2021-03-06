#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Graph import *
from heapq import *

# Método para manter invariante da heap depois de uma modificação de valor.
# Considerando que a distância sempre será menor a cada atualização (relaxamento),
# o método coloca a posição atualizada na posição correta utilizando dessa informação, ou seja,
# o elemento da posição 'pos' vai ser atualizado com comparação aos seus 'pais', até chegar na posição correta
def siftdown(heap, startpos, pos):
    newitem = heap[pos]
    # Percorre o caminho até a raiz, movendo os pais para baixo até achar o local certo
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
    #iniciando dijkstra
    def __init__(self, graph, s, eps = float('inf')):
        self.graph = graph
        self.p = {}   
        self.d = {}
        self.eps = eps
        self.vizinhos = set()
        self.vizinhos.add(s) #considerando que o vértice é vizinho dele próprio, útil para o DBSCAN 
        self.visitados = [False] * graph.getNumVertices()
        self.heap = []
        #iniciando todos os vértices com precedente -1 e distância infinita
        for n in graph.getVertices():
            self.p[n] = -1
            self.d[n] = float('inf')
        #iniciando vértice s com d = 0 e como visitado
        self.d[s] = 0
        self.visitados[s] = True
        #adicionando s na heap
        heappush(self.heap, (self.d[s], s))

    #relaxação do vértice
    def relax(self, u, v, w):
        if self.d[v] > self.d[u] + w:
            indexV = self.heap.index((self.d[v], v))
            self.d[v] = self.d[u] + w
            # se a distância do vértice para s for menor ou igual a eps,
            # então ele é vizinho de eps
            if self.d[v] <= self.eps:
                self.vizinhos.add(v)
            self.p[v] = u
            self.heap[indexV] = (self.d[v], v)
            #atualizando a heap
            siftdown(self.heap, 0, indexV)

    def run(self):
        #retirando elementos da heap até a heap estar vazia
        while len(self.heap) != 0:
            priority, u = heappop(self.heap)
            # O dijkstra modificado está interessado apenas 
            # em achar vizinhos do vértice na rede dentro de um valor eps.
            # Caso a distância para um vértice já seja maior que eps, 
            # então o relaxamento dos seus filhos também será,
            # sendo assim a relaxação dos filhos é descartada.
            # Além disso, podemos parar a execução, pois a min heap garante 
            # que os elementos restantes na heap terão distância maior  
            if self.d[u] > self.eps: 
                break
            for (v, w) in self.graph.getAdj(u):
                if not self.visitados[v]:
                    heappush(self.heap, (self.d[v], v))
                    self.visitados[v] = True                        
                self.relax(u, v, w)
        return self.vizinhos

