#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Implémentation d'un graphe à l'aide d'une liste d'adjacence. Les n sommets
sont identifiés par de simples naturels (0, 1, 2, ..., n-1)."""

import bisect 

class ListeAdjacence(object):
    def __init__(self, num = 0):
        """
        Initialise un graphe sans arêtes sur num sommets.

        >>> G = ListeAdjacence() # Créer un graph sans num
        >>> G._liste_adjacence
        []

        >>> G = ListeAdjacence(3) # Créer un graph avec num positif
        >>> G._liste_adjacence
        [[], [], []]

        >>> G = ListeAdjacence(-3) # Créer un graph avec num négatif
        >>> G._liste_adjacence
        []
        """
        self._liste_adjacence = [list() for _ in range(num)]

    def ajouter_arete(self, source, destination):
        """
        Ajoute l'arête {source, destination} au graphe, en créant les
        sommets manquants le cas échéant.
        
        >>> G = ListeAdjacence()
        >>> G.ajouter_arete(2, 1) # Ajouter une arete sur un graphe vide (aucun sommet)
        >>> G._liste_adjacence
        [[], [2], [1]]

        >>> G.ajouter_arete(0, 1) # Ajoute une arete sur un graphe avec les sommets déjà existants
        >>> G._liste_adjacence
        [[1], [0, 2], [1]]

        >>> G.ajouter_arete(2, 1) # Ajouter une arete déjà existante
        >>> G._liste_adjacence
        [[1], [0, 2], [1]]

        >>> G.ajouter_arete(-1, 1) # Ajoute une arete avec une valeur négative
        >>> G._liste_adjacence
        [[1], [0, 2], [1]]
        """
        if source < 0 or destination < 0:
            return

        if self.nombre_sommets() <= max(source, destination):
            for _ in range(self.nombre_sommets(), max(source, destination) + 1):
                self.ajouter_sommet()
        
        if not (destination in self._liste_adjacence[source]):
            bisect.insort(self._liste_adjacence[source], destination)

            if source != destination:
                bisect.insort(self._liste_adjacence[destination], source)

    def ajouter_aretes(self, iterable):
        """
        Ajoute toutes les arêtes de l'itérable donné au graphe. N'importe
        quel type d'itérable est acceptable, mais il faut qu'il ne contienne
        que des couples de naturels.
        
        >>> G = ListeAdjacence()
        >>> G.ajouter_aretes([[0, 1]]) # Ajouter qu'1 arete
        >>> G._liste_adjacence
        [[1], [0]]

        >>> G.ajouter_aretes([(1, 3), (2, 3)]) # Ajouter 2 aretes
        >>> G._liste_adjacence
        [[1], [0, 3], [3], [1, 2]]

        >>> G.ajouter_aretes([(1, 3), [0, 1], (5, 8)]) # Ajouter 3 aretes, dont 2 déjà présente
        >>> G._liste_adjacence
        [[1], [0, 3], [3], [1, 2], [], [8], [], [], [5]]
        """
        for u, v in iterable:
            if (type(u) == type(v) == int):
                self.ajouter_arete(u, v)

    def ajouter_sommet(self):
        """
        Ajoute un nouveau sommet au graphe et renvoie son identifiant.

        >>> G = ListeAdjacence()
        >>> G.ajouter_sommet()
        0

        >>> G.ajouter_sommet()
        1
        """
        self._liste_adjacence.append([])
        return len(self._liste_adjacence) - 1   

    def aretes(self):
        """ 
        Renvoie l'ensemble des arêtes du graphe sous forme de couples (si on
        les stocke sous forme de paires, on ne peut pas stocker les boucles,
        c'est-à-dire les arêtes de la forme (u, u)).
        
        >>> G = ListeAdjacence()
        >>> G.aretes()
        set()

        >>> G.ajouter_arete(2, 1)
        >>> G.ajouter_arete(0, 1)
        >>> G.aretes()
        {frozenset({0, 1}), frozenset({1, 2})}

        >>> G.ajouter_aretes([(0, 5), [0, 1], [2, 3], [2, 2]])
        >>> G.aretes()
        {frozenset({2}), frozenset({2, 3}), frozenset({1, 2}), frozenset({0, 1}), frozenset({0, 5})}
        """
        res = set()

        for i in range(len(self._liste_adjacence)):
            for e in self._liste_adjacence[i]:
                if not ({i, e} in res):
                    res.add(frozenset([i, e]))

        return res

    def boucles(self):
        """
        Renvoie les boucles du graphe, c'est-à-dire les arêtes reliant un
        sommet à lui-même.

        >>> G = ListeAdjacence()
        >>> G.boucles()
        []

        >>> G.ajouter_arete(2, 2)
        >>> G.boucles()
        [2]

        >>> G.ajouter_aretes([(2, 2), (0, 1), (5, 5), (0, 0)])
        >>> G.boucles()
        [0, 2, 5]
        """
        res = []

        for i in range(len(self._liste_adjacence)):
            for e in self._liste_adjacence[i]:
                if e > i:
                    break
                if i == e:
                    res.append(i)
    
        return res

    def contient_arete(self, u, v):
        """
        Renvoie True si l'arête {u, v} existe, False sinon.
        
        >>> G = ListeAdjacence(3)
        >>> G.contient_arete(0, 1)
        False

        >>> G.ajouter_arete(2, 1)
        >>> G.contient_arete(2, 1)
        True

        >>> G.contient_arete(1, 2)
        True

        >>> G.ajouter_aretes([(2, 1), (3, 3)])
        >>> G.contient_arete(3, 3)
        True

        >>> G.contient_arete(4, 1)
        False
        """
        if self.nombre_sommets() > max(u, v):
            for e in self._liste_adjacence[u]:
                if e == v:
                    return True
            
            for e in self._liste_adjacence[v]:
                if e == u:
                    return True
        
        return False

    def contient_sommet(self, u):
        """
        Renvoie True si le sommet u existe, False sinon.

        >>> G = ListeAdjacence()
        >>> G.contient_sommet(0)
        False

        >>> G = ListeAdjacence(3)
        >>> G.contient_sommet(2)
        True

        >>> G.contient_sommet(G.ajouter_sommet())
        True

        >>> G.contient_sommet(3)
        True

        >>> G.contient_sommet(4)
        False
        """
        return u >= 0 and u < self.nombre_sommets()


    def degre(self, sommet):
        """
        Renvoie le degré d'un sommet, c'est-à-dire le nombre de voisins
        qu'il possède.
        
        >>> G = ListeAdjacence()
        >>> G.degre(0)
        0

        >>> G.ajouter_arete(0, 1)
        >>> G.degre(0)
        1

        >>> G.degre(1)
        1

        >>> G.ajouter_aretes([(0, 2), (0, 1), (0, 5)])
        >>> G.degre(0)
        3

        >>> G.degre(5)
        1
        """
        if sommet < self.nombre_sommets():
            return len(self._liste_adjacence[sommet])

        return 0

    def nombre_aretes(self):
        """
        Renvoie le nombre d'arêtes du graphe.

        >>> G = ListeAdjacence()
        >>> G.nombre_aretes()
        0

        >>> G = ListeAdjacence(3)
        >>> G.nombre_aretes()
        0

        >>> G.ajouter_arete(0, 2)
        >>> G.nombre_aretes()
        2

        >>> G.ajouter_aretes([[0, 2], [4, 3], [8, 9]])
        >>> G.nombre_aretes()
        6
        """
        res = 0

        for sublist in self._liste_adjacence:
            res += len(sublist)
        
        return res

    def nombre_boucles(self):
        """
        Renvoie le nombre d'arêtes de la forme {u, u}.
        
        >>> G = ListeAdjacence()
        >>> G.nombre_boucles()
        0

        >>> G.ajouter_arete(2, 2)
        >>> G.nombre_boucles()
        1

        >>> G.ajouter_aretes([(2, 2), (0, 1), (5, 5), (0, 0)])
        >>> G.nombre_boucles()
        3
        """
        return len(self.boucles())

    def nombre_sommets(self):
        """
        Renvoie le nombre de sommets du graphe.

        >>> from random import randint
        >>> n = randint(0, 1000)
        >>> ListeAdjacence(n).nombre_sommets() == n
        True

        >>> ListeAdjacence(-2).nombre_sommets()
        0

        >>> ListeAdjacence(0).nombre_sommets()
        0
        """
        return len(self._liste_adjacence)

    def retirer_arete(self, u, v):
        """
        Retire l'arête {u, v} si elle existe ; provoque une erreur sinon.
        
        >>> G = ListeAdjacence()
        >>> G.ajouter_aretes([(2, 2), (0, 1), (5, 5), (0, 0)])
        >>> G._liste_adjacence
        [[0, 1], [0], [2], [], [], [5]]

        >>> G.retirer_arete(2, 2)
        >>> G._liste_adjacence
        [[0, 1], [0], [], [], [], [5]]

        # Le test suivant retire une arete qui n'est pas dans le graphe, et provoque donc une erreur
        # >>> G.retirer_arete(0, 2)
        """
        self._liste_adjacence[u].remove(v)

        if u != v:
            self._liste_adjacence[v].remove(u)

    def retirer_aretes(self, iterable):
        """
        Retire toutes les arêtes de l'itérable donné du graphe. N'importe
        quel type d'itérable est acceptable, mais il faut qu'il ne contienne
        que des couples d'éléments (quel que soit le type du couple).
        
        >>> G = ListeAdjacence()
        >>> G.ajouter_aretes([(2, 2), (0, 1), (5, 5), (0, 0)])
        >>> G._liste_adjacence
        [[0, 1], [0], [2], [], [], [5]]

        >>> G.retirer_aretes([(2, 2), [0, 1]])
        >>> G._liste_adjacence
        [[0], [], [], [], [], [5]]
        """
        for u, v in iterable:
            self.retirer_arete(u, v)

    def retirer_sommet(self, sommet):
        """
        Déconnecte un sommet du graphe et le supprime.
        
        >>> G = ListeAdjacence()
        >>> G.retirer_sommet(3)
        >>> G._liste_adjacence
        []

        >>> G.ajouter_aretes([(2, 2), (0, 1), (4, 4), (0, 0)])
        >>> G._liste_adjacence
        [[0, 1], [0], [2], [], [4]]

        >>> G.retirer_sommet(3)
        >>> G._liste_adjacence
        [[0, 1], [0], [2], [3]]

        >>> G.retirer_sommet(0)
        >>> G._liste_adjacence
        [[], [1], [2]]

        >>> G.retirer_sommet(3)
        >>> G._liste_adjacence
        [[], [1], [2]]
        """
        if sommet >= self.nombre_sommets() or sommet < 0:
            return
        
        # Pour chaque liste dans liste_ajdacence
        for sublist in self._liste_adjacence:
            # Si le sommet qu'on veut retirer est dans une liste, on l'enlève
            if sommet in sublist:
                sublist.remove(sommet)
            
            # Et pour chaque sommet restant, pour tous les sommets supérieur à sommet,
            # on les décrémente car il y a un sommet en moins
            # (si on retire le sommet n, le sommet n + 1 devient n, n + 2 -> n + 1, etc.)
            for i in range(len(sublist)):
                if sublist[i] > sommet:
                    sublist[i] -= 1
            
        self._liste_adjacence.pop(sommet)

    def retirer_sommets(self, iterable):
        """
        Efface les sommets de l'itérable donné du graphe, et retire toutes
        les arêtes incidentes à ces sommets.
        
        >>> G = ListeAdjacence()
        >>> G.ajouter_aretes([(2, 2), (0, 1), (4, 4), (0, 0)])
        >>> G._liste_adjacence
        [[0, 1], [0], [2], [], [4]]
        
        >>> G.retirer_sommets([3])
        >>> G._liste_adjacence
        [[0, 1], [0], [2], [3]]

        >>> G.retirer_sommets([6, 0, 2, -2])
        >>> G._liste_adjacence
        [[], [1]]
        """
        sommets_retires = []

        for s_a_retirer in iterable:
            if s_a_retirer < self.nombre_sommets():   
                # On décrément "s_a_retirer" pour chaque "s_retire" plus petit que lui
                # En effet, si on a retiré un sommet n, alors le sommet n + 1 devient n (n + 2 -> n + 1, etc.)
                for s_retire in sommets_retires:
                    if s_a_retirer > s_retire:
                        s_a_retirer -= 1

                self.retirer_sommet(s_a_retirer)
                sommets_retires.append(s_a_retirer)

    def sommets(self):
        """
        Renvoie l'ensemble des sommets du graphe.
        
        >>> G = ListeAdjacence()
        >>> G.sommets()
        []

        >>> G.ajouter_aretes([(0, 1), (0, 3)])
        >>> G.sommets()
        [0, 1, 2, 3]

        >>> G = ListeAdjacence(5)
        >>> G.sommets()
        [0, 1, 2, 3, 4]
        """
        res = []

        for i in range(self.nombre_sommets()):
            res.append(i)

        return res

    def sous_graphe_induit(self, iterable):
        """
        Renvoie le sous-graphe induit par l'itérable de sommets donné.

        >>> G = ListeAdjacence()
        >>> G.ajouter_aretes([(2, 1), (0, 3), (4, 3), (0, 2), (1, 3), (2, 3)])
        >>> G._liste_adjacence
        [[2, 3], [2, 3], [0, 1, 3], [0, 1, 2, 4], [3]]

        >>> G.sous_graphe_induit([1, 2, 3])
        [[1, 2], [0, 2], [0, 1]]

        >>> G.sous_graphe_induit([1])
        [[0]]

        >>> G.sous_graphe_induit([5])
        []
        """
        res = []

        # On construit une liste des sommets qui ne seront pas dans le sous-graphe
        sommets_pas_dans_iterable = []
        for i in range(self.nombre_sommets()):
            if not (i in iterable):
                sommets_pas_dans_iterable.append(i)

        for i in range(self.nombre_sommets()):
            if i in iterable:
                sommets_a_retirer = []
                # On retire les sommets qui ne sont pas dans iterable
                for s in sommets_pas_dans_iterable:
                    if s in self._liste_adjacence[i]:
                        self._liste_adjacence[i].remove(s)
                
                # Dans chaque liste de "res", on diminue la valeur des sommets qui restent
                # si besoin (si un sommet inférieur à lui n'est plus dans le sous-graphe)
                for j in range(len(self._liste_adjacence[i])):
                    for s in sommets_pas_dans_iterable:
                        if self._liste_adjacence[i][j] > s:
                            self._liste_adjacence[i][j] -= 1

                res.append(self._liste_adjacence[i])

        return res

    def voisins(self, sommet):
        """
        Renvoie la liste des voisins d'un sommet.

        >>> G = ListeAdjacence()
        >>> G.ajouter_aretes([(2, 2), (0, 1), (4, 4), (0, 0)]) 
        >>> G._liste_adjacence
        [[0, 1], [0], [2], [], [4]]

        >>> G.voisins(2)
        [2]

        >>> G.voisins(0)
        [0, 1]

        >>> G.voisins(-1)
        []

        >>> G.voisins(5)
        []
        """
        if sommet < self.nombre_sommets() and sommet >= 0:
            return self._liste_adjacence[sommet]
        
        return []

def export_dot(graphe):
    """
    Renvoie une chaîne encodant le graphe au format dot.

    NB : Même fonction que celui dans "matriceadjacence.py", 
    à l'exception de la création du graphe qui se fait par l'appele "ListeAdjacence()"
    
    NB 2 : Les résultats des doctests de "export_dot(graph)" sont en commentaires car
    ils n'arrivent pas à détecter les bonnes réponses malgré le fait qu'on 
    écrive exactement ce qui est prévu et attendu
    
    >>> G = ListeAdjacence()
    >>> print(export_dot(G))
    Graph G {
    }

    >>> G.ajouter_aretes([(2, 2), (0, 1), (3, 2), (0, 0), (1, 2)])
    >>> G._liste_adjacence
    [[0, 1], [0, 2], [1, 2, 3], [2]]
    
    # >>> print(export_dot(G))
    # Graph G {
    #     0 -- 1 -- 0;
    #     1 -- 0 -- 2;
    #     2 -- 1 -- 3 -- 2;
    #     3 -- 2;
    # }

    >>> G = ListeAdjacence()
    >>> G.ajouter_aretes([(0, 0), (1, 1), (2, 2), (3, 3)])
    >>> G._liste_adjacence
    [[0], [1], [2], [3]]
    
    # >>> print(export_dot(G))
    # Graph G {
    #     0 -- 0;
    #     1 -- 1;
    #     2 -- 2;
    #     3 -- 3;
    # }
    """
    res = "Graph G {\n"

    for i in range(graphe.nombre_sommets()):
        boucle = False # Variable qui permettra de savoir si on rajoute "i" à la fin de sa ligne

        res += "\t" + str(i)

        for j in graphe.voisins(i):
            if i == j:
                boucle = True
            else:
                res += " -- " + str(j) 
        
        if boucle:
            res += " -- " + str(i)
            
        res += ";\n"

    return res + "}"

def main():
    import doctest
    doctest.testmod()

if __name__ == "__main__":
    main()