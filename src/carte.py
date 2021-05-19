# coding: utf8
""" Ce module contient la classe Carte représentant la carte dans laquelle l'écosystème se trouve """

from random import random
from entites import *

class Carte:
        """ Classe permettant de représenter l'espace dans lequel
            l'écosystème se trouve
        """
        largeur_carte = largeur_carte
        hauteur_carte = hauteur_carte
        
        def __init__(self):
                """ Constructeur de la classe Carte
                """
                
                self.largeur = self.largeur_carte
                self.hauteur = self.hauteur_carte
                self.faune = {}
                self.flore = {}
                self.initialiser_flore()
                self.initialiser_faune()

        def initialiser_flore(self, quantite_min=0, quantite_max=30):
                """ Génère un objet Vegetation dans chaque case de
                    la grille de l'attribut flore
                """
                for x in range(self.largeur):
                        for y in range(self.hauteur):
                                quantite = (quantite_max - quantite_min) * random() + quantite_min
                                self.flore[x,y] = Vegetation(x, y, quantite)
        
        def initialiser_faune(self):
                """ Génère toutes les cases de la grille de l'attribut
                    faune destinées à contenir les entités
                """
                for x in range(self.largeur):
                        for y in range(self.hauteur):
                                self.faune[x,y] = None

        def quantite_totale_vegetation(self):
                """ Renvoie la quantité totale de végétation sur 
                    toute la carte 
                """
                quantite = 0
                for vegetation in self.flore.values():
                        quantite += vegetation.quantite
                return quantite

        def case_valide(self, x, y):
                """ Renvoie True si les coordonnées correspondent
                    à une case de la carte qui existe, et False sinon 
                """
                return (x,y) in self.faune

        def case_libre(self, x, y):
                """ Renvoie True si la case est vide (qu'il n'y pas 
                    d'animaux sur la case), renvoie False sinon 
                """
                if(self.faune[x,y] == None):
                        return True
                return False
