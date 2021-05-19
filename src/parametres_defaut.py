# coding: utf8
""" Ce module comporte les principaux paramètres par défaut
de la simulation. Ce module est utilisé par les modules
carte et entites"""

import random
from time import time

"""
Paramètres concernant la classe Carte
"""

largeur_carte = 75
hauteur_carte = 75

"""
Paramètres concernant les différentes entités
"""

#Végétation
vegetation_croissance_type_alea = True 
vegetation_croissance_min = 0.1
vegetation_croissance_max = 0.3
vegetation_croissance_fixe = 0.2
vegetation_quantite_max = 100

distance_reproduction = 1

#Petits herbivores
petit_herbivore_delai_reproduction = 20
petit_herbivore_age_min_reproduction = 30
petit_herbivore_esperance_vie = 500
petit_herbivore_perte_energie = 5

#Grands herbivores
grand_herbivore_delai_reproduction = 100
grand_herbivore_age_min_reproduction = 200
grand_herbivore_esperance_vie = 1000
grand_herbivore_perte_energie = 0.5

#Petits carnivores
petit_carnivore_delai_reproduction = 100
petit_carnivore_age_min_reproduction = 200
petit_carnivore_esperance_vie = 1000
petit_carnivore_perte_energie = 0.5

#Grands carnivores
grand_carnivore_delai_reproduction = 100
grand_carnivore_age_min_reproduction = 200
grand_carnivore_esperance_vie = 1000
grand_carnivore_perte_energie = 0.5


""" Dictionnaire comportant les différents paramètres.
"""
PARAMETRES_DEFAUT = {
        "general": {
                "nombre_petit_herbivore": 100,
                "nombre_grand_herbivore": 50,
                "nombre_petit_carnivore": 30,
                "nombre_grand_carnivore": 20
                },
        "carte": {
                "largeur_carte": largeur_carte,
                "hauteur_carte": hauteur_carte
                },
        "petit_herbivore": {
                "delai_reproduction": petit_herbivore_delai_reproduction,
                "age_reproduction": petit_herbivore_age_min_reproduction,
                "esperance_vie": petit_herbivore_esperance_vie,
                "perte_energie": petit_herbivore_perte_energie
                },
        "grand_herbivore": {
                "delai_reproduction": grand_herbivore_delai_reproduction,
                "age_reproduction": grand_herbivore_age_min_reproduction,
                "esperance_vie": grand_herbivore_esperance_vie,
                "perte_energie": grand_herbivore_perte_energie
                },
        "petit_carnivore": {
                "delai_reproduction": petit_carnivore_delai_reproduction,
                "age_reproduction": petit_carnivore_age_min_reproduction,
                "esperance_vie": petit_carnivore_esperance_vie,
                "perte_energie": petit_carnivore_perte_energie
                },
        "grand_carnivore": {
                "delai_reproduction": grand_carnivore_delai_reproduction,
                "age_reproduction": grand_carnivore_age_min_reproduction,
                "esperance_vie": grand_carnivore_esperance_vie,
                "perte_energie": grand_carnivore_perte_energie
                },
        "vegetation": {
                "quantite_max": vegetation_quantite_max,
                "croissance_min": vegetation_croissance_min,
                "croissance_max": vegetation_croissance_max,
                "croissance_fixe": vegetation_croissance_fixe,
                "type_croissance": "Aléatoire"
                }
        }

