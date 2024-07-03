import copy
import math
import geopy

import networkx as nx
from geopy.distance import geodesic

from database.DAO import DAO


class Model:
    def __init__(self):
        self._grafo = nx.Graph()
        self._bestPath = []
        self._bestDistance = 0

    def getPath(self):
        self._bestPath = []
        self._bestDistance = 0
        parziale = []
        for node in self._grafo.nodes:
            parziale.append(node)
            self._ricorsione(parziale)
            parziale.pop()
        return self._bestPath, self._bestDistance

    def _ricorsione(self,parziale):
        #CONDIZIONE FINALE
        if self.calcolaDistanza(parziale)>self._bestDistance:
            self._bestDistance = self.calcolaDistanza(parziale)
            self._bestPath = copy.deepcopy(parziale)
            #NON ESCO PERCHE POSSO AGGIUNGERE

        #CONDIZIONE PER AGGIUNGERE:
        for node in self._grafo.neighbors(parziale[-1]):
            if node not in parziale:#VERIFICO CHE IL CAMMINO E' SEMPLICE
                if len(parziale)<2:
                    parziale.append(node)
                    self._ricorsione(parziale)
                    parziale.pop()
                else:
                    print(self._grafo[parziale[-1]][node]["weight"])
                    print(self._grafo[parziale[-2]][parziale[-1]]["weight"])
                    if self._grafo[parziale[-1]][node]["weight"]>self._grafo[parziale[-2]][parziale[-1]]["weight"]:
                        parziale.append(node)
                        self._ricorsione(parziale)
                        parziale.pop()

    def calcolaDistanza(self,listOfNodes):
        distanza = 0
        if len(listOfNodes)<2:
            return distanza
        for i in range(0, len(listOfNodes) - 1):
            nodo1 = listOfNodes[i]
            nodo2 = listOfNodes[i + 1]
            distanza += geodesic((nodo1.Lat, nodo1.Lng), (nodo2.Lat, nodo2.Lng)).kilometers
        return distanza

    def distanzaGeo(self,nodo1,nodo2):
        return geodesic((nodo1.Lat, nodo1.Lng), (nodo2.Lat, nodo2.Lng)).kilometers





    def fillDD(self,anno):
        forme = DAO.getShape(anno)
        return forme

    def buildGraph(self,anno,forma):
        self.stati = DAO.getStates()
        self._grafo.add_nodes_from(self.stati)
        self._creaArchi(anno,forma)

    def _creaArchi(self,anno,forma):
        self._grafo.clear_edges()
        for u in self._grafo.nodes:
            for v in self._grafo.nodes:
                if u != v:
                    result = DAO.getNeighbors()
                    for r in result:
                        if u.id ==r[0] and v.id ==r[1]:
                            peso = int(DAO.getPeso(u.id,v.id,anno,forma)[0])
                            self._grafo.add_edge(u,v,weight= peso)

    def adiacenze(self):
        lista = []
        for ele in self._grafo.nodes:
            somma = 0
            for vicino in self._grafo.neighbors(ele):
                somma += self._grafo[ele][vicino]["weight"]
            lista.append((ele,somma))
        return lista
    def graphDetails(self):
        return len(self._grafo.nodes),len(self._grafo.edges)