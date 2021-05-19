# coding: utf8
""" Ce module sert à l'affichage du menu de l'interface graphique
"""

import tkinter as tk
from tkinter import ttk
import pygame
from parametres_defaut import *
import pygame.locals
from main import *
from random import randint

GRIS1 = (217, 217, 217)
GRIS2 = (236, 236, 236)
GRIS3 = (130, 130, 130)
GRIS4=(100, 100, 100)
BLANC = (255, 255, 255)
NOIR = (0, 0, 0)
COULEUR_MENU = GRIS1
CLASSES_ENTITES = [PetitHerbivore, GrandHerbivore, PetitCarnivore, GrandCarnivore, Vegetation]

if not pygame.font.get_init():
        pygame.font.init()

POLICE_DEFAUT = pygame.font.SysFont("Times", 16)
POLICE2 = pygame.font.SysFont("Times", 12)

class Menu():
        """ Classe permettant d'afficher le menu de l'interface graphique
                Seule cette classe est utilisée directement dans le main.
                Les autres classes du modules sont utilisés à partir de
                cette classe là.
        """
        marges = 10
        espaces = 10
        
        def __init__(self, largeur, hauteur, simulateur):
                """ Constructeur de la classe Menu
                        Prend en paramètres la largeur et la hauteur que doit
                        faire le menu ainsi que le simulateur de l'écosystème.
                        Construit la surface qui servira d'image de fond
                        pour le menu, et crée les sprites à afficher dans le
                        menu.
                """
                
                """ Création des attributs du menu """
                self.largeur = largeur
                self.centre = int(self.largeur / 2) # Correspond au centre horizontalement
                self.hauteur = hauteur
                self.simulateur = simulateur
                self.fond = pygame.Surface((self.largeur, self.hauteur))
                self.fond.fill(COULEUR_MENU)
                self.rect = self.fond.get_rect()
                pygame.draw.line(self.fond, GRIS4, (largeur - 1, 0), (largeur - 1, hauteur))
                pygame.draw.line(self.fond, GRIS3, (largeur - 2, 0), (largeur - 2, hauteur))
                self.pause = True
                self.classes_affichees = {}
                for i in range(len(CLASSES_ENTITES)):
                        self.classes_affichees[CLASSES_ENTITES[i]] = True

                """ Création des statistiques """
                self.set_liste_stats()
                stats = StatsMenu(self.largeur - 20, self.liste_stats, marge_haut = 5, pos=(self.marges, self.marges))
                stats.draw(self.fond)
                
                """ Création de la légende """
                legende = Legende(self.largeur - 20, espace = 10, marge_haut = 5)
                legende.rect.bottomleft = self.marges, self.hauteur - self.marges
                legende.draw(self.fond)

                self.fond = self.fond.convert()

                """ Initialisation des sprites servant aux statistiques """

                self.stats = pygame.sprite.Group()
                self.stats.add(stats.get_sprites())


                self.interactions = Interactions(self.largeur - 20, simulateur, espace = 10, marge_haut = 5)

                """ Initialisation des boutons du menu """
                
                self.sprites = pygame.sprite.Group()
                self.boutons_affichage = legende.get_sprites()
                [self.sprites.add(self.boutons_affichage[key][1]) for key in self.boutons_affichage.keys()]

                self.bouton_lancer = Bouton("Lancer la simulation", event = pygame.event.Event(PAUSE))
                self.bouton_lancer.rect.centerx, self.bouton_lancer.rect.top = self.centre, stats.rect.bottom + self.espaces
                self.bouton_pause = Bouton("Mettre en pause", event = pygame.event.Event(PAUSE))
                self.bouton_pause.rect.center = self.bouton_lancer.rect.center
                
                bouton_reinit = Bouton("Réinitialiser la simulation", event = pygame.event.Event(REINITIALISER))
                bouton_reinit.rect.centerx, bouton_reinit.rect.top = self.centre, self.bouton_lancer.rect.bottom + self.espaces
                bouton_parametre = Bouton("Modifier les paramètres", event = pygame.event.Event(PARAMETRES))
                bouton_parametre.rect.centerx, bouton_parametre.rect.top = self.centre, bouton_reinit.rect.bottom + self.espaces
                self.sprites.add(bouton_parametre, bouton_reinit, self.bouton_lancer)

                self.interactions.rect.topleft = self.marges, bouton_parametre.rect.bottom + self.espaces
                self.sprites.add(self.interactions.sprites)
                """ Une fois les sprites initialisés et l'image de fond du
                        menu créée, le rectangle correspondant à la position
                        où est affiché le menu est créé, et on affiche les
                        sprites sur le l'image du menu.
                """
                self.update()

        def draw(self, surface):
                """ Affiche le menu sur la surface donnée
                """
                surface.blit(self.image, self.rect)

        def set_liste_stats(self):
                """ Initialise la liste des statistiques qui seront affichés.
                        La liste contient le texte qui sera affiché sur le menu,
                        la fonction qui renvoie la donnée de la stat ainsi que
                        les éventuels arguments de la fonction.
                        Permet d'apporter des modifications aux statistiques à
                        afficher en ne modifiant que cette liste.
                """
                self.liste_stats = [["Nombre d'itérations:", self.simulateur.get_temps],
                                ["Petits herbivores:", self.simulateur.nombre_entites, PetitHerbivore],
                                ["Grands herbivores:", self.simulateur.nombre_entites, GrandHerbivore],
                                ["Petits carnivores:", self.simulateur.nombre_entites, PetitCarnivore],
                                ["Grands carnivores:", self.simulateur.nombre_entites, GrandCarnivore]]

        def position_relative(self, x, y):
                """ Renvoie la position relative au menu
                        La position de la souris correspond à la position
                        dans la fenêtre pygame et non dans le menu. Les positions
                        des boutons étant relatif à la position du menu, cette
                        méthode permet de gérer correctement ces boutons en
                        transformant une position absolue dans la fenêtre en une
                        position relative au menu.
                """
                a,b = self.rect.topleft
                return (x-a, y-b)

        def events(self, event):
                """ Méthode permettant de gérer les events pygame liés à la
                        souris concernant le menu
                """
                x,y=event.pos
                position = self.position_relative(x,y)
                if event.type == pygame.MOUSEBUTTONDOWN:
                        for bouton in self.sprites:
                                bouton.event_clic_down(position)
                                
                if event.type == pygame.MOUSEBUTTONUP:
                        for bouton in self.sprites:
                                bouton.event_clic_up(position)

                if event.type == pygame.MOUSEMOTION:
                        for bouton in self.sprites:
                                bouton.event_survol(position)

        def update(self):
                """ Met à jour l'affichage du menu
                        Met à jour les sprites des boutons, ainsi que les sprites
                        des statistiques si la simulateur n'est pas en pause,
                        puis affiche tous les sprites sur l'image de fond du menu.
                """
                if not self.pause:
                        self.stats.update()
                self.image = self.fond.copy()
                self.interactions.draw(self.image)
                self.stats.draw(self.image)
                self.sprites.update()
                self.sprites.draw(self.image)

        def event_pause(self):
                """ Méthode à appeler lorsque le bouton pour mettre
                        en pause/reprendre la simulation est activé.
                """
                if self.pause:
                        self.pause = False
                        self.sprites.remove(self.bouton_lancer)
                        self.sprites.add(self.bouton_pause)
                else:
                        self.pause = True
                        self.sprites.remove(self.bouton_pause)
                        self.sprites.add(self.bouton_lancer)

        def event_reinit(self, simulateur):
                """ Méthode à appeler lors de la réinitialisation de
                        la simulation
                """
                for sprite in self.stats:
                        if sprite.fonction == self.simulateur.get_temps:
                                sprite.fonction = simulateur.get_temps
                        else:
                                sprite.fonction = simulateur.nombre_entites
                self.simulateur = simulateur
                self.interactions.simulateur = simulateur
                self.stats.update()

        def event_affichage(self, classe):
                """ Méthode à appeler lors de l'activation des boutons
                        gérant l'affichage de la simulation
                """
                if self.classes_affichees[classe]:
                        self.classes_affichees[classe] = False
                        self.sprites.remove(self.boutons_affichage[classe][1])
                        self.sprites.add(self.boutons_affichage[classe][0])
                else:
                        self.classes_affichees[classe] = True
                        self.sprites.remove(self.boutons_affichage[classe][0])
                        self.sprites.add(self.boutons_affichage[classe][1])


""" Toutes les classes qui suivent ne servent uniquement au fonctionnement
du menu, et ne sont utilisées qu'à l'intérieur de celui-ci.
"""


class SpriteStat(pygame.sprite.Sprite):
        """ Classe correspondant à un sprite pour l'affichage d'une statistique
        A chaque actualisation, le sprite détermine la nouvelle valeur à afficher
        en appelant la fonction qui lui est attribué """

        police = POLICE_DEFAUT

        def __init__(self, fonction, *args):
                """ Constructeur de la classe
                Prend comme paramètres la fonction à
                appeler lors de l'actualisation du
                sprite, ainsi que ses éventuels
                paramètres """

                pygame.sprite.Sprite.__init__(self)
                self.fonction = fonction
                self.args = args
                self.valeur = self.fonction(*self.args)
                self.image = self.police.render(str(self.valeur), True, NOIR)
                self.rect = self.image.get_rect()

        def update(self):
                """ Met à jour la valeur que le sprite affiche
                        en appelant la fonction qui lui est attribuée.
                        Déplace le rectangle de tel sorte que sa position à
                        droite soit la même.
                """
                self.x, self.y = self.rect.topright
                self.valeur = self.fonction(*self.args)
                self.image = self.police.render(str(self.valeur), True, NOIR)
                self.rect = self.image.get_rect()
                self.rect = self.rect.move(self.x - self.rect.width, self.y)

class Bouton(pygame.sprite.Sprite):
        """ Classe permettant de créer un sprite pygame correspondant
                à un bouton cliquable. Le bouton envoie un event
                pygame à chaque que l'on clique dessus.
                L'apparence et le fonctionnement est inspiré des boutons
                de Tkinter.
        """

        def __init__(self, texte, font = POLICE_DEFAUT, event = None, margeh = 10, margev = 5):
                """ Constructeur de la classe Bouton """
                pygame.sprite.Sprite.__init__(self)
                l,h = font.size(texte)
                l += margeh * 2
                h += margev * 2
                """ On crée trois surfaces pygame, une correspondant
                    à l'image qui sera affichée lorsque le bouton
                    sera survolé, une autre lorsqu'il sera enfoncé, et
                    enfin une dernière pour le reste du temps
                """
                self.image_normal = pygame.Surface((l, h))
                self.image_clic = pygame.Surface((l, h))
                self.rect = self.image_normal.get_rect()
                
                pygame.draw.rect(self.image_clic, GRIS3, self.rect, 1)
                pygame.draw.rect(self.image_clic, BLANC, (1,1,l-1,h-1))
                pygame.draw.rect(self.image_normal, BLANC, self.rect, 1)
                pygame.draw.rect(self.image_normal, GRIS3, (1,1,l-1,h-1))

                self.image_survol = self.image_normal.copy()

                pygame.draw.rect(self.image_survol, GRIS2, (1,1,l-2,h-2))
                pygame.draw.rect(self.image_clic, GRIS2, (1,1,l-2,h-2))
                pygame.draw.rect(self.image_normal, GRIS1, (1,1,l-2,h-2))
                
                texte = font.render(texte, True, (0, 0, 0))

                self.image_normal.blit(texte, (margeh,margev))
                self.image_survol.blit(texte, (margeh,margev))
                self.image_clic.blit(texte, (margeh+1,margev+1))

                self.image = self.image_normal
                self.survole = False
                self.clic = False
                self.event = event

        def update(self):
                """ Cette méthode permet de mettre à jour l'affichage des boutons
                en fonction de s'il est survolé ou enfoncé ou non,
                et de créer un event pygame si le bouton est activé """
                if self.survole:
                        if self.clic:
                                self.image = self.image_clic
                        else:
                                self.image = self.image_survol
                else:
                        self.image = self.image_normal

        def event_clic_down(self, position):
                """ Méthode appelé lorsque le clic de souris est enfoncé """
                self.clic = self.rect.collidepoint(position)

        def event_clic_up(self, position):
                """ Méthode appelé lorsque le clic de souris est relâché """
                if self.clic:
                        if self.rect.collidepoint(position):
                                pygame.event.post(self.event)
                        self.clic = False

        def event_survol(self, position):
                """ Méthode appelé lorsque la souris est déplacée,
                pour regarder si le curseur survol le bouton """
                self.survole = self.rect.collidepoint(position)


""" Les classes suivantes ne servent qu'à placer plus efficacement une grande
        partie des éléments du menu, allégeant et rendant plus lisible le code.
        La gestion de la mise en place des éléments du menu est ainsi plus
        facile et plus facilement modifiable et paramétrable.
"""


class Ligne(pygame.Rect):
        """ Classe permettant de créer un rectangle dans lequel il est plus
                facile de placer et ajouter des éléments, et permet de
                subdiviser la surface.
        """

        def __init__(self, largeur, hauteur, couleur = COULEUR_MENU):
                """ Constructeur de la classe. Prend en paramètres les
                        dimensions (largeur/hauteur) du rectangle ainsi que sa
                        couleur qui est de la même couleur que le menu par défaut.
                """
                self.hauteur = hauteur
                self.largeur = largeur
                self.image = pygame.Surface((largeur, hauteur))
                self.image.fill(couleur)
                rect = self.image.get_rect()
                self.sprites = []
                pygame.Rect.__init__(self, rect)

        def draw(self, surface):
                """ Affiche le contenu de la ligne en fonction de la position
                        du rectangle sur la surface donnée, et transforme
                        la position des sprites contenus pour la rendre
                        relative à la surface où est affiché la ligne
                        et non plus relative à la ligne elle-même
                """
                for sprite in self.sprites:
                        sprite.rect.topleft = sprite.rel_pos
                        sprite.rect = sprite.rect.move(self.topleft)
                surface.blit(self.image, self.topleft)

        def get_pos(self, surface, position):
                """ Permet de de placer plus facilement les éléments dans
                    la ligne. Permet par exemple de placer en bas à droite,
                    ou au centre de la ligne plus facilement.
                """
                rect = surface.get_rect()
                if position == None:
                        x,y = 0,0
                elif position == "centre":
                        x,y = self.centerx - rect.centerx, self.centery - rect.centery
                else:
                        x,y = position[0], position[1]
                if x == "g": x = 0 # Place l'élément à gauche
                if x == "c": x = self.centerx - rect.centerx - self.left # Place l'élément au centre horizontalement
                if x == "d": x = self.width - rect.width # Place l'élément à droite
                if y == "h": y = 0 # Place l'élément en haut
                if y == "c": y = self.centery - rect.centery - self.top # Place l'élément au centre verticlament
                if y == "b": y = self.height - rect.height # Place l'élément en bas
                return (x,y)

        def blit(self, surface, position):
                x,y = self.get_pos(surface, position)
                self.image.blit(surface, (x,y))
                        
                
        def ajouter_texte(self, texte, position = None, police = POLICE_DEFAUT, couleur = NOIR, ):
                """ Méthode permettant d'ajouter du texte
                """
                texte = police.render(texte, True, couleur)
                self.blit(texte, position)

        def ajouter_image(self, image, position = None, redim = None):
                """ Méthode permettant d'ajouter une image
                """
                if type(image) == str:
                        image = pygame.image.load(image)
                if redim:
                        image = pygame.transform.scale(image, redim)
                self.blit(image, position)

        def ajouter_sprite(self, sprite, position = None):
                """ Méthode permettant d'ajouter un sprite
                """
                x,y = self.get_pos(sprite.image, position)
                sprite.rect.topleft = x,y
                sprite.rel_pos = x,y
                self.sprites.append(sprite)
                
class Cadre:
        """ Classe permettant de créer une surface divisée en plusieurs
                lignes, et de gérer leur position.
        """

        police_titre = POLICE_DEFAUT
        couleur_titre = NOIR

        def __init__(self, largeur, titre, **kwargs):
                """ Prend en paramètres la largeur le titre du cadre.
                    Il est possible de mettre des marges et une couleur
                    de fond autre que celles de base.
                    La hauteur du cadre est déduite automatiquement
                    en fonction du des éléments qu'il contient
                """
                self.couleur_fond = kwargs.get("couleur_fond", COULEUR_MENU)
                self.marge_gauche = kwargs.get("marge_gauche", kwargs.get("marge", 10))
                self.marge_droite = kwargs.get("marge_droite", kwargs.get("marge", 10))
                self.marge_haut = kwargs.get("marge_haut", kwargs.get("marge", 10))
                self.marge_bas = kwargs.get("marge_bas", kwargs.get("marge", 10))
                self.espace = kwargs.get("espace", 5)
                pos = kwargs.get("pos", (0,0))
                
                self.largeur = largeur
                self.titre = self.police_titre.render(titre, True, self.couleur_titre, self.couleur_fond)
                self.titre_rect = self.titre.get_rect()
                self.lignes = []
                self.rect = pygame.Rect(pos + (0,0))

        def draw(self, surface):
                """ Affiche le contenu du cadre sur la surface donnée,
                        et adapte la position des sprites contenus pour
                        la rendre relative au menu et non plus relative
                        aux lignes dans lesquels sont contenus les sprites.
                        Permet ainsi de gérer l'affichage des sprites
                        directement depuis le menu, et permet faire fonctionner
                        correctement les boutons.
                """
                for ligne in self.lignes:
                        for sprite in ligne.sprites:
                                sprite.rect.topleft = sprite.rel_pos
                                sprite.rect = sprite.rect.move(ligne.topleft)
                                sprite.rect = sprite.rect.move(self.rect.topleft)
                surface.blit(self.image, self.rect.topleft)

        def __getattr__(self, attribut):
                if attribut == "sprites":
                        return self.get_sprites()
                if attribut == "hauteur":
                        return self.get_hauteur()
                if attribut == "image":
                        return self.get_image()

        def get_sprites(self):
                """ Renvoie la liste des sprites contenues dans le cadre """
                liste = []
                for ligne in self.lignes:
                        for sprite in ligne.sprites:
                                liste.append(sprite)
                return liste

        def ajouter_ligne(self, ligne, n=1):
                """ Permet d'ajouter une ligne au cadre.
                        Crée une ligne vide de hauteur spécifié en paramètre
                        ou ajoute directement la ligne donnée en paramètre.
                """
                for i in range(n):
                        if type(ligne) == int:
                                ligne = Ligne(self.largeur - self.marge_gauche - self.marge_droite, ligne)
                        self.lignes.append(ligne)

        def get_hauteur(self):
                """ Calcul la hauteur du cadre
                """
                hauteur = self.marge_haut + self.marge_bas + self.titre_rect.height
                hauteur += (len(self.lignes) - 1) * self.espace
                for i in range(len(self.lignes)):
                        hauteur += self.lignes[i].height
                self.hauteur = hauteur
                return hauteur

        def get_image(self):
                """ Cette méthode permet de mettre en place l'affichage du cadre
                """
                hauteur = self.hauteur
                self.image = pygame.Surface((self.largeur, self.hauteur))
                pos = self.rect.topleft
                self.rect = self.image.get_rect()
                self.rect.topleft = pos
                self.image.fill(self.couleur_fond)
                
                pygame.draw.rect(self.image, GRIS3, (0,int(self.titre_rect.height/2), self.largeur, self.hauteur-int(self.titre_rect.height/2)), 1)
                self.titre_rect.centerx = self.rect.width/2
                self.titre_rect.top = 0
                self.image.blit(self.titre, self.titre_rect)

                y = 0 + self.titre_rect.height + self.marge_haut
                for ligne in self.lignes:
                        ligne.topleft = self.marge_gauche, y
                        ligne.draw(self.image)
                        y += ligne.height + self.espace
                return self.image

class StatsMenu(Cadre):
        """ Classe servant à afficher les statistiques dans le menu """

        police = POLICE_DEFAUT

        def __init__(self, largeur, liste, **kwargs):
                """ Prend en paramètre la largeur du cadre,
                    et la liste des statistique contenant
                    la légende qui sera affichée pour la stat
                    et la fonction à appeler à chaque mise à
                    jour pour déterminer la valeur de la stat
                    ainsi que ses éventuels paramètres.
                """
                taille_police = self.police.size("")[1]
                Cadre.__init__(self, largeur, "  Statistiques  ", **kwargs)
                self.liste_stats = []
                self.sprites_stats = pygame.sprite.Group()
                [self.set_liste(*liste[i]) for i in range(len(liste))]
                for i in range(len(self.liste_stats)):
                        self.ajouter_ligne(taille_police)
                        self.lignes[i].ajouter_texte(self.liste_stats[i]["nom"])
                        stat = SpriteStat(self.liste_stats[i]["fonction"], *self.liste_stats[i]["args"])
                        self.lignes[i].ajouter_sprite(stat, "dc")
                self.get_image()

        def set_liste(self, nom, fonction, *args):
                """ Transforme la liste donnée à la construction de la classe
                    en un dicionnaire plus pratique à utiliser
                """
                self.liste_stats.append({"nom": nom, "fonction": fonction, "args": args})

class Legende(Cadre):
        """ Classe permettant d'afficher la légende """
        
        """ Contient la liste des images de la légende
            Source: https://www.spriters-resource.com/
        """
        images = ["img/legende/PetitHerbivore_legende.png",
                  "img/legende/GrandHerbivore_legende.png",
                  "img/legende/PetitCarnivore_legende.png",
                  "img/legende/GrandCarnivore_legende.png",
                  "img/legende/Vegetation_faible.png",
                  "img/legende/Vegetation_forte.png"]
        """ Contient le texte à afficher pour chaque image
        """
        legendes = ["Petit herbivore",
                    "Grand herbivore",
                    "Petit carnivore",
                    "Grand carnivore",
                    "Vegetation ( - quantité)",
                    "Vegetation ( + quantité)"]
        
        taille_image = 20
        police = POLICE_DEFAUT

        def __init__(self, largeur, **kwargs):
                """ Constructeur de la classe. Prend en paramètre la largeur que doit faire la légende
                et les éventuels paramètres pour le cadre
                """
                Cadre.__init__(self, largeur, "  Légende  ", **kwargs)
                for i in range(len(self.images)):
                        self.ajouter_ligne(self.taille_image)
                        self.lignes[i].ajouter_image(self.images[i], redim = [self.taille_image] * 2)
                        self.lignes[i].ajouter_texte(self.legendes[i], (self.taille_image + 10, "c"), POLICE2)
                        if i<len(CLASSES_ENTITES):
                                classe = CLASSES_ENTITES[i]
                                event = pygame.event.Event(AFFICHAGE_CLASSE)
                                event.classe = classe
                                b1, b2 = Bouton("Afficher", POLICE2, event), Bouton("Masquer", POLICE2, event)
                                [self.lignes[i].ajouter_sprite(b, "dc") for b in [b1,b2]]
                self.get_image()

        def get_sprites(self):
                """ Renvoie la liste des sprites sous forme de dictionnaire
                        ayant pour clés les classes des entités et pour items
                        un tableau comportant le bouton servant à afficher et
                        celui servant à masquer les entités de la classe
                        correspondante dans la simulateur.
                """
                liste = Cadre.get_sprites(self)
                dic = {}
                for sprite in liste:
                        if not sprite.event.classe in dic.keys():
                                dic[sprite.event.classe] = []
                        dic[sprite.event.classe].append(sprite)
                return dic
                
class Interactions(Cadre):
        """ Classe permetant d'interagir avec l'écosystème """

        police = POLICE2 = pygame.font.SysFont("Times", 16)

        def __init__(self, largeur, simulateur, **kwargs):
                """ Prend en paramètres la largeur du cadre et le
                    simulateur, ainsi que les eventuels paramètres
                    pour l'affichage du cadre
                """
                Cadre.__init__(self, largeur, "  Interactions  ", **kwargs)
                self.simulateur = simulateur

                interactions = ["Ajouter des entités", "Supprimer des entités"]
                for i in range(len(interactions)):
                        event = pygame.event.Event(INTERACTION)
                        event.fonction = [self.ajouter_entites, self.selection_supprimer_entites][i]
                        bouton = self.bouton_lancer = Bouton(interactions[i], event = event)
                        event = pygame.event.Event(INTERACTION_OPTIONS)
                        event.interaction = i
                        bouton.image_normal_base = bouton.image_normal
                        bouton.image_survol_base = bouton.image_survol
                        bouton_options = self.bouton_lancer = Bouton("...", event = event)
                        self.ajouter_ligne(bouton.rect.height)
                        self.lignes[i].ajouter_sprite(bouton, "gc")
                        self.lignes[i].ajouter_sprite(bouton_options, "dc")

                
                self.interaction_clic = None
                
                self.cible = "Petit carnivore"
                self.quantite = 3
                self.curseur = pygame.mouse.get_cursor()
                self.rayon = 5

        def modifier_options(self, event):
                """ Fonction appelée lorsqu'un des deux boutons pour
                    modifier les options des interactions est enfoncé
                """
                if event.interaction == 0: self.fenetre_options1()
                else: self.fenetre_options2()
                
        def fenetre_options1(self):
                """ Ouvre une fenêtre Tkinter très simple pour modifier
                    les options de l'interaction servant à ajouter des entités
                """
                cibles = ["Petit herbivore", "Grand herbivore", "Petit carnivore", "Grand carnivore", "Aléatoire"]
                fenetre = tk.Tk()
                fenetre.title("Options")
                f1 = tk.LabelFrame(text = "Entités à ajouter")
                cible = tk.StringVar(value=self.cible)
                tk.OptionMenu(f1, cible, *cibles).pack(padx=5,pady=5)
                f1.pack(padx=10,pady=10, fill=tk.X)

                f2 = tk.LabelFrame(text = "Nombre d'entités à ajouter:")
                quantite = tk.StringVar(value=self.quantite)
                tk.Spinbox(f2, from_ = 0, to = 10, increment = 1, width=15, textvariable = quantite).pack(padx=5,pady=5)
                f2.pack(padx=10,pady=10, fill=tk.X)
                
                tk.Button(fenetre, text="Confirmer", command=fenetre.destroy).pack(side=tk.BOTTOM)
                fenetre.bind("<Return>", fenetre.destroy)
                fenetre.mainloop()
                
                self.quantite = int(quantite.get())
                self.cible = cible.get()

        def fenetre_options2(self):
                """ Ouvre une fenêtre Tkinter très simple pour modifier
                    les options de l'interaction servant à supprimer des entités
                """
                cibles = ["Petit herbivore", "Grand herbivore", "Petit carnivore", "Grand carnivore", "Aléatoire"]
                fenetre = tk.Tk()
                fenetre.title("Options")
                notebook = ttk.Notebook(fenetre)
                notebook.pack(pady=5, padx=10)

                f1 = tk.LabelFrame(text = "Rayon")
                rayon = tk.IntVar(value=self.rayon)
                tk.Spinbox(f1, textvariable = rayon).pack(padx=5,pady=5)
                f1.pack(padx=10,pady=10, fill=tk.X)
                
                bf = tk.Frame(fenetre)
                bf.pack(side = tk.BOTTOM)
                tk.Button(bf, text="Confirmer", command=fenetre.destroy).pack(side=tk.BOTTOM)
                fenetre.mainloop()
                self.rayon = rayon.get()

        def ajouter_entites(self, **kwargs):
                """ Fonction appelée que l'interaction pour ajouter des
                    entités est utilisé.
                    Renvoie la liste des entités ajoutées
                """
                if self.cible != "Aléatoire":
                        classe = {"Petit herbivore": PetitHerbivore, "Grand herbivore": GrandHerbivore, "Petit carnivore": PetitCarnivore, "Grand carnivore": GrandCarnivore}
                        liste = self.simulateur.generer(classe[self.cible], self.quantite)
                        effectif = self.simulateur.effectifs[classe[self.cible]]
                        effectif[len(effectif)-1] += len(liste)
                        return liste
                else:
                        classes = [PetitHerbivore, GrandHerbivore, PetitCarnivore, GrandCarnivore]
                        liste = []
                        for n in range(self.quantite):
                                i = randint(0, len(classes)-1)
                                liste+=self.simulateur.generer(classes[i])
                        return liste

        def selection_supprimer_entites(self, **kwargs):
                """ Fonction appelée que le bouton de l'interaction
                    pour supprimer des entités est activé.
                    La supression des entités se fait lorsque l'on
                    clique sur la carte une fois ce bouton activé.
                """
                taille_pixel = kwargs["taille_pixel"]
                if self.interaction_clic:
                        self.interaction_clic = None
                        self.lignes[1].sprites[0].image_normal = self.lignes[1].sprites[0].image_normal_base
                        self.lignes[1].sprites[0].image_survol = self.lignes[1].sprites[0].image_survol_base
                else:
                        self.interaction_clic = self.supprimer_entites
                        self.curseur = self._creer_curseur(self.rayon * taille_pixel, 1)
                        self.lignes[1].sprites[0].image_normal = self.lignes[1].sprites[0].image_clic
                        self.lignes[1].sprites[0].image_survol = self.lignes[1].sprites[0].image_clic
                return []

        def supprimer_entites(self, pos):
                """ Fonction appelé lorsque l'on clique sur la carte
                    alors que le bouton pour supprimer des entités
                    est activé.
                    Les entités sont retirées de la carte et de la
                    liste du simulateur
                    Renvoie la liste des entités supprimées
                """
                liste=[]
                for y in range(pos[1]-self.rayon, pos[1]+self.rayon):
                        for x in range(int(pos[0]-(self.rayon**2 - (y-pos[1])**2)**0.5), int(pos[0] + (self.rayon**2 - (y-pos[1])**2)**0.5)+1):
                                if self.simulateur.carte.case_valide(x,y):
                                        if self.simulateur.carte.faune[x,y]:
                                                entite = self.simulateur.carte.faune[x,y]
                                                self.simulateur.carte.faune[x,y] = None
                                                self.simulateur.liste_entites[type(entite)].remove(entite)
                                                liste.append(entite)
                
                return liste
                                        

        def _creer_curseur(self, r, e):
                """ Permet de créer un cercle de rayon r et
                    d'épaisseur e pour le curseur lorsqu'on
                    veut utiliser l'interaction pour supprimer
                    des entités
                """
                curseur_strs = ()
                taille = 8 * ((2 * r) // 8 + 1)
                for y in range(taille):
                        ligne = ""
                        for x in range(taille):
                                d = ((x - r)**2 + (y - r)**2)**0.5
                                
                                if (x,y) in [(r-2,r),(r-1,r),(r,r-2),(r,r-1),(r,r),(r,r+1),(r,r+2),(r+1,r),(r+2,r)]:
                                        ligne += "X"
                                elif d<r-e/2 or d>r+e/2:
                                        ligne += " "
                                else:
                                        ligne += "X"
                        curseur_strs+=(ligne,)
                return ((taille,taille), (r,r), *(pygame.cursors.compile(curseur_strs, black="X", white="x")))
                
