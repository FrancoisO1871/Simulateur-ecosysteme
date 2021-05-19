# coding: utf8
""" Ce module permet l'affichage de la fenêtre principale servant
    à afficher l'écosystème ou le graphique montrant son évolution
"""

import pygame
from parametres_defaut import *
import pygame.locals
import sys
from main import *

LEGENDES = {PetitHerbivore: "Petit herbivore",
                PetitCarnivore: "Petit carnivore",
                GrandHerbivore: "Grand herbivore",
                GrandCarnivore: "Grand carnivore"}

# Source des sprites: https://www.spriters-resource.com/
SPRITES = {PetitHerbivore: "img/PetitHerbivore_sprite_20px.png", PetitCarnivore: "img/PetitCarnivore_sprite_20px.png", GrandHerbivore: "img/GrandHerbivore_sprite_20px.png", GrandCarnivore: "img/GrandCarnivore_sprite_20px.png"}

TAILLE_CASE = 10
ECOSYSTEME = 1
STATISTIQUES = 2
GRIS1 = (217, 217, 217)
GRIS2 = (236, 236, 236)
GRIS3 = (130,130,130)
BLANC = (255,255,255)
NOIR = (0,0,0)
ONGLETS = pygame.USEREVENT + 5
COULEURS = {PetitHerbivore: (0,255,0), PetitCarnivore: (255,100,100), GrandHerbivore: (0,0,255), GrandCarnivore: (150,0,0)}

if not pygame.font.get_init():
        pygame.font.init()

POLICE_DEFAUT = pygame.font.SysFont("Times", 16)
POLICE2 = pygame.font.SysFont("Times", 12)
POLICE_TITRE = pygame.font.SysFont("Times", 24)
POLICE_TITRE.set_bold(True)

class FenetrePrincipale:
        """ Classe permettant de visualiser l'écosystème dans l'interface graphique
        """
        def __init__(self, simulateur, largeur, hauteur):
                """ Prend en paramètre le simulateur à afficher,
                    ainsi que la largeur et la hauteur que doit
                    faire surface de la fenêtre
                """
                self.largeur = largeur
                self.hauteur = hauteur
                self.rect = pygame.Rect(0, 0, largeur, hauteur)
                self.simulateur = simulateur
                self.fenetre = ECOSYSTEME # Correspond à l'onglet sélectionné
                # L'attribut fond correspond à l'image de fond sur laquelle est affiché la carte ou le graph
                self.fond = pygame.Surface((largeur, hauteur))
                
                """ On crée les deux onglets de la fenêtre qu'on ajoute comme
                    attribut et qu'on met dans un groupe de sprites
                """
                self.onglet_eco = Onglet("Ecosystème", True, event = pygame.event.Event(ONGLETS))
                self.onglet_stats = Onglet("Statistiques", False, event = pygame.event.Event(ONGLETS))
                self.onglet_stats.rect.bottomleft = self.onglet_eco.rect.bottomright
                self.onglets = pygame.sprite.Group()
                self.onglets.add(self.onglet_eco, self.onglet_stats)
                self.onglet_rect = pygame.Rect.union(self.onglet_eco.rect, self.onglet_stats.rect)
                ho = self.onglet_eco.rect.height # Hauteur de l'onglet: permet de déduire la hauteur restante pour l'affichage du reste
                
                """ On met en place l'image de fond sur laquelle seront affichés
                    les onglets et la carte ou le graphique
                """
                self.fond.fill((226, 226, 226))
                pygame.draw.rect(self.fond, GRIS3, (0,ho-1,largeur,hauteur))
                pygame.draw.rect(self.fond, GRIS2, (1,ho,largeur-2,hauteur-1-ho))
                self.image = self.fond.copy()
                self.onglets.draw(self.image)
                
                """ On ajoute comme attribut un objet de la classe FenetreEcosysteme
                    permettant d'afficher la carte et un de la classe FenetreStatistiques
                    permettant d'afficher le graphique
                """
                self.ecosysteme = FenetreEcosysteme(simulateur, largeur, hauteur-ho)
                self.statistiques = FenetreStatistiques(simulateur, largeur-2, hauteur-ho-1)
                self.centre = (largeur/2, (hauteur-ho)/2 + ho) # Centre de la surface où afficher le graphique ou la carte

        def draw(self, surface, classes):
                """ Affiche la fenêtre principale
                    Prend en paramètres la surface sur laquelle
                    la fenêtre doit être affichée, ainsi que les
                    classes qui sont affichées.
                    En fonction de l'onglet qui est sélectionné,
                    affiche le graphique ou la carte dans le rectangle
                    de l'attribut rect sur la surface donnée.
                """
                if self.fenetre == ECOSYSTEME:
                        self.ecosysteme.rect.center = self.centre
                        self.ecosysteme.draw(self.image, classes)
                else:
                        self.statistiques.rect.center = self.centre
                        self.statistiques.draw(self.image, classes)
                surface.blit(self.image, self.rect)

        def position_relative(self, pos):
                """ Renvoie la position relative au menu
                        La position de la souris correspond à la position
                        dans la fenêtre pygame et non dans le menu. Les positions
                        des boutons étant relatif à la position du menu, cette
                        méthode permet de gérer correctement ces boutons en
                        transformant une position absolue dans la fenêtre en une
                        position relative au menu.
                """
                x,y = pos
                a,b = self.rect.topleft
                return (x-a, y-b)

        def update(self):
                """ Appelle la fonction update de la fenêtre
                    de l'écosystème ou du graphique en fonction
                    de l'onglet sélectionné.
                """
                if self.fenetre == ECOSYSTEME:
                        self.ecosysteme.update()
                else:
                        self.statistiques.update()

        def event(self, event):
                """ Gère les events de clic de souris sur
                    les onglets permettant d'alterner entre
                    la carte et le graphique.
                """
                pos = self.position_relative(event.pos)
                if not self.onglet_stats.selectionne:
                        if self.onglet_stats.rect.collidepoint(pos): 
                                """ Si l'onglet stats n'est pas sélectionné
                                    et qu'on clic dessus, la fenêtre affichera
                                    désormais le graphique et non plus la carte
                                """
                                self.onglets.update()
                                self.fenetre = STATISTIQUES
                                self.image = self.fond.copy()
                                self.onglets.draw(self.image)

                elif self.onglet_eco.rect.collidepoint(pos):
                        """ Si l'onglet de l'écosystème n'est pas sélectionné
                            et qu'on clic dessus, la fenêtre affichera
                            désormais la carte de l'écosystème et
                            non plus le graphique
                        """
                        self.fenetre = ECOSYSTEME
                        self.onglets.update()
                        self.image = self.fond.copy()
                        self.onglets.draw(self.image)
                        self.ecosysteme = FenetreEcosysteme(self.simulateur, self.largeur, self.hauteur-self.onglet_eco.rect.height)

        def reinitialiser(self, simulateur):
                """ Méthode appelée lorsque la simulation est
                        réintialiser pour lier le nouveau
                        simulateur
                """
                self.image = self.fond.copy()
                self.onglets.draw(self.image)
                self.simulateur = simulateur
                self.statistiques.simulateur = simulateur
                self.ecosysteme = FenetreEcosysteme(simulateur, self.largeur, self.hauteur-self.onglet_eco.rect.height)

class FenetreStatistiques:
        """ Cette classe permet d'afficher un graphique montrant l'évolution
                de l'effectif des différentes entités
        """

        def __init__(self, simulateur, largeur, hauteur):
                """ Prend en attribut le simulateur ainsi que
                    les dimensions de la surface sur laquelle
                    sera affiché le graphique
                """
                self.simulateur = simulateur
                self.largeur = largeur
                self.hauteur = hauteur

                self.fond = pygame.Surface((largeur, hauteur)) # Image de de fond
                self.rect = self.fond.get_rect() # Rectangle sur la laquelle est dessiné la fenêtre
                self.graphe = pygame.Surface((500,500)) # Surface de la courbe
                self.graphe_rect = self.graphe.get_rect() # Rectangle sur la laquelle est dessiné la courbe
                self.graphe_rect.center = self.rect.centerx, self.rect.centery - 30

                self.fond.fill(GRIS2)
                
                """ On ajoute un titre au dessus de la courbe
                """
                titre = POLICE_TITRE.render("Evolution des populations", True, NOIR)
                rect = titre.get_rect()
                rect.center = (self.rect.centerx, self.graphe_rect.top - 30)
                self.fond.blit(titre, rect)
                
                """ On ajoute une légende pour les deux axes
                """
                axex = POLICE_DEFAUT.render("Nombre d'itérations", True, NOIR)
                rect = axex.get_rect()
                rect.midtop = (self.rect.centerx, self.graphe_rect.bottom + 30)
                self.fond.blit(axex, rect)

                axey = POLICE_DEFAUT.render("Nombre d'entités", True, NOIR)
                axey = pygame.transform.rotate(axey, 90)
                rect = axey.get_rect()
                rect.midright = (self.graphe_rect.left - 30, self.rect.centery)
                self.fond.blit(axey, rect)

                """ On affiche la légende des différentes courbes
                    sur l'image de fond
                """
                surfaces = []
                for k in COULEURS.keys():
                        texte = POLICE_DEFAUT.render(LEGENDES[k], True, NOIR)
                        x,y = texte.get_rect().size
                        x,y = x + 35, y+10
                        s = pygame.Surface((x,y))
                        s.fill(GRIS2)
                        pygame.draw.line(s, COULEURS[k], (15,y/2), (30, y/2))
                        s.blit(texte, (35, 5))
                        surfaces.append(s)
                rect = surfaces[0].get_rect()
                for i in range(1,len(surfaces)):
                        r2 = surfaces[i].get_rect()
                        r2.topleft = rect.topright
                        rect = pygame.Rect.union(rect, r2)
                legende = pygame.Surface(rect.size)
                x = 0
                for i in range(len(surfaces)):
                        legende.blit(surfaces[i], (x,0))
                        x+= surfaces[i].get_rect().width

                rect.center = self.graphe_rect.centerx, self.graphe_rect.bottom + 80
                self.fond.blit(legende, rect)

                self.image = self.fond.copy()
                

        def draw(self, surface, classes):
                self.image = self.fond.copy()
                self.graphe.fill((255,255,255))
                maxs=[max(self.simulateur.effectifs[k]) for k in self.simulateur.effectifs.keys() if classes[k]]
                if maxs == []:
                        ymax = 1
                else:
                        ymax = max(maxs)*1.05
                        if ymax == 0:
                                ymax = 1
                
                [self.dessiner_courbes(self.graphe, self.simulateur.effectifs[k], ymax, COULEURS[k]) for k in self.simulateur.effectifs.keys() if classes[k]]

                self.axes(ymax, self.simulateur.temps)

                self.image.blit(self.graphe, self.graphe_rect)
                surface.blit(self.image, self.rect)

        def update(self):
                self.simulateur.iteration()

        def axes(self, ymax, xmax):
                """ Dessine l'axe des abscisses et des ordonnées en
                    dessous à coté et en dessous de la surface où sont
                    affichées les courbes
                """
                if xmax == 0: 
                        """ Si xmax vaut zéro, aucune courbe n'est de toutes
                            façons affiché, on met xmax à 1 pour éviter une
                            division par 0
                        """
                        xmax = 1
                rect = self.graphe_rect # On récupère le rectangle où sont affichés les courbes
                h,l = rect.size
                
                """ On détermine tout d'abord l'espace entre chaque points
                    pour chaque axe, de telle sorte qu'il n'y ait pas plus
                    de 15 points, et que l'espace entre deux points soit
                    le produit de 1, 2,5 ou 5 (valeurs du tableau e) et
                    d'une puissance de 10
                """
                e = [1, 2.5, 5]
                i=0
                while ymax / (e[i%3] * 10**(i//3)) > 15: i+=1
                ey = (e[i%3] * 10**(i//3))
                i=0
                while xmax / (e[i%3] * 10**(i//3)) > 15: i+=1
                ex = (e[i%3] * 10**(i//3))
                
                """ On affiche l'axe des ordonnées à gauche du rectangle
                    des courbes. On dessine un trait vertical tout le long
                    du rectangle, puis on ajoute un trait en fonction de l'espace
                    déterminé tout juste précédemment
                """
                x = rect.left - 5
                pygame.draw.line(self.image, NOIR, (x, rect.bottom), (x, rect.top))
                y = rect.bottom
                for i in range(int(ymax/ey)+1):
                        texte = POLICE2.render(str(int(i*ey)), True, NOIR)
                        texte_rect = texte.get_rect()
                        texte_rect.midright = (x-4, y)
                        self.image.blit(texte, texte_rect)
                        pygame.draw.line(self.image, NOIR, (x-2,y), (x,y))
                        y -= h/ymax * ey

                """ On affiche l'axe des abscisses en bas du rectangle
                    des courbes de façon similaire
                """
                y = rect.bottom + 5
                pygame.draw.line(self.image, NOIR, (rect.left, y), (rect.right, y))
                x = rect.left
                for i in range(int(xmax/ex)+1):
                        texte = POLICE2.render(str(int(i*ex)), True, NOIR)
                        texte_rect = texte.get_rect()
                        texte_rect.midtop = (x, y+4)
                        self.image.blit(texte, texte_rect)
                        pygame.draw.line(self.image, NOIR, (x,y+2), (x,y))
                        x += l/xmax * ex
                
                

        def dessiner_courbes(self, surface, effectif, ymax, couleur):
                """ Dessine les courbes correspondantes à l'évolution
                        de l'effectif de chaque classe d'entité sur la
                        surface donnée
                        Prend donc en paramètres la surface sur laquelle
                        on dessine la courbe, la liste des effectifs des
                        entités de chaque classe, la valeur en ordonnée
                        maximale (la valeur en abscisse est déduite de la
                        taille de la liste des effectifs) et la liste
                        des couleurs de chaque courbe
                """
                rect = surface.get_rect()
                l,h = rect.size
                xmax = len(effectif) - 1
                if(xmax<l):
                        """ Si le nombre de valeurs est inférieur au nombre de
                                pixels, on trace les lignes qui relient tous
                                les points de chaque valeur
                        """
                        for i in range(xmax):
                                x1,y1 = int(i*l/xmax), h - effectif[i] * h/ymax
                                x2,y2 = int((i+1)*l/xmax), h - effectif[i+1] * h/ymax
                                pygame.draw.line(surface, couleur, (x1,y1), (x2,y2))
                else:
                        """ Sinon, si le nombre de pixel est inférieur
                                au nombre de valeurs, alors on trace les
                                lignes reliant les points pour chaque pixel
                        """
                        for x in range(l-1):
                                y1 = h - effectif[int(x*xmax/l)] * h/ymax
                                y2 = h - effectif[int((x+1)*xmax/l)] * h/ymax
                                pygame.draw.line(surface, couleur, (x,y1), (x+1,y2))
                

class FenetreEcosysteme:
        """ Classe permettant l'affichage de l'écosystème """

        def __init__(self, simulateur, largeur, hauteur):
                """ Constructeur de la classe
                    Prend en paramètres le simulateur et les dimensions
                    de la surface disponible pour afficher la carte
                """
                self.simulateur = simulateur
                """ On détermine tout d'abord le nombre de pixel que va
                    faire chaque case en fonction de la surface disponible
                    et la surface que cela prendra
                """
                self.taille_pixel = min(largeur // simulateur.carte.largeur, hauteur // simulateur.carte.hauteur)
                self.largeur = simulateur.carte.largeur * self.taille_pixel
                self.hauteur = simulateur.carte.hauteur * self.taille_pixel
                self.image = pygame.Surface((self.largeur, self.hauteur))
                self.rect = self.image.get_rect()
                
                
                self.images_sprites = {}
                self.sprites = {Vegetation: pygame.sprite.Group()}
                """ On redimensionne l'image des sprites pour l'adapter
                    à la surface disponible
                """
                for e in SPRITES.keys():
                        self.sprites[e] = pygame.sprite.Group()
                        img = pygame.image.load(SPRITES[e])
                        x,y = img.get_rect().size
                        img = pygame.transform.scale(img, (int((x/20) * self.taille_pixel),int((y/20) * self.taille_pixel)))
                        self.images_sprites[e] = img
                
                """ L'attribut liste_sprites correspond à un dictionnaire
                    ayant pour clés chaque entité, et pour valeur son sprite
                    associé. Permet d'accéder directement au sprite d'une 
                    entité précise, et permet ainsi d'accéder directement aux
                    sprites à supprimer lorsque qu'une entité meurt.
                """
                self.liste_sprites = {}
                
                """ On crée tous les sprites pour chaque entité
                """
                for k in simulateur.liste_entites.keys():
                        for entite in simulateur.liste_entites[k]:
                                if k==Vegetation:
                                        self.sprites[k].add(SpriteVegetation(entite, self.taille_pixel))
                                else:
                                        sprite = SpriteAnimaux(entite, self.taille_pixel, self.images_sprites)
                                        self.liste_sprites[entite] = sprite
                                        self.sprites[type(entite)].add(sprite)
                
                """ On met à jour tous les sprites et on les affiche
                """
                [self.sprites[key].update() for key in self.sprites.keys()]
                [self.sprites[key].draw(self.image) for key in self.sprites.keys()]

        def update(self):
                """ Fait avancer la simulation d'une itération,
                    supprime les sprites des entités décédées,
                    affiche un sprite pour chaque nouvelle entité,
                    et met à jour tous les sprites
                """
                self.simulateur.iteration()
                        
                self.add_sprites(self.simulateur.entite_nouvelles)
                self.del_sprites(self.simulateur.entite_morte)

                [self.sprites[key].update() for key in self.sprites.keys()]
                
                
        def draw(self, surface, classes):
                """ Affiche la carte sur la surface donnée
                    Affiche toutes les cases de végétation puis
                    tous les sprites des entités si leur affichage
                    (déterminée à partir du paramètre classe)
                    est activé
                """
                self.image.fill((0,0,0))
                [self.sprites[key].draw(self.image) for key in self.sprites.keys() if classes[key]]
                surface.blit(self.image, self.rect)

        def add_sprites(self, liste):
                """ Crée un sprite pour chaque nouvelle entité et l'ajoute à la liste des sprites """
                for i in range(len(liste)):
                        sprite = SpriteAnimaux(liste[i], self.taille_pixel, self.images_sprites)
                        self.liste_sprites[liste[i]] = sprite
                        self.sprites[type(liste[i])].add(sprite)

        def del_sprites(self, liste):
                """ Retire tous les sprites correspondant à une entité qui n'existe plus """
                for i in range(len(liste)):
                        self.liste_sprites[liste[i]].kill()
                        del self.liste_sprites[liste[i]]

        def position_ecosysteme(self, pos):
                """ Retourne la case correspondant à la position donnée
                    Permet de déterminer la zone sur laquelle effectuer
                    les interactions
                """
                x,y = pos
                a,b = self.rect.topleft
                return ((x-a)//self.taille_pixel, (y-b)//self.taille_pixel)

class SpriteVegetation(pygame.sprite.Sprite):
        """ Classe correspondant au sprite pygame d'une entité de végétation """
        
        def __init__(self, entite, taille_pixel):
                """ Constructeur de la classe """
                pygame.sprite.Sprite.__init__(self)

                self.entite = entite
                self.x, self.y = entite.position
                
                self.image = pygame.Surface([taille_pixel] * 2)
                self.image.fill(pygame.Color(0,int(55+2*self.entite.quantite),0))
                self.rect = self.image.get_rect()
                self.rect = self.rect.move(self.x * taille_pixel,self.y * taille_pixel)

        def update(self):
                """ Met à jour la couleur du pixel représentant la végétation en fonction de sa quantité """
                self.image.fill(pygame.Color(0,int(55+2*self.entite.quantite),0))

class SpriteAnimaux(pygame.sprite.Sprite):
        """ Sprite pygame correspondant à toutes les entités qui ne sont pas de la végétation """

        def __init__(self, entite, taille_pixel, sprites):
                """ Constructeur de la classe SpriteAnimaux """ 
                pygame.sprite.Sprite.__init__(self)

                self.entite = entite
                self.x, self.y = entite.position
                self.taille_pixel = taille_pixel
                self.image = sprites[type(entite)]
                self.rect = self.image.get_rect()
                self.rect = self.rect.move(self.x * taille_pixel,self.y * taille_pixel)

        def update(self):
                """ Déplace le sprite à la nouvelle position de l'entité """
                t = self.taille_pixel
                x1,y1 = self.entite.position
                self.rect = self.rect.move(x1*t-self.x*t,y1*t-self.y*t)
                self.x = x1
                self.y = y1

class Onglet(pygame.sprite.Sprite):
        """ Classe Onglet héritant de la classe Sprite de pygame
            Très similaire à la classe Bouton du module menu.
            Permet de créer les deux onglets pour choisir entre
            l'affichage de la carte ou du graphique.
        """

        def __init__(self, texte, select, font = POLICE_DEFAUT, event = None, margeh = 15, margev = 5):
                """ Constructeur de la classe Onglet """
                pygame.sprite.Sprite.__init__(self)
                l,h = font.size(texte)
                l += margeh * 2
                h += margev * 2
                self.image_select = pygame.Surface((l, h))
                self.image_unselect = pygame.Surface((l, h-4))
                self.rect_unselect = self.image_unselect.get_rect()
                self.rect_select = self.image_select.get_rect()

                pygame.draw.rect(self.image_select, GRIS3, self.rect_select, 1)
                pygame.draw.rect(self.image_select, GRIS2, (1,1,l-2,h-1))

                pygame.draw.rect(self.image_unselect, GRIS3, self.rect_unselect, 1)
                pygame.draw.rect(self.image_unselect, GRIS1, (1,1,l-2,h-6))
                
                texte = font.render(texte, True, (0, 0, 0))

                self.image_select.blit(texte, (margeh,margev))
                self.image_unselect.blit(texte, (margeh,margev-2))

                
                self.event = event
                self.rect = self.rect_select
                self.selectionne = not select
                self.update()
                        
                 

        def event(self, position):
                """ Méthode appelé lorsque le clic de souris est enfoncé """
                if self.rect.collidepoint(position) and not self.selectionne:
                        pygame.event.post(self.event)
                        self.selectionne = True
                        self.image = self.image_select
                        
        def update(self):
                """ Met à jour le sprite
                """
                select = self.selectionne
                if select:
                        self.selectionne = False
                        self.image = self.image_unselect
                        self.rect_unselect.bottomleft = self.rect.bottomleft
                        self.rect = self.rect_unselect
                else:
                        self.selectionne = True
                        self.image = self.image_select
                        self.rect_select.bottomleft = self.rect.bottomleft
                        self.rect = self.rect_select
