#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from graphe import *
from math import inf
from os import listdir
from os.path import isfile, join
import argparse

######################################################################################################

def charger_donnees(graphe, fichier):
    ajoute_sommet = False
    ajouter_arete = False

    with open("./donnees/" + fichier, "r") as file:
        for ligne in file:
            if ("stations" in ligne):
                ajoute_sommet = True
                ajouter_arete = False
                continue

            elif ("connexions" in ligne):
                ajoute_sommet = False
                ajouter_arete = True
                continue
            
            if ajoute_sommet:
                ligne = ligne.split(':')
                graphe.ajouter_sommet(int(ligne[0]))
                graphe.ajouter_nom(int(ligne[0]), ligne[1].replace('\n', ''))

            elif ajouter_arete:
                ligne = ligne.split('/')
                graphe.ajouter_arete(int(ligne[0]), int(ligne[1]), fichier.replace(".txt", ''))

######################################################################################################

def numerotations(G):
    debut = dict()
    parent = dict()
    ancetre = dict()
    
    for s in G.sommets():
        debut[s] = 0
        parent[s] = None
        ancetre[s] = inf

    instant = 0

    def numerotation_recursive(s):
        nonlocal debut
        nonlocal parent
        nonlocal ancetre
        nonlocal instant

        instant += 1
        debut[s] = ancetre[s] = instant

        for t, _ in G.voisins(s):
            if debut[t]:
                if parent[s] != t:
                    ancetre[s] = min(ancetre[s], debut[t])
            
            else:
                parent[t] = s
                numerotation_recursive(t)
                ancetre[s] = min(ancetre[s], ancetre[t])
    
    if (G.nombre_sommets() > 0):
        # # La racine choisit sera toujours le 1er sommet de G.sommets(). Pour varier les résultats, on peut choisir de façon aléatoire la racine dans G.sommets() de cette façon :
        # import random
        # numerotation_recursive(random.choice(tuple(G.sommets())))
        numerotation_recursive(next(iter(G.sommets())))

    for v in G.sommets():
        if debut[v] == 0:
            numerotation_recursive(v)

    return debut, parent, ancetre

######################################################################################################

def points_articulation(G):
    debut, parent, ancetre = numerotations(G)
    articulations = set()
    racines = { r for r in parent if parent[r] == None}

    def degre_sortant(s, parent, G):
        return sum(1 for v, _ in G.voisins(s) if parent[v] == s)

    for depart in racines:
        if degre_sortant(depart, parent, G) >= 2:
            articulations.add(depart)

    for v in G.sommets():
        if (parent[v]) and (parent[v] not in racines) and (ancetre[v] >= debut[parent[v]]):
            articulations.add(parent[v])
    
    return articulations

######################################################################################################

def ponts(G):
    debut, parent, ancetre = numerotations(G)
    ponts = set()
    
    for v in G.sommets():
        if (parent[v]) and (ancetre[v] > debut[parent[v]]):
            ponts.add((v, parent[v]))
    
    return ponts

######################################################################################################

def amelioration_ponts(G):
    feuilles = []
    ponts_G = ponts(G)

    # Si on a qu'1 seul pont, on relie une des extremités du pont à un des descendants de l'autre extremité
    if len(ponts_G) == 1:
        pont = next(iter(ponts_G))
        for v, _ in G.voisins(pont[1]):
            if v != pont[0]:
                return [[v, pont[0]]]

        for v, _ in G.voisins(pont[0]):
            if v != pont[1]:
                return [[v, pont[1]]]
                        
        # Si on arrive ici, ça veut dire que le graphe n'avait que 2 sommets : on ne peut pas ajouter d'arete pour supprimer le pont
        return []

    def est_une_feuille(p0, p1, ponts, G):
        sommets = set()
        sommets.add(p0)
        
        while (True):
            nouveaux_sommets = set()
            
            # Pour chaque sommet dans 'sommets', on ajoute ses voisins dans 'nouveaux_sommets' s'il n'est pas déjà dans 'sommets' et qu'il est différent de p1 (= l'autre extremité du pont (p0, p1))
            for s in sommets:
                for v, _ in G.voisins(s):
                    if (v != p1) and (v not in sommets):
                        nouveaux_sommets.add(v)
                        
                        # Si ce nouveau sommet est une extremité d'un pont, p0 n'est pas une feuille
                        for pont in ponts:
                            if v in pont:
                                return False 
            
            # Si on n'a pas ajouté de nouveaux sommets, ça veut dire qu'on a ajouté tous les accessibles depuis p0 et aucun d'entre eux n'était une extremité de pont : p0 est une feuille
            if len(nouveaux_sommets) == 0:
                return True

            sommets = set.union(sommets, nouveaux_sommets)

    # Pour chaque pont, on regarde si ses extremités sont des feuilles, et on les ajouter à la liste "feuilles" si c'est le cas
    for p0, p1 in ponts_G:
        if est_une_feuille(p0, p1, ponts_G, G):
            feuilles.append(p0)
        
        if est_une_feuille(p1, p0, ponts_G, G):
            feuilles.append(p1)

    # Puis on relie chaque feuille à la feuille suivante dans la liste de "feuilles", et on renvoie cette nouvelle liste
    return [[feuilles[i], feuilles[i + 1]] for i in range(len(feuilles) - 1)]

######################################################################################################

def amelioration_points_articulation(G):
    aretes = []
    articulations = dict()
    articulations_triees = dict()
    debut, parent, ancetre = numerotations(G)
    racines = { r for r in parent if parent[r] == None}

    # Ajoute les points d'articulations et leur(s) descendant(s) qui provoque(nt) le point d'articulation dans le dictionnaire 'articulations' (clé = point d'articulation, valeur = le set du (des) descendant(s))
    for s in G.sommets():
        if (parent[s]) and (parent[s] not in racines) and (ancetre[s] >= debut[parent[s]]):
            if parent[s] not in articulations:
                articulations[parent[s]] = {s}
            else:
                articulations[parent[s]].add(s)
    
    # Puis on trie les points d'articulations dans le dictionnaire "articulations_triees" en ajoutant les plus profonds d'abord :
    # pour cela, on trie la liste "debut" dans l'ordre décroissant, et pour chaque sommet du graphe, on ajoute dans "articulations_triees" les sommets qui sont dans "articulations"
    for s, _ in sorted(debut.items(), reverse=True, key=lambda t: t[1]):
        if s in articulations:
            articulations_triees[s] = articulations[s]

    # Ajoute les racines (et leurs descendants) au dictionnaire 'articulations_triees' si les racines sont des points d'articulation
    for r in racines:
        descendants = { v for v in parent if parent[v] == r }
        if len(descendants) >= 2:
            articulations_triees[r] = descendants

    # On répare chaque point d'articulation et on les supprime dès qu'on les a réparé
    while (len(articulations_triees) > 0):
        u = next(iter(articulations_triees.keys()))

        # Si 'u' n'est pas la racine, ajoute le ou les arete [racine, descendant de u] (si plusieurs descendants) et on supprime 'u' de "articulations_triees"
        if u not in racines:
            for s in articulations_triees[u]:
                aretes.append([next(iter(racines)), s])
            articulations_triees.pop(u)

            # Puis on supprime tous les points d'articulations sur le chemin de 'u' à 'r' si et seulement si 
            # le(s) descendant(s) qui crée(nt) le point d'articulation est/sont sur ce chemin (= path)
            path = {u}
            while (parent[u] not in racines):
                u = parent[u]
                path.add(u)

                if u in articulations_triees:
                    if articulations_triees[u].issubset(path):
                        articulations_triees.pop(u)
                    else:
                        # Si on ne peut pas supprimer 'u', on regarde si on peut supprimer au moins 1 de ses descendants qui provoquent le point d'articulations (s'il a plusieurs descendants)
                        to_remove = set()
                        for s in articulations_triees[u]:
                            if s in path:
                                to_remove.add(s)
                                
                        for s in to_remove:
                            articulations_triees[u].remove(s)
        
        # Si 'u' est une racine, on parcourt ses descendants et on ajoute les aretes qui permettent de les lier entre elles
        else:
            descendants = list(articulations_triees[u])
            
            for i in range(len(descendants)):
                for j in range(i + 1, len(descendants)):
                    aretes.append([descendants[i], descendants[j]])            
            
            articulations_triees.pop(u)
        
    return aretes

######################################################################################################

def charger_ligne(G, type, lignes):
    # Si on veut charger toutes les lignes
    if lignes == []:
        print("Chargement de toutes les lignes de " + type.lower() + " ...", end = '')

        if type == "METRO":
            fichiers = [f for f in listdir("./donnees/") if isfile(join("./donnees/", f)) and f[0:5] == "METRO"]

        elif type == "RER":
            fichiers = [f for f in listdir("./donnees/") if isfile(join("./donnees/", f)) and f[0:3] == "RER"]

        for f in fichiers:
            charger_donnees(G, f)

        print(" terminé.")

    # Si on veut charger seulement quelques lignes
    elif lignes != None:
        lignes_non_valides = []

        print("Chargement des lignes " + str(lignes) + " de " + type.lower() + " ...", end = '')

        for ligne in reversed(lignes):
            station = type + "_" + ligne + ".txt"

            if isfile(join("./donnees", station)):
                charger_donnees(G, station)

            else:
                lignes.remove(ligne)
                lignes_non_valides.append(ligne)

        print(" terminé.")
        if len(lignes_non_valides) > 0:
            print("Les lignes " + str(lignes_non_valides) + " n'ont pas pu être trouvées.")

######################################################################################################

def afficher_lignes_stations(G):
    print("\nLe réseau contient les " + str(G.nombre_sommets()) + " stations suivantes:\n")
    for s in sorted(map(G.nom_sommet_et_num, G.sommets())):
        print(s)

######################################################################################################

def afficher_articulations(G):
    articulations_G = list(points_articulation(G))

    print("\nLe réseau contient les " + str(len(articulations_G)) + " points d'articulation suivants:")

    i = 1
    for s in sorted(articulations_G, key=lambda s: G.nom_sommet(s)):
        print("\t" + str(i) + " : " + G.nom_sommet(s))
        i += 1

######################################################################################################

def afficher_ponts(G):
    ponts_G = list(ponts(G))

    # On trie les noms de couple de chaque pont pour mettre en 1ère position le 1er pont 
    for i in range(len(ponts_G)):
        if G.nom_sommet(ponts_G[i][0]) > G.nom_sommet(ponts_G[i][1]):
            ponts_G[i] = ponts_G[i][1], ponts_G[i][0]

    print("\nLe réseau contient les " + str(len(ponts_G)) + " ponts suivants:")

    for pont in sorted(ponts_G, key=lambda pont: G.nom_sommet(pont[0])):
        print("\t - " + G.nom_sommet(pont[0]) + " -- " +  G.nom_sommet(pont[1]))
        
######################################################################################################

def afficher_ameliorer_articulations(G):
    # print("\nAVANT : Nombre de points d'articulations", len(points_articulation(G)))
    aretes = amelioration_points_articulation(G)
    
    # Pour chaque couple d'arete, on trie les noms pour mettre en 1ère position la 1ère station dans l'ordre alphabétique  
    for i in range(len(aretes)):
        if G.nom_sommet(aretes[i][0]) > G.nom_sommet(aretes[i][1]):
            aretes[i] = aretes[i][1], aretes[i][0]
    
    print("\nOn peut éliminer tous les points d'articulation du réseau en rajoutant les " + str(len(aretes)) + " arêtes suivantes:")
    for arete in sorted(aretes, key=lambda arete: G.nom_sommet(arete[0])):
        print("\t - " + G.nom_sommet(arete[0]) + " -- " +  G.nom_sommet(arete[1]))
        # G.ajouter_arete(arete[0], arete[1], None)
    
    # print("\nAPRES : Nombre de points d'articulations", len(points_articulation(G)))

######################################################################################################

def afficher_ameliorer_ponts(G):
    # print("\nAVANT : Nombre de ponts", len(ponts(G)))
    aretes = amelioration_ponts(G)

    # Pour chaque couple d'arete, on trie les noms pour mettre en 1ère position la 1ère station dans l'ordre alphabétique
    for i in range(len(aretes)):
        if G.nom_sommet(aretes[i][0]) > G.nom_sommet(aretes[i][1]):
            aretes[i] = aretes[i][1], aretes[i][0]
    
    print("\nOn peut éliminer tous les ponts du réseau en rajoutant les "+ str(len(aretes)) + " arêtes suivantes:")
    for arete in sorted(aretes, key=lambda arete: G.nom_sommet(arete[0])):
        print("\t - " + G.nom_sommet(arete[0]) + " -- " +  G.nom_sommet(arete[1]))
        # G.ajouter_arete(arete[0], arete[1], None)
        
    # print("\nAPRES : Nombre de ponts", len(ponts(G)))

######################################################################################################

def main():
    parser = argparse.ArgumentParser(description='Programme permettant de charger des stations de metro et rer sous forme de graphe, et d\'afficher les points d\'articulations et ponts de chaque graphe mais également quelles aretes ajouter dans le graphe pour les corriger.')

    parser.add_argument('--metro', 
                        nargs = '*',                  
                        help = "--metro [lignes] : précise les lignes de métro que l’on veut charger dans le réseau. Le paramètre lignes est facultatif : s’il existe, il s’agit des numéros de lignes qui nous intéressent (par exemple : --metro 3b 7 14) ; sinon, on charge toutes les lignes de métro disponibles dans le répertoire courant."
                        )

    parser.add_argument('--rer', 
                        nargs = '*',
                        help = "--rer [lignes] : cf. --metro, mais pour les lignes de RER."
                        )

    parser.add_argument('--liste-stations', 
                        action = 'store_true',
                        help = "--liste-stations : affiche la liste des stations du réseau avec leur identifiant triées par ordre alphabétique"
                        )

    parser.add_argument('--articulations', 
                        action = 'store_true',
                        help = "--articulations : affiche les points d’articulation du réseau qui a été chargé"
                        )

    parser.add_argument('--ponts', 
                        action = 'store_true',
                        help = "--ponts : affiche les ponts du réseau qui a été chargé"
                        )

    parser.add_argument('--ameliorer-articulations', 
                        action = 'store_true',
                        help = "--ameliorer-articulations : affiche les points d’articulation du réseau qui a été chargé, ainsi que les arêtes à rajouter pour que ces stations ne soient plus des points d’articulation"
                        )

    parser.add_argument('--ameliorer-ponts', 
                        action = 'store_true',
                        help = "--ameliorer-ponts : affiche les ponts du réseau qui a été chargé, ainsi que les arêtes à rajouter pour que ces arêtes ne soient plus des ponts"
                        )

    args = parser.parse_args()

    reseau = Graphe()
    charger_ligne(reseau, "METRO", args.metro)
    charger_ligne(reseau, "RER", args.rer)

    print("Le réseau contient " + str(reseau.nombre_sommets()) + " sommets" + " et " + str(reseau.nombre_aretes()) + " arêtes.")

    if (args.liste_stations):
        afficher_lignes_stations(reseau)

    if (args.ponts):
        afficher_ponts(reseau)

    if (args.articulations):
        afficher_articulations(reseau)

    if (args.ameliorer_articulations):
        afficher_ameliorer_articulations(reseau)

    if (args.ameliorer_ponts):
        afficher_ameliorer_ponts(reseau)

if __name__ == "__main__":
    main()