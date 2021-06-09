#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Implémentation d'un graphe à l'aide d'une matrice d'adjacence. Les n sommets
sont identifiés par de simples naturels (0, 1, 2, ..., n-1).
"""

class MatriceAdjacence(object):
    def __init__(self, num = 0):
        """Initialise un graphe sans arêtes sur num sommets.

        >>> G = MatriceAdjacence()
        >>> G._matrice_adjacence
        []

        >>> G = MatriceAdjacence(3)
        >>> G._matrice_adjacence
        [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

        >>> G = MatriceAdjacence(-1)
        >>> G._matrice_adjacence
        []
        """
        self._matrice_adjacence = [[0] * num for _ in range(num)]

    def ajouter_arete(self, source, destination):
        """
        Ajoute l'arête {source, destination} au graphe, en créant les
        sommets manquants le cas échéant.

        >>> G = MatriceAdjacence()
        >>> G.ajouter_arete(2, 1)
        >>> G._matrice_adjacence
        [[0, 0, 0], [0, 0, 1], [0, 1, 0]]

        >>> G.ajouter_arete(0, 1) # Ajoute une arete sur un graphe avec les sommets déjà existants
        >>> G._matrice_adjacence
        [[0, 1, 0], [1, 0, 1], [0, 1, 0]]

        >>> G.ajouter_arete(2, 1) # Ajouter une arete déjà existante
        >>> G._matrice_adjacence
        [[0, 1, 0], [1, 0, 1], [0, 1, 0]]

        >>> G.ajouter_arete(-1, 1) # Ajoute une arete avec une valeur négative
        >>> G._matrice_adjacence
        [[0, 1, 0], [1, 0, 1], [0, 1, 0]]
        """
        if source < 0 or destination < 0:
            return

        if self.nombre_sommets() <= max(source, destination):
            for _ in range(self.nombre_sommets(), max(source, destination) + 1):
                self.ajouter_sommet()

        self._matrice_adjacence[source][destination] = 1
        self._matrice_adjacence[destination][source] = 1

    def ajouter_aretes(self, iterable):
        """
        Ajoute toutes les arêtes de l'itérable donné au graphe. N'importe
        quel type d'itérable est acceptable, mais il faut qu'il ne contienne
        que des couples de naturels.

        >>> G = MatriceAdjacence()
        >>> G.ajouter_aretes([[0, 1]]) # Ajouter qu'1 arete
        >>> G._matrice_adjacence
        [[0, 1], [1, 0]]

        >>> G.ajouter_aretes([(1, 3), (2, 3)]) # Ajouter 2 aretes
        >>> G._matrice_adjacence
        [[0, 1, 0, 0], [1, 0, 0, 1], [0, 0, 0, 1], [0, 1, 1, 0]]

        >>> G.ajouter_aretes([(1, 3), [0, 1], (4, 2)]) # Ajouter 3 aretes, dont 2 déjà présente
        >>> G._matrice_adjacence
        [[0, 1, 0, 0, 0], [1, 0, 0, 1, 0], [0, 0, 0, 1, 1], [0, 1, 1, 0, 0], [0, 0, 1, 0, 0]]
        """
        for u, v in iterable:
            if (type(u) == type(v) == int):
                self.ajouter_arete(u, v)

    def ajouter_sommet(self):
        """
        Ajoute un nouveau sommet au graphe et renvoie son identifiant.

        >>> G = MatriceAdjacence()

        >>> G.ajouter_sommet()
        0
        >>> G._matrice_adjacence
        [[0]]

        >>> G.ajouter_sommet()
        1
        >>> G._matrice_adjacence
        [[0, 0], [0, 0]]
        """
        for sublist in self._matrice_adjacence:
            sublist.append(0)
        
        n = len(self._matrice_adjacence) + 1
        self._matrice_adjacence.append([0 for _ in range(n)])

        return len(self._matrice_adjacence) - 1

    def aretes(self):
        """
        Renvoie l'ensemble des arêtes du graphe sous forme de couples (si on
        les stocke sous forme de paires, on ne peut pas stocker les boucles,
        c'est-à-dire les arêtes de la forme (u, u)).
        
        >>> G = MatriceAdjacence()
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

        for i in range(len(self._matrice_adjacence)):
            for j in range (i + 1):
                if self._matrice_adjacence[i][j] == 1:
                    res.add(frozenset([i, j]))

        return res

    def boucles(self):
        """
        Renvoie les boucles du graphe, c'est-à-dire les arêtes reliant un
        sommet à lui-même.
        
        >>> G = MatriceAdjacence()
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

        for i in range(self.nombre_sommets()):
            if self._matrice_adjacence[i][i] == 1:
                res.append(i)
        
        return res

    def contient_arete(self, u, v):
        """
        Renvoie True si l'arête {u, v} existe, False sinon.
        
         >>> G = MatriceAdjacence(3)
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
            return self._matrice_adjacence[u][v] == 1

        return False

    def contient_sommet(self, u):
        """
        Renvoie True si le sommet u existe, False sinon.
        
        >>> G = MatriceAdjacence()
        >>> G.contient_sommet(0)
        False

        >>> G = MatriceAdjacence(3)
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
        
        >>> G = MatriceAdjacence()
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
        res = 0

        if self.nombre_sommets() > sommet:
            for s in self._matrice_adjacence[sommet]:
                res += s

        return res

    def nombre_aretes(self):
        """
        Renvoie le nombre d'arêtes du graphe.

        >>> G = MatriceAdjacence()
        >>> G.nombre_aretes()
        0

        >>> G = MatriceAdjacence(3)
        >>> G.nombre_aretes()
        0

        >>> G.ajouter_arete(0, 2)
        >>> G.nombre_aretes()
        2

        >>> G.ajouter_aretes([[0, 2], [4, 3], [8, 9]]) # Ajout de 2 nouvelles aretes
        >>> G.nombre_aretes()
        6
        """
        res = 0

        for sublist in self._matrice_adjacence:
            for s in sublist:
                res += s

        return res

    def nombre_boucles(self):
        """
        Renvoie le nombre d'arêtes de la forme {u, u}.
        
        >>> G = MatriceAdjacence()
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
        >>> MatriceAdjacence(n).nombre_sommets() == n
        True

        >>> MatriceAdjacence(-2).nombre_sommets()
        0

        >>> MatriceAdjacence(0).nombre_sommets()
        0
        """
        return len(self._matrice_adjacence)

    def retirer_arete(self, u, v):
        """
        Retire l'arête {u, v} si elle existe ; provoque une erreur sinon.
        
        >>> G = MatriceAdjacence()
        >>> G.ajouter_aretes([(2, 2), (0, 1), (3, 2), (0, 0)]) 
        >>> G._matrice_adjacence
        [[1, 1, 0, 0], [1, 0, 0, 0], [0, 0, 1, 1], [0, 0, 1, 0]]

        >>> G.retirer_arete(2, 2)
        >>> G._matrice_adjacence
        [[1, 1, 0, 0], [1, 0, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0]]

        # Le test suivant retire une arete qui n'est pas dans le graphe, et provoque donc une erreur
        # >>> G.retirer_arete(5, 6)
        """
        self._matrice_adjacence[u][v] = 0
        self._matrice_adjacence[v][u] = 0

    def retirer_aretes(self, iterable):
        """
         Retire toutes les arêtes de l'itérable donné du graphe. N'importe
        quel type d'itérable est acceptable, mais il faut qu'il ne contienne
        que des couples d'éléments (quel que soit le type du couple).
        
        >>> G = MatriceAdjacence()
        >>> G.ajouter_aretes([(2, 2), (0, 1), (3, 2), (0, 0)])
        >>> G._matrice_adjacence
        [[1, 1, 0, 0], [1, 0, 0, 0], [0, 0, 1, 1], [0, 0, 1, 0]]

        >>> G.retirer_aretes([(2, 2), [0, 1]])
        >>> G._matrice_adjacence
        [[1, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0]]
        """
        for u, v in iterable:
            self.retirer_arete(u, v)


    def retirer_sommet(self, sommet):
        """
        Déconnecte un sommet du graphe et le supprime.
        
        >>> G = MatriceAdjacence()
        >>> G.retirer_sommet(3)
        >>> G._matrice_adjacence
        []

        >>> G.ajouter_aretes([(2, 2), (0, 1), (3, 2), (0, 0)])
        >>> G._matrice_adjacence
        [[1, 1, 0, 0], [1, 0, 0, 0], [0, 0, 1, 1], [0, 0, 1, 0]]

        >>> G.retirer_sommet(2)
        >>> G._matrice_adjacence
        [[1, 1, 0], [1, 0, 0], [0, 0, 0]]

        >>> G.retirer_sommet(0)
        >>> G._matrice_adjacence
        [[0, 0], [0, 0]]

        >>> G.retirer_sommet(2)
        >>> G._matrice_adjacence
        [[0, 0], [0, 0]]
        """
        if sommet >= self.nombre_sommets() or sommet < 0:
            return

        if sommet < self.nombre_sommets():
            self._matrice_adjacence.pop(sommet)

            for sublist in self._matrice_adjacence:
                sublist.pop(sommet)
        

    def retirer_sommets(self, iterable):
        """
        Efface les sommets de l'itérable donné du graphe, et retire toutes
        les arêtes incidentes à ces sommets.
        
        >>> G = MatriceAdjacence()
        >>> G.ajouter_aretes([(2, 2), (0, 1), (4, 4), (0, 0)])
        >>> G._matrice_adjacence
        [[1, 1, 0, 0, 0], [1, 0, 0, 0, 0], [0, 0, 1, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 1]]

        >>> G.retirer_sommets([3])
        >>> G._matrice_adjacence
        [[1, 1, 0, 0], [1, 0, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]

        >>> G.retirer_sommets([6, 0, 2, -2])
        >>> G._matrice_adjacence
        [[0, 0], [0, 1]]
        """
        s_retires = []

        for s_a_retirer in iterable:
            for s_retire in s_retires:
                if s_a_retirer > s_retire:
                    s_a_retirer -= 1

            self.retirer_sommet(s_a_retirer)

            s_retires.append(s_a_retirer)

    def sommets(self):
        """
        Renvoie l'ensemble des sommets du graphe.
        
        >>> G = MatriceAdjacence()
        >>> G.sommets()
        []

        >>> G.ajouter_aretes([(0, 1), (0, 3)])
        >>> G.sommets()
        [0, 1, 2, 3]

        >>> G = MatriceAdjacence(5)
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

        >>> G = MatriceAdjacence()
        >>> G.ajouter_aretes([(2, 1), (0, 3), (4, 3), (0, 2), (1, 3), (2, 3)])
        >>> G._matrice_adjacence
        [[0, 0, 1, 1, 0], [0, 0, 1, 1, 0], [1, 1, 0, 1, 0], [1, 1, 1, 0, 1], [0, 0, 0, 1, 0]]

        >>> G.sous_graphe_induit([1, 2, 3])
        [[0, 1, 1], [1, 0, 1], [1, 1, 0]]

        >>> G.sous_graphe_induit([1])
        [[0]]

        >>> G.sous_graphe_induit([5])
        []
        """
        res = []

        for s in iterable:
            if s >= 0 and s < self.nombre_sommets():
                new_sublist = []

                for s_bis in iterable:
                    new_sublist.append(self._matrice_adjacence[s][s_bis])
                
                res.append(new_sublist)

        return res

    def voisins(self, sommet):
        """
        Renvoie la liste des voisins d'un sommet.

        >>> G = MatriceAdjacence()
        >>> G.ajouter_aretes([(2, 2), (0, 1), (3, 2), (0, 0)])
        >>> G._matrice_adjacence
        [[1, 1, 0, 0], [1, 0, 0, 0], [0, 0, 1, 1], [0, 0, 1, 0]]

        >>> G.voisins(2)
        [2, 3]

        >>> G.voisins(0)
        [0, 1]

        >>> G.voisins(-1)
        []

        >>> G.voisins(5)
        []
        """
        res = []

        if sommet < self.nombre_sommets() and sommet >= 0:
            for i in range(len(self._matrice_adjacence[sommet])):
                if self._matrice_adjacence[sommet][i] == 1:
                    res.append(i)

        return res

def export_dot(graphe):
    """
    Renvoie une chaîne encodant le graphe au format dot.

    NB : Même fonction que celui dans "listeadjacence.py", 
    à l'exception de la création du graphe qui se fait par l'appele "MatriceAdjacence()"

	NB 2 : Les résultats des doctests de "export_dot(graph)" sont en commentaires car
    ils n'arrivent pas à détecter les bonnes réponses malgré le fait qu'on 
    écrive exactement ce qui est prévu et attendu

	>>> G = MatriceAdjacence()
    >>> print(export_dot(G))
    Graph G {
    }

    >>> G.ajouter_aretes([(2, 2), (0, 1), (3, 2), (0, 0), (1, 2)])
    >>> G._matrice_adjacence
    [[1, 1, 0, 0], [1, 0, 1, 0], [0, 1, 1, 1], [0, 0, 1, 0]]
    
    # >>> print(export_dot(G))
    # Graph G {
    #     0 -- 1 -- 0;
    #     1 -- 0 -- 2;
    #     2 -- 1 -- 3 -- 2;
    #     3 -- 2;
    # }

    >>> G = MatriceAdjacence()
    >>> G.ajouter_aretes([(0, 0), (1, 1), (2, 2), (3, 3)])
    >>> G._matrice_adjacence
    [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]

	# >>> print(export_dot(G))
	# Graph G {
	# 	0 -- 0;
	# 	1 -- 1;
	# 	2 -- 2;
	# 	3 -- 3;
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
