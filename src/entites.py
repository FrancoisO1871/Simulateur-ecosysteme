# coding: utf8
""" Ce module contient les classes représentant les différentes entités 
    de l'écosystème. Chaque entité sera un objet d'une de ces classes.
"""

from parametres_defaut import *
from random import randint
from random import random

class Entite:
        """ Classe Entite dont toutes les clasees des espèces animales hérite"""
        
        def __init__(self, x, y, energie, sexe, age=0):
                """ Constructeur de la classe entité """
                self.position = (x,y)
                self.age = age
                self.energie = energie
                self.sexe = sexe

        def reproduction(self, carte):
                """ Cette méthode essaye de faire reproduire l'entité,
                    renvoie la nouvelle entité née et l'ajoute à la carte
                    si la reproduction est possible, renvoie False sinon
                """
                if(not self.sexe == 0 or not self.age - self.derniere_reproduction > self.delai_reproduction):
                        return False
                xe,ye = self.position
                for x in range(xe - self.distance_reproduction, xe + self.distance_reproduction):
                        for y in range(ye - self.distance_reproduction, ye + self.distance_reproduction):
                                if(carte.case_valide(x,y)):
                                        entite = carte.faune[x,y]
                                        if(isinstance(entite, type(self))  and entite.sexe == 1 and entite.age - entite.derniere_reproduction > entite.delai_reproduction):
                                                for x in range(xe - self.distance_reproduction, xe + self.distance_reproduction):
                                                        for y in range(ye - self.distance_reproduction, ye + self.distance_reproduction):
                                                                if carte.case_valide(x,y):
                                                                        if(carte.case_libre(x,y)):
                                                                                if(random() > 0.5):
                                                                                        s = 1
                                                                                else:
                                                                                        s = 0
                                                                                self.derniere_reproduction = self.age
                                                                                entite.derniere_reproduction = entite.age
                                                                                classe = type(self)
                                                                                nouvelle_entite = classe(x, y, 100, s, 0)
                                                                                carte.faune[x,y] = nouvelle_entite
                                                                                return nouvelle_entite
                                                return False
                return False

        def _changer_case(self, carte, position):
                """ Déplace l'entite sur la carte et change ses attributs 
                    de position 
                """
                carte.faune[self.position] = None
                carte.faune[position] = self
                self.position = position

        def deplacement(self, carte, dist):
                dist = self.vision
                """ Permet à l'entité de se déplacer.
                    Evalue pour chaque direction l'intérêt de s'y diriger,
                    donnant plus de chance à l'entité de se déplacer
                    vers une case plus intéressante.
                """
                x,y = self.position

                valeur_haut = 0
                if(carte.case_valide(x,y+1)):
                        if(carte.case_libre(x,y+1)):
                                for i in range(1, dist+1):
                                        for j in range(-i+1, i-1):
                                                if(carte.case_valide(x+j,y+i)):
                                                        valeur_haut += self.evaluer_case(carte, (x+j,y+i))
                                valeur_haut = max(0, valeur_haut)
                valeur_bas = 0
                if(carte.case_valide(x,y-1)):
                        if(carte.case_libre(x,y-1)):
                                for i in range(1, dist+1):
                                        for j in range(-i+1, i-1):
                                                if(carte.case_valide(x+j,y-i)):
                                                        valeur_bas += self.evaluer_case(carte, (x+j,y-i))
                                valeur_bas = max(0, valeur_bas)
                valeur_droite = 0
                if(carte.case_valide(x+1,y)):
                        if(carte.case_libre(x+1,y)):
                                for i in range(1, dist+1):
                                        for j in range(-i+1, i-1):
                                                if(carte.case_valide(x+i,y+j)):
                                                        valeur_droite += self.evaluer_case(carte, (x+i,y+j))
                                valeur_droite = max(0, valeur_droite)
                valeur_gauche = 0
                if(carte.case_valide(x-1,y)):
                        if(carte.case_libre(x-1,y)):
                                for i in range(1, dist+1):
                                        for j in range(-i+1, i-1):
                                                if(carte.case_valide(x-i,y+j)):
                                                        valeur_gauche += self.evaluer_case(carte, (x-i,y+j))
                                valeur_gauche = max(0, valeur_gauche)

                s=valeur_haut+valeur_bas+valeur_droite+valeur_gauche
                if(s == 0):
                        return

                r = random()
                if(r<valeur_haut/s):
                        self._changer_case(carte, (x,y+1))
                elif(r<(valeur_haut+valeur_bas)/s):
                        self._changer_case(carte, (x,y-1))
                elif(r<(valeur_haut+valeur_bas+valeur_gauche)/s):
                        self._changer_case(carte, (x-1,y))
                else:
                        self._changer_case(carte, (x+1,y))
                        

        def manger(self, carte, dist=1):
                """ Tente de nourrir l'entité. Renvoie l'entité mangée,
                    s'il y a en une et la supprime de la carte si elle est
                    un animal. Renvoie None si aucune entité est mangée.
                """
                
                xe,ye = self.position
                if(chaine_alimentaire[type(self)][Vegetation]):
                        entite = carte.flore[xe,ye]
                        if(100 - self.energie < entite.quantite):
                                entite.quantite -= 100 - self.energie
                                self.energie = 100
                        else:
                                self.energie += entite.quantite
                                entite.quantite = 0
                        return entite
                else:
                        for x in range(xe - dist, xe + dist):
                                for y in range(ye - dist, ye + dist):
                                        if(carte.case_valide(x, y)):
                                                entite = carte.faune[x,y]
                                                if(entite):
                                                        if(chaine_alimentaire[type(self)][type(entite)]):
                                                                self.energie = 100
                                                                carte.faune[x,y] = None
                                                                return entite
                return None

        def reduction_energie(self, carte):
                """ Baisse le niveau d'énergie de l'entité.
                    Renvoie True si l'entité n'a plus d'énergie
                    et la supprime de la carte, renvoie False sinon
                """
                self.energie -= self.perte_energie
                if(self.energie <= 0):
                        carte.faune[self.position] = None
                        return True
                return False

        def vieillissement(self, carte):
                """ Augmente l'âge de l'entité.
                    Si l'âge de l'entité atteint son attribut espérance 
                    de vie, l'entite est supprimé de la carte et renvoie
                    True. Renvoie False sinon.
                """
                self.age += 1
                if(self.age >= self.esperance_vie):
                        carte.faune[self.position] = None
                        return True
                return False

        def evaluer_case(self, carte, pos):
                """ Donne une note à la case en fonction de l'intérêt 
                    qu'elle représente pour l'entité 
                """
                valeur_case = 10
                entite = carte.faune[pos]
                if(chaine_alimentaire[type(self)][Vegetation]):
                        valeur_case += 100 * carte.flore[pos].quantite / self.energie**2
                if(not entite):
                        return valeur_case
                if(chaine_alimentaire[type(self)][type(entite)]):
                        valeur_case += 100 / self.energie**2
                elif(chaine_alimentaire[type(entite)][type(self)]):
                        valeur_case -= 50
                elif(isinstance(entite, type(self))):
                        if(self.age - self.derniere_reproduction > self.delai_reproduction and self.sexe != entite.sexe):
                                valeur_case += 200
                        else:
                                valeur_case += 5
                return valeur_case


class GrandCarnivore(Entite):
        """ Classe représentant les grands carnivores. Hérite de la classe Entite """
        
        vision = 10
        esperance_vie = grand_carnivore_esperance_vie
        delai_reproduction = grand_carnivore_delai_reproduction
        age_reproduction = grand_carnivore_age_min_reproduction
        perte_energie = grand_carnivore_perte_energie
        distance_reproduction = distance_reproduction
        couleur = "red3"
        
        def __init__(self, x, y, energie, sexe, age=0):
                """ Constructeur de la classe GrandCarnivore """
                Entite.__init__(self, x, y, energie, sexe,age)
                self.derniere_reproduction = self.age_reproduction - self.delai_reproduction

        def __repr__(self):
                return "Grand carnivore: " + str(self.position) + ", energie: " + str(int(self.energie))
                
class PetitCarnivore(Entite):
        """ Classe représentant les petits carnivores. Hérite de la classe Entite """

        vision = 10
        esperance_vie = petit_carnivore_esperance_vie
        delai_reproduction = petit_carnivore_delai_reproduction
        age_reproduction = petit_carnivore_age_min_reproduction
        perte_energie = petit_carnivore_perte_energie
        distance_reproduction = distance_reproduction
        couleur="orange"
        
        def __init__(self, x, y, energie, sexe, age=0):
                """ Constructeur de la classe PetitCarnivore """
                
                Entite.__init__(self, x, y, energie, sexe, age)
                self.derniere_reproduction = self.age_reproduction - self.delai_reproduction

        def __repr__(self):
                return "Petit Carnivore: " + str(self.position)




class GrandHerbivore(Entite):
        """ Classe représentant les grands herbivores. Hérite de la classe Entite """

        vision = 3
        esperance_vie = grand_herbivore_esperance_vie
        delai_reproduction = grand_herbivore_delai_reproduction
        age_reproduction = grand_herbivore_age_min_reproduction
        perte_energie = grand_herbivore_perte_energie
        distance_reproduction = distance_reproduction
        couleur = "blue"
        
        def __init__(self, x, y, energie, sexe, age=0):
                """ Constructeur de la classe GrandHerbivore """
                
                Entite.__init__(self, x, y, energie, sexe, age)
                self.derniere_reproduction = self.age_reproduction - self.delai_reproduction



class PetitHerbivore(Entite):
        """ Classe représentant les petits herbivores. Hérite de la classe Entite """
        vision = 3
        esperance_vie = petit_herbivore_esperance_vie
        delai_reproduction = petit_herbivore_delai_reproduction
        age_reproduction = petit_herbivore_age_min_reproduction
        perte_energie = petit_herbivore_perte_energie
        distance_reproduction = distance_reproduction
        couleur = "cyan"
        
        def __init__(self, x, y, energie, sexe, age=0):
                """ Constructeur de la classe PetitHerbivore """
                
                Entite.__init__(self, x, y, energie, sexe, age)
                self.derniere_reproduction = self.age_reproduction - self.delai_reproduction

        def __repr__(self):
                return "Petit Herbivore : " + str(self.position) + ", energie: " + str(int(self.energie))



class Vegetation():
        """ Classe représentant la végétation. N'hérite pas de la classe Entite"""

        quantite_max = vegetation_quantite_max
        croissance_min = vegetation_croissance_min
        croissance_max = vegetation_croissance_max
        croissance_fixe = vegetation_croissance_fixe
        """ La croissance de la végétation et soit fixe
            (ajoute l'attribut croissance_fixe à la quantité
            à chaque itération) ou aléatoire: (ajoute une quantité
            aléatoire entre croissance_min et croissance_max à
            chaque itération
        """
        croissance_type_alea = vegetation_croissance_type_alea
        
        def __init__(self, x, y, quantite=0):
                """ Constructeur de la classe Végétation"""
                self.position = x,y
                self.quantite = quantite

        def __repr__(self):
                return "Vegetation : (" + str(self.position) + ") " + str(self.quantite) + "%"

        def croissance(self):
                """ Cette méthode augmente la quantité de la végétation """
                if(self.croissance_type_alea):
                        self.quantite = min(self.quantite + (self.croissance_max - self.croissance_min) * random() + self.croissance_min, self.quantite_max)
                else:
                        self.quantite = min(self.quantite + self.croissance_fixe, self.quantite_max)


""" Représentation sous forme d'un dictionnaire de
    la chaîne alimentaire
"""
chaine_alimentaire = {GrandCarnivore: {GrandCarnivore: False, PetitCarnivore: True,GrandHerbivore: True, PetitHerbivore: True, Vegetation: False},
PetitCarnivore: {GrandCarnivore: False, PetitCarnivore: False,GrandHerbivore: True, PetitHerbivore: True, Vegetation: False},
GrandHerbivore: {GrandCarnivore: False, PetitCarnivore: False,GrandHerbivore: False, PetitHerbivore: False, Vegetation: True},
PetitHerbivore: {GrandCarnivore: False, PetitCarnivore: False,GrandHerbivore: False, PetitHerbivore: False, Vegetation: True},
Vegetation: {GrandCarnivore: False, PetitCarnivore: False,GrandHerbivore: False, PetitHerbivore: False, Vegetation: False}}
