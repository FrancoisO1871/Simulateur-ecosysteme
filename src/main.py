# coding: utf8

""" Module principal du programme servant à lancer l'interface graphique du programme """

import pygame
from simulateur import *
from parametres_defaut import *
from menu import *
from fenetre import *
import pygame.locals
import sys
import time
import parametres


PAUSE = pygame.USEREVENT + 1
REINITIALISER = pygame.USEREVENT + 2
PARAMETRES = pygame.USEREVENT + 3
AFFICHAGE_CLASSE = pygame.USEREVENT + 4
ONGLETS = pygame.USEREVENT + 5
INTERACTION = pygame.USEREVENT + 6
INTERACTION_OPTIONS = pygame.USEREVENT + 7

simulateur = Simulateur(50,50,50,50)

TAILLE_CASE = 10

LARGEUR_MENU = 240
LARGEUR = 960
HAUTEUR = 720

if __name__ == '__main__':

        """ Initialisation de l'interface graphique
        """

        pygame.init()
        CURSEUR_BASE = pygame.mouse.get_cursor()
        pygame.display.set_caption("Simulateur d'écosystème")
        screen = pygame.display.set_mode((LARGEUR,HAUTEUR))
        screen.fill((226, 226, 226))

        """ Création puis affichage du menu et de la fenêtre principal servant
                à afficher l'écosystème
        """
        parametres = parametres.Parametres()
        simulateur = Simulateur(*parametres.entites_depart)
        frame = FenetrePrincipale(simulateur, LARGEUR - LARGEUR_MENU-10, HAUTEUR-10)
        menu = Menu(LARGEUR_MENU, HAUTEUR, simulateur)
        
        menu.draw(screen)
        frame.rect = frame.rect.move((LARGEUR_MENU+5, 5))
        frame.draw(screen, menu.classes_affichees)
        pygame.display.flip()

        """ Boucle principale du programme
        """

        curseur = 0

        while True:

                """ Traitement des évènements pygame
                """
                if pygame.event.peek(pygame.MOUSEMOTION):
                        """ Si il y'a plusieurs events de mouvement de souris,
                                on ne s'intéresse qu'au dernier, car seul l'endroit
                                où se trouve la souris au moment où gérer l'affichage
                                est intéressant, tous les autres endroits par lesquels
                                elle est passé ne changent rien.
                        """
                        event = pygame.event.get(pygame.MOUSEMOTION)[-1]
                        pygame.event.clear(pygame.MOUSEMOTION)
                        if menu.rect.collidepoint(event.pos):
                                """ Si la souris est sur la surface du menu,
                                        envoie directement l'event au menu
                                """
                                menu.events(event)
                        if menu.interactions.interaction_clic:
                                """ Si le bouton pour supprimer des entités
                                        est enfoncé, change le curseur de la
                                        souris si elle se trouve sur la carte
                                """
                                if curseur == 0:
                                        if frame.fenetre == 1 and frame.ecosysteme.rect.collidepoint(frame.position_relative(event.pos)):
                                                pygame.mouse.set_cursor(*menu.interactions.curseur)
                                                curseur = 1
                                elif curseur == 1:
                                        if not frame.fenetre == 1 or not frame.ecosysteme.rect.collidepoint(frame.position_relative(event.pos)):
                                                pygame.mouse.set_cursor(*CURSEUR_BASE)
                                                curseur=0
                        
                for event in pygame.event.get():

                        """ On traite d'abord ici les events pygame de base,
                                les events de clic de souris.
                        """
                        
                        if event.type == pygame.MOUSEBUTTONUP:
                                """ Seul le menu exploite les events lorsque
                                        le bouton de souris est relâché. L'event
                                        est donc envoie au menu qui le gère
                                        lui-même l'event
                                """
                                menu.events(event)
                        if event.type == pygame.MOUSEBUTTONDOWN:
                                if menu.rect.collidepoint(event.pos):
                                        """ Envoie l'event au menu si le clic se
                                                trouve sur sa surface
                                        """
                                        menu.events(event)
                                elif frame.onglet_rect.collidepoint(frame.position_relative(event.pos)):
                                        """ Lorsqu'un clic est effectué sur les onglets
                                                l'event est gérer par la fenêtre permettant
                                                l'affichage de l'écosystème
                                        """
                                        frame.event(event)
                                        frame.draw(screen, menu.classes_affichees)
                                elif menu.interactions.interaction_clic and frame.fenetre == 1 and frame.ecosysteme.rect.collidepoint(frame.position_relative(event.pos)):
                                        """ Gère les interactions lorsqu'on clique sur la carte
                                        """
                                        pos = frame.ecosysteme.position_ecosysteme(frame.position_relative(event.pos))
                                        liste = menu.interactions.interaction_clic(pos)
                                        frame.ecosysteme.del_sprites(liste)
                                        frame.draw(screen, menu.classes_affichees)
                                        menu.stats.update()
                                        
                                        
                        if event.type == pygame.QUIT:
                                pygame.quit()
                                sys.exit()

                        """ On traite ensuite ici les events personnalisés,
                                qui ont été envoyés lors de l'activation
                                d'un bouton
                        """

                        if event.type == PAUSE:
                                """ Event permettant de mettre en
                                        pause/reprendre la simulation
                                """
                                menu.event_pause()

                        if event.type == REINITIALISER:
                                """ Réinitialiser la simulation en recréant une
                                nouvelle simulation. Affiche le nouvel écosystème
                                et met en pause la simulation """
                                if not menu.pause:
                                        menu.event_pause()
                                simulateur = Simulateur(*parametres.entites_depart)
                                frame.reinitialiser(simulateur)
                                frame.draw(screen, menu.classes_affichees)
                                menu.event_reinit(simulateur)

                        if event.type == AFFICHAGE_CLASSE:
                                """ Event permettant de gérer les classes
                                        à afficher dans l'écosystème
                                """
                                menu.event_affichage(event.classe)
                                frame.draw(screen, menu.classes_affichees)

                        if event.type == PARAMETRES:
                                """ Event pour la modification des
                                        paramètres de l'écosystème.
                                """
                                parametres.modifier_parametres()

                        if event.type == INTERACTION_OPTIONS:
                                """ Modifications des options des
                                        interactions
                                """
                                menu.interactions.modifier_options(event)

                        if event.type == INTERACTION:
                                """ Gestion des interactions entre l'utilisateur
                                        et l'écosystème.
                                """
                                
                                l = event.fonction(taille_pixel = frame.ecosysteme.taille_pixel)
                                frame.ecosysteme.add_sprites(l)
                                frame.draw(screen, menu.classes_affichees)
                                menu.stats.update()

                
                """ Met à jour l'affichage de la fenêtre
                """
                
                menu.update()
                menu.draw(screen)
                                
                if(not menu.pause):
                        """ Continue la simulation si elle n'est pas en pause et
                                affiche l'écosystème.
                        """
                        frame.update()
                        frame.draw(screen, menu.classes_affichees)

                pygame.display.flip()
        
