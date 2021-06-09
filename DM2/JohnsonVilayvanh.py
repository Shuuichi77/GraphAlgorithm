#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class Graphe(object):
    def __init__(self):
        """
        Initialise un graphe sans arêtes
        """
        self.dictionnaire = dict()

    def ajouter_arete(self, u, v, poids):
        """Ajoute une arête entre les sommmets u et v, en créant les sommets
        manquants le cas échéant."""
        # vérification de l'existence de u et v, et création(s) sinon
        if u not in self.dictionnaire:
            self.dictionnaire[u] = set()
        if v not in self.dictionnaire:
            self.dictionnaire[v] = set()
        # ajout de u (resp. v) parmi les voisins de v (resp. u)
        self.dictionnaire[u].add((v, poids))
        self.dictionnaire[v].add((u, poids))

    def ajouter_aretes(self, iterable):
        """Ajoute toutes les arêtes de l'itérable donné au graphe. N'importe
        quel type d'itérable est acceptable, mais il faut qu'il ne contienne
        que des couples d'éléments (quel que soit le type du couple)."""
        for u, v, poids in iterable:
            self.ajouter_arete(u, v, poids)

    def ajouter_sommet(self, sommet):
        """Ajoute un sommet (de n'importe quel type hashable) au graphe."""
        self.dictionnaire[sommet] = set()

    def ajouter_sommets(self, iterable):
        """Ajoute tous les sommets de l'itérable donné au graphe. N'importe
        quel type d'itérable est acceptable, mais il faut qu'il ne contienne
        que des éléments hashables."""
        for sommet in iterable:
            self.ajouter_sommet(sommet)

    def aretes(self):
        """Renvoie l'ensemble des arêtes du graphe. Une arête est représentée
        par un tuple (a, b) avec a <= b afin de permettre le renvoi de boucles.
        """
        return {
            tuple((u, v, poids)) 
            for u in self.dictionnaire
                for (v, poids) in self.dictionnaire[u]
                    if u <= v
        }

    def boucles(self):
        """Renvoie les boucles du graphe, c'est-à-dire les arêtes reliant un
        sommet à lui-même."""
        return {(u, u) for u in self.dictionnaire if u in self.dictionnaire[u]}

    def contient_arete(self, u, v):
        """Renvoie True si l'arête {u, v} existe, False sinon."""
        if self.contient_sommet(u) and self.contient_sommet(v):
            return u in self.dictionnaire[v]  # ou v in self.dictionnaire[u]
        return False

    def contient_sommet(self, u):
        """Renvoie True si le sommet u existe, False sinon."""
        return u in self.dictionnaire

    def degre(self, sommet):
        """Renvoie le nombre de voisins du sommet; s'il n'existe pas, provoque
        une erreur."""
        return len(self.dictionnaire[sommet])

    def nombre_aretes(self):
        """Renvoie le nombre d'arêtes du graphe."""
        return len(self.aretes())

    def nombre_boucles(self):
        """Renvoie le nombre d'arêtes de la forme {u, u}."""
        return len(self.boucles())

    def nombre_sommets(self):
        """Renvoie le nombre de sommets du graphe."""
        return len(self.dictionnaire)

    def retirer_arete(self, u, v):
        """Retire l'arête {u, v} si elle existe; provoque une erreur sinon."""
        self.dictionnaire[u].remove(v)  # plante si u ou v n'existe pas
        self.dictionnaire[v].remove(u)  # plante si u ou v n'existe pas

    def retirer_aretes(self, iterable):
        """Retire toutes les arêtes de l'itérable donné du graphe. N'importe
        quel type d'itérable est acceptable, mais il faut qu'il ne contienne
        que des couples d'éléments (quel que soit le type du couple)."""
        for u, v in iterable:
            self.retirer_arete(u, v)

    def retirer_sommet(self, sommet):
        """Efface le sommet du graphe, et retire toutes les arêtes qui lui
        sont incidentes."""
        del self.dictionnaire[sommet]
        # retirer le sommet des ensembles de voisins
        for u in self.dictionnaire:
            self.dictionnaire[u].discard(sommet)

    def retirer_sommets(self, iterable):
        """Efface les sommets de l'itérable donné du graphe, et retire toutes
        les arêtes incidentes à ces sommets."""
        for sommet in iterable:
            self.retirer_sommet(sommet)

    def sommets(self):
        """Renvoie l'ensemble des sommets du graphe."""
        return set(self.dictionnaire.keys())

    def sous_graphe_induit(self, iterable):
        """Renvoie le sous-graphe induit par l'itérable de sommets donné."""
        G = Graphe()
        G.ajouter_sommets(iterable)
        for u, v in self.aretes():
            if G.contient_sommet(u) and G.contient_sommet(v):
                G.ajouter_arete(u, v)
        return G

    def voisins(self, sommet):
        """Renvoie l'ensemble des voisins du sommet donné."""
        return self.dictionnaire[sommet]

    def poids_arete(self, u, v):
        if u in self.dictionnaire:
            for x, poids in self.dictionnaire[u]:
                if x == v:
                    return poids
        return 0

##################################################################################################

class Tas(object):
    """Implémentation de la structure de données Tas."""
    def __init__(self):
        """Initialisation des structures de données nécessaires."""
        self.table = []
        self.size = 0

    def inserer(self, element):
        """Insère un élément dans le tas en préservant la structure."""
        index = self.size
        self.table.append(element)
        self.size += 1

        while index > 0:
            father_index = (index - 1) // 2
            father = self.table[father_index]

            if father <= element:
                break

            else:
                self.table[index] = father
                self.table[father_index] = element
                index = father_index

    def min_child(self, index):
        """Renvoie l'indice du plus petit fils"""
        # Si le noeud actuel n'a pas de fils droit, on renvoie l'indice du fils gauche
        if (index * 2 + 2) >= self.size:
            return index * 2 + 1

        # Sinon on renvoie le plus petit fils
        else:  
            if self.table[index * 2 + 1] < self.table[index * 2 + 2]:
                return index * 2 + 1
            else:
                return index * 2 + 2

    def extraire_minimum(self):
        """Extrait et renvoie le minimum du tas en préservant sa structure."""
        root = self.table[0]
        
        self.table[0] = self.table[self.size - 1]
        self.table.pop()
        self.size -= 1

        index = 0
        # Tant que le noeud actuel a un fils
        while((index * 2 + 1) < self.size):
            # On recupère l'indice du fils le plus petit
            min_child = self.min_child(index)

            # Si le noeud actuel est plus grand que ce fils, on les échange
            if self.table[index] > self.table[min_child]:
                self.table[index], self.table[min_child] = self.table[min_child], self.table[index]
            
            index = min_child

        return root

    def pas_vide(self):
        return self.size != 0

##################################################################################################

class UnionFind(object):
    """Implémentation de la structure de données Union-Find."""
    def __init__(self, ensemble):
        """Initialisation des structures de données nécessaires."""
        self.parents = dict()
        self.ranks = dict()

        for s in ensemble:
            self.parents[s] = s
            self.ranks[s] = 0

    def find(self, element):
        """Renvoie le numéro de la classe à laquelle appartient l'élément."""
        if (element != self.parents[element]):
            self.parents[element] = self.find(self.parents[element])
        
        return self.parents[element]

    def union(self, premier, second):
        """Fusionne les classes contenant les deux éléments donnés."""
        i = self.find(premier)
        j = self.find(second)
        
        if i != j:
            if self.ranks[i] > self.ranks[j]:
                self.parents[j] = i
            elif self.ranks[j] < self.ranks[i]:
                self.parents[i] = j
            else:
                self.parents[i] = j
                self.ranks[j] += 1

##################################################################################################

def acpm_kruskal(G):
    foret = type(G)()
    classes = UnionFind(list(G.sommets())) 

    for u, v, p in sorted(G.aretes(), key=lambda tuple:tuple[2]):
        if classes.find(u) != classes.find(v):
            foret.ajouter_arete(u, v, p)
            classes.union(classes.find(u), classes.find(v))
    
    return foret

##################################################################################################

def stocker_aretes_valides(G, u, S, hors_arbre):
    for v, _ in G.voisins(u):
        if hors_arbre[v]:
            S.inserer((G.poids_arete(u, v), u, v))

def extraire_arete_sure(S, hors_arbre):
    while S.pas_vide():
        p, u, v = S.extraire_minimum()

        if hors_arbre[u] != hors_arbre[v]:
            return u, v, p

    return None, None, float('inf')

################################

def acpm_prim(G, depart):
    arbre = type(G)()
    arbre.ajouter_sommet(depart)
    
    hors_arbre = dict()
    for s in G.sommets():
        hors_arbre[s] = True
    hors_arbre[depart] = False

    candidates = Tas()
    stocker_aretes_valides(G, depart, candidates, hors_arbre)

    while True:
        u, v, p = extraire_arete_sure(candidates, hors_arbre)

        if u == None:
            return arbre
        
        if not hors_arbre[u]:
            u, v = v, u
        
        arbre.ajouter_arete(u, v, p)
        hors_arbre[u] = False
        stocker_aretes_valides(G, u, candidates, hors_arbre)

    return arbre

################################

def fcpm_prim(G):
    depart = list(G.sommets())[0]
    arbre = type(G)()
    arbre.ajouter_sommet(depart)
    
    hors_arbre = dict()
    for s in G.sommets():
        hors_arbre[s] = True
    hors_arbre[depart] = False

    candidates = Tas()
    stocker_aretes_valides(G, depart, candidates, hors_arbre)
    nouvelle_boucle = False # Pour savoir si on doit relancer le while depuis le début (lorsqu'on relance la boucle sur un nouveau sommet)
    
    while True:
        u, v, p = extraire_arete_sure(candidates, hors_arbre)

        if u == None:
            all_false = True
            
            # On regarde si on a encore des sommets "True" dans hors_arbre.
            # Si c'est le cas, on recommence la boucle while avec ce nouveau sommet
            for s in hors_arbre:
                if hors_arbre[s]:
                    arbre.ajouter_sommet(s)
                    hors_arbre[s] = False
                    stocker_aretes_valides(G, s, candidates, hors_arbre)
                    
                    all_false = False
                    nouvelle_boucle = True
                    break
            
            # Si on est rentré dans le if du for, all_false = false car on doit relancer le while sur un nouveau sommet
            if all_false:
                return arbre
        
        # Si c'est une nouvelle boucle, on recommence le while depuis le début
        if nouvelle_boucle:
            nouvelle_boucle = False
            continue
        
        if not hors_arbre[u]:
            u, v = v, u
        
        arbre.ajouter_arete(u, v, p)
        hors_arbre[u] = False
        stocker_aretes_valides(G, u, candidates, hors_arbre)

    return arbre

##################################################################################################
