# coding: utf8

""" Ce module sert de moteur simulant les interactions entre les entités  """

from entites import *
from random import randint
from carte import *
from parametres_defaut import *
from time import time

class Simulateur:
        """ Classe Simulateur permettant de simuler les
            interractions entre les différentes entités
        """

        def generer(self, classe, n=1, age=0):
                """ Génère des des entités et les ajoute à la 
                    carte du Simulateur et à la liste des entités 
                """
                if(not classe in self.liste_entites):
                        self.liste_entites[classe] = []
                i = 0
                l = []
                while i < n:
                        x=randint(0,self.carte.largeur-1)
                        y=randint(0,self.carte.hauteur-1)
                        if(self.carte.case_libre(x,y)):
                                s=randint(0,1)
                                entite = classe(x,y,100,s,age)
                                self.liste_entites[classe].append(entite)
                                self.entite_nouvelles.append(entite)
                                self.carte.faune[x,y] = entite
                                l.append(entite)
                                i+=1
                return l # Retourne la liste des entités générées

        def vegetation(self):
                """ Ajoute à la liste des entités toutes la 
                    végétation générée initialement dans la carte 
                """
                self.liste_entites[Vegetation] = []
                for k in self.carte.flore.keys():
                        self.liste_entites[Vegetation].append(self.carte.flore[k])
        
        def __init__(self, ph=30, gh=0, pc=0, gc=0):
                """ Constructeur de la classe Simulateur
                    Prend en paramètres le nombre d'entités initial
                    pour chaque classe.
                """
                self.carte = Carte()
                self.liste_entites = {}
                self.entite_morte = []
                self.entite_nouvelles = []
                self.vegetation()
                self.generer(PetitHerbivore, ph)
                self.generer(GrandHerbivore, gh)
                self.generer(PetitCarnivore, pc)
                self.generer(GrandCarnivore, gc)
                self.temps = 0
                self.effectifs = {PetitHerbivore: [], GrandHerbivore: [], PetitCarnivore: [], GrandCarnivore: []}
                self.statistiques()

        def deplacement_entites(self):
                """ Déplace toutes les entités de l'écosystème
                """
                for k in self.liste_entites.keys():
                        if("deplacement" in dir(k)):
                                for j in range(len(self.liste_entites[k])):
                                        self.liste_entites[k][j].deplacement(self.carte, 5)

        def reproduction(self):
                """ Tente de reproduire toutes les entités
                    en appelant la méthode reproduction
                    de chaque entité (hors végétation)
                    Les nouvelles entités sont ajoutés à
                    la liste des entités
                """
                for k in self.liste_entites.keys():
                        if("reproduction" in dir(k)):
                                for j in range(len(self.liste_entites[k])):
                                        nouvelleEntite = self.liste_entites[k][j].reproduction(self.carte)
                                        if(nouvelleEntite):
                                                self.entite_nouvelles.append(nouvelleEntite)
                                                self.liste_entites[type(nouvelleEntite)].append(nouvelleEntite)

        def alimentation(self):
                """ Tente de nourrir toutes les espèces 
                    animales et fait croître la végétation
                    Les entités mangés sont retirés de la
                    liste des entités
                """
                for k in self.liste_entites.keys():
                        if("manger" in dir(k)):
                                for entite in self.liste_entites[k]:
                                        entiteMangee = entite.manger(self.carte)
                                        if(entiteMangee):
                                                if(not isinstance(entiteMangee, Vegetation)):
                                                        self.entite_morte.append(entiteMangee)
                                                        self.liste_entites[type(entiteMangee)].remove(entiteMangee)
                        if("croissance" in dir(k)):
                                for entite in self.liste_entites[k]:
                                        entite.croissance()

        def energie(self):
                """ Réduit l'énergie de toutes les entités
                    Les entités qui n'ont plus d'énergie
                    sont retirés de la liste des entités
                """
                for k in self.liste_entites.keys():
                        if("reduction_energie" in dir(k)):
                                for entite in self.liste_entites[k]:
                                        if(entite.reduction_energie(self.carte)):
                                                self.entite_morte.append(entite)
                                                self.liste_entites[k].remove(entite)

        def age(self):
                """ Augmente l'âge de toutes les entités 
                    Les entités qui meurent de vieillesse
                    sont retirés de la liste des entités
                """
                for k in self.liste_entites.keys():
                        if("vieillissement" in dir(k)):
                                for entite in self.liste_entites[k]:
                                        if(entite.vieillissement(self.carte)):
                                                self.entite_morte.append(entite)
                                                self.liste_entites[k].remove(entite)

        def iteration(self):
                """ Effectue toutes les interactions de
                    l'écosystème une fois. Fait avancer
                    la simulation d'une itération
                """
                self.entite_morte = []
                self.entite_nouvelles = []
                self.deplacement_entites()
                self.reproduction()
                self.alimentation()
                self.energie()
                self.age()
                self.temps += 1
                self.statistiques()

        def get_temps(self):
                """ Retourne l'âge de l'écosystème, le nombre d'itérations
                    effectués depuis le début de la simulation
                    Est utilisé pour l'affichage des statistiques
                    de l'interface graphique.
                """
                return self.temps

        def nombre_entites(self, classe):
                """ Retourne le nombre d'entités de la classe donnée
                """
                return len(self.liste_entites[classe])

        def statistiques(self):
                """ Ajoute à la liste de l'attribut statistiques le
                    nombre d'entités de chaque classe. Permet de voir
                    l'évolution du nombre d'entités de l'écosystème
                """
                for k in self.effectifs.keys():
                        self.effectifs[k].append(len(self.liste_entites[k]))
