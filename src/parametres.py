""" Ce module contient la classe Parametres permettant de charger,
    sauvegarder, et modifier les paramètres de l'écosystème via
    une interface graphique Tkinter. Tkinter est ici utilisé
    car beaucoup plus pratique que Pygame pour un rendu propre
    beaucoup plus facilement, sans avoir à créer chaque widget ect ...,
    gérer les entrées claviers bien plus facilement. L'intérêt de Pygame
    par rapport à Tkinter dans le reste du programme est exclusivement
    pour des questions de performances qui ne sont aucunement nécessaires
    dans ce cas là.
 """

import copy
import os
import json
import tkinter as tk
import tkinter.messagebox
from tkinter import ttk
from simulateur import *
from parametres_defaut import *
import pygame.locals

CLASSES = {"petit_herbivore": PetitHerbivore, "grand_herbivore": GrandHerbivore, "petit_carnivore": PetitCarnivore, "grand_carnivore": GrandCarnivore, "vegetation": Vegetation}

cibles = ["Petit herbivore", "Grand herbivore", "Petit carnivore", "Grand carnivore", "Aléatoire"]


class Parametres:

        # Dossier et fichier contenant les paramètres
        dossier = "./"
        fichier = "config.json"

        def __init__(self):
                """ Constructeur de la classe """
                
                """ Charge les paramètres enregistrés
                    et crée le fichier s'il n'existe pas
                """
                if self.fichier in os.listdir(self.dossier):
                        fichier = open(self.dossier + self.fichier, "r")
                        self.liste_configs = json.load(fichier)
                        if "defaut" in self.liste_configs.keys():
                                self.config = copy.deepcopy(self.liste_configs["defaut"])
                        else:
                                self.config = copy.deepcopy(PARAMETRES_DEFAUT)
                                self.liste_configs["defaut"] = copy.deepcopy(self.config)
                                fichier = open(self.dossier + self.fichier, "w")
                                fichier.write(json.dumps(self.liste_configs, indent = 8))
                else:
                        self.config = copy.deepcopy(PARAMETRES_DEFAUT)
                        self.liste_configs = {"defaut": self.config}
                        fichier = open(self.dossier + self.fichier, "w")
                        fichier.write(json.dumps(self.liste_configs, indent = 8))
                fichier.close()
                
                """ L'attribut tkvars contient les variables Tkinter
                    correspondant à chacun des paramètres
                """
                self.tkvars = {} 
                
                self.appliquer_parametres(self.config)

        def fenetre_sauvegarder(self):
                """ Ouvre la fenêtre permettant de sauvegarder
                    une configuration
                """
                self.nom = tk.StringVar()
                fen2 = tk.Toplevel()
                self.fenetre2 = fen2
                fen2.title("Enregister la configuration")
                tk.Label(fen2, text = "Nom de la configuration").grid(row=0, columnspan=2)
                tk.Entry(fen2, textvariable=self.nom).grid(row=1, columnspan=2)
                
                tk.Button(fen2, text="Confirmer", command=self.sauvegarder_config).grid(row=2, column=0, pady=5)
                tk.Button(fen2, text="Annuler", command=fen2.destroy).grid(row=2, column=1, pady=5)
                fen2.mainloop()

        def sauvegarder_config(self):
                """ Sauvegarde dans le fichier json la
                    configuration
                """
                nom = self.nom.get()
                if nom in self.liste_configs.keys():
                        if not tk.messagebox.askyesnocancel("resef", "Ce nom est déjà utilisé pour une autre configuration. Voulez-vous l'écraser ?"):
                                return
                for c in self.config.keys():
                        for p in self.config[c].keys():
                                self.config[c][p] = self.tkvars[c][p].get()
                self.liste_configs[nom] = copy.deepcopy(self.config)
                fichier = open(self.dossier + self.fichier, "w")
                fichier.write(json.dumps(self.liste_configs, indent = 8))
                fichier.close()
                self.fenetre2.destroy()

        def fenetre_charger(self):
                """ Ouvre la fenêtre permettant de charger
                    une configuration
                """
                fen2 = tk.Toplevel()
                self.fenetre2 = fen2
                fen2.title("Charger une configuration")
                tk.Label(fen2, text = "Nom de la configuration").grid(row=0, columnspan=2)
                self.liste_charger = tk.Listbox(fen2)
                self.liste_charger.grid(row=1, columnspan=2)
                index = 0
                for nom in self.liste_configs.keys():
                        self.liste_charger.insert(index, nom)
                        index+=1
                tk.Button(fen2, text="Confirmer", command=self.charger_config).grid(row=2, column=0, pady=5)
                tk.Button(fen2, text="Annuler", command=fen2.destroy).grid(row=2, column=1, pady=5)
                fen2.mainloop()

        def charger_config(self):
                """ Modifie toutes les variables Tkinter
                    pour leurs appliquer la configuration
                    chargée
                """
                nom = self.liste_charger.get(self.liste_charger.curselection())
                self.config = copy.deepcopy(self.liste_configs[nom])
                for c in self.tkvars.keys():
                        for p in self.tkvars[c].keys():
                                self.tkvars[c][p].set(self.config[c][p])
                self.fenetre2.destroy()

        def appliquer_parametres(self, config):
                """ Applique tous les paramètres à la simulation
                """
                for classe in ["petit_herbivore", "grand_herbivore", "petit_carnivore", "grand_carnivore"]:
                        for param in ["esperance_vie", "delai_reproduction", "age_reproduction", "perte_energie"]:
                                setattr(CLASSES[classe], param, config[classe][param])
                for param in ["quantite_max", "croissance_min", "croissance_max", "croissance_fixe"]:
                        setattr(Vegetation, param, config["vegetation"][param])
                if config["vegetation"]["type_croissance"] == "Aléatoire":
                        Vegetation.croissance_type_alea = True
                else:
                        Vegetation.croissance_type_alea = False

                for param in ["largeur_carte", "hauteur_carte"]:
                        setattr(Carte, param, config["carte"][param])
                self.entites_depart = [self.config["general"][k] for k in self.config["general"].keys()]
                
                
        def set_tkvars(self):
                """ Change la valeur de toutes les variables
                    Tkinter pour leurs mettre la valeur de la
                    configuration actuelle
                """
                for c in self.config.keys():
                        self.tkvars[c] = {}
                        for p in self.config[c].keys():
                                if p == "type_croissance":
                                        self.tkvars[c][p] = tk.StringVar()
                                elif c == "carte" or c=="general":
                                        self.tkvars[c][p] = tk.IntVar()
                                else:
                                        self.tkvars[c][p] = tk.DoubleVar()
                                self.tkvars[c][p].set(self.config[c][p])

        def save_tkvars(self):
                """ Fonction appelée lorsque clique sur le bouton
                    Confirmer pour appliquer les paramètres.
                    Met toutes les valeurs des variables Tkinter
                    à l'attribut config de la classe
                """
                for c in self.config.keys():
                        for p in self.config[c].keys():
                                self.config[c][p] = self.tkvars[c][p].get()
                self.fenetre.destroy()

        def set_default(self):
                """ Fonction appelée lorsque sur le bouton Par défaut
                    Met toutes les variables Tkinter avec
                    les paramètres par défaut de l'écosystème
                """
                for c in self.tkvars.keys():
                        for p in self.tkvars[c].keys():
                                self.tkvars[c][p].set(PARAMETRES_DEFAUT[c][p])

        def modifier_parametres(self):
                """ Ouvre la fenêtre Tkinter permettant de
                    modifier les paramètres de l'écosystème
                """
                fenetre = tk.Tk()
                self.fenetre = fenetre
                self.set_tkvars()

                
                fenetre.title("Paramètres")

                """ On utilise le widget Notebook pour diviser les
                    différents paramètres en plusieurs onglets
                    bien plus facilement
                """
                notebook = ttk.Notebook(fenetre)
                notebook.grid(columnspan = 3, pady=5, padx=10)
                
                """ On ajoute les onglets un par un, et puis on leurs
                    ajoute les paramètres que l'ont peut modifier un
                    par un ... Redondant, mais pas tant que ça de
                    moyens plus efficaces ...
                """
                # Paramètres pour le nombre d'entités initial
                general = tk.Frame(notebook)
                notebook.add(general, text="Général")
                entites_depart = tk.LabelFrame(general, text = "Nombre d'entités de départ")
                tk.Label(entites_depart, text = "Nombre de petits herbivores").grid(row=1, column=1, pady=10, stick=tk.E)
                tk.Spinbox(entites_depart, textvariable = self.tkvars["general"]["nombre_petit_herbivore"]).grid(row=1, column=2, pady=10)
                tk.Label(entites_depart, text = "Nombre de grands herbivores").grid(row=2, column=1, pady=10, stick=tk.E)
                tk.Spinbox(entites_depart, textvariable = self.tkvars["general"]["nombre_grand_herbivore"]).grid(row=2, column=2, pady=10)
                tk.Label(entites_depart, text = "Nombre de petits carnivores").grid(row=3, column=1, pady=10, stick=tk.E)
                tk.Spinbox(entites_depart, textvariable = self.tkvars["general"]["nombre_petit_carnivore"]).grid(row=3, column=2, pady=10)
                tk.Label(entites_depart, text = "Nombre de grands carnivores").grid(row=4, column=1, pady=10, stick=tk.E)
                tk.Spinbox(entites_depart, textvariable = self.tkvars["general"]["nombre_grand_carnivore"]).grid(row=4, column=2, pady=10)
                entites_depart.pack(padx=10, pady=5, fill=tk.X)
                

                # Paramètres de la carte et de la végétation
                carte = tk.Frame(notebook)
                notebook.add(carte, text="Carte")
                # Carte
                params_carte = tk.LabelFrame(carte, text = "Carte")
                tk.Label(params_carte, text = "Hauteur de la carte").grid(row=1, column=1, pady=10, stick=tk.E)
                tk.Spinbox(params_carte, textvariable = self.tkvars["carte"]["hauteur_carte"]).grid(row=1, column=2, pady=10)
                tk.Label(params_carte, text = "Largeur de la carte").grid(row=2, column=1, pady=10, stick=tk.E)
                tk.Spinbox(params_carte, textvariable = self.tkvars["carte"]["largeur_carte"]).grid(row=2, column=2, pady=10)
                params_carte.pack(padx=10, pady=5, fill=tk.X)

                # Végétation
                vegetation = tk.LabelFrame(carte, text = "Végétation")
                tk.Label(vegetation, text = "Quantité maximum de végétation").grid(row=1, column=1, pady=10, stick=tk.E)
                tk.Spinbox(vegetation, textvariable = self.tkvars["vegetation"]["quantite_max"]).grid(row=1, column=2, pady=10)
                tk.Label(vegetation, text = "Type de croissance").grid(row=2, column=1, pady=10, stick=tk.E)
                tk.OptionMenu(vegetation, self.tkvars["vegetation"]["type_croissance"], "Aléatoire", "Fixe").grid(row=2, column=2, pady=10)
                tk.Label(vegetation, text = "Croissance par itération (si croissance fixe)").grid(row=3, column=1, pady=10, stick=tk.E)
                tk.Spinbox(vegetation, textvariable = self.tkvars["vegetation"]["croissance_fixe"]).grid(row=3, column=2, pady=10)
                tk.Label(vegetation, text = "Croissance maximum par itération").grid(row=4, column=1, pady=10, stick=tk.E)
                tk.Spinbox(vegetation, textvariable = self.tkvars["vegetation"]["croissance_max"]).grid(row=4, column=2, pady=10)
                tk.Label(vegetation, text = "Croissance minimum par itération").grid(row=5, column=1, pady=10, stick=tk.E)
                tk.Spinbox(vegetation, textvariable = self.tkvars["vegetation"]["croissance_min"]).grid(row=5, column=2, pady=10)
                vegetation.pack(padx=10, pady=5, fill=tk.X)

                # Paramètres pour les herbivores
                herbivores = tk.Frame(notebook)
                notebook.add(herbivores, text="Herbivores")
                petit_herbivore = tk.LabelFrame(herbivores, text="Petits herbivores")
                grand_herbivore = tk.LabelFrame(herbivores, text="Grands herbivores")
                
                # Paramètres pour les carnivores
                carnivores = tk.Frame(notebook)
                notebook.add(carnivores, text="Carnivores")
                petit_carnivore = tk.LabelFrame(carnivores, text="Petits carnivores")
                grand_carnivore = tk.LabelFrame(carnivores, text="Grands carnivores")

                """ On ajoute tous les widgets pour les entités 
                    autres que la végétation
                """
                d = {"petit_herbivore": petit_herbivore, "grand_herbivore":grand_herbivore, "petit_carnivore":petit_carnivore, "grand_carnivore":grand_carnivore}
                for k in d.keys():
                        tk.Label(d[k], text = "Espérance de vie").grid(row=1, column=1, pady=10, stick=tk.E)
                        tk.Spinbox(d[k], textvariable = self.tkvars[k]["esperance_vie"]).grid(row=1, column=2, pady=10)
                        tk.Label(d[k], text = "Perte d'énergie par itération").grid(row=2, column=1, pady=10, stick=tk.E)
                        tk.Spinbox(d[k], textvariable = self.tkvars[k]["perte_energie"]).grid(row=2, column=2, pady=10)
                        tk.Label(d[k], text = "Délai entre deux reproductions").grid(row=3, column=1, pady=10, stick=tk.E)
                        tk.Spinbox(d[k], textvariable = self.tkvars[k]["delai_reproduction"]).grid(row=3, column=2, pady=10)
                        tk.Label(d[k], text = "Age minimal de reproduction").grid(row=4, column=1, pady=10, stick=tk.E)
                        tk.Spinbox(d[k], textvariable = self.tkvars[k]["age_reproduction"]).grid(row=4, column=2, pady=10)
                        d[k].pack(padx=10,pady=5, fill=tk.X)

                """ On crée les deux boutons de menu en haut de l'écran
                    pour sauvegarder ou charger une configuration
                """
                menu = tk.Menu(fenetre)
                fenetre["menu"] = menu
                menu.add_command(label="Sauvegarder la configuration", command=self.fenetre_sauvegarder)
                menu.add_command(label="Charger une configuration", command=self.fenetre_charger)

                """ On ajoute les trois boutons pour appliquer les
                    modifications, les annuler, ou mettre la config
                    par défaut
                """
                tk.Button(fenetre, text="Confirmer", command=self.save_tkvars).grid(row=1, column=1, pady=5)
                tk.Button(fenetre, text="Annuler", command=fenetre.destroy).grid(row=1, column=2, pady=5)
                tk.Button(fenetre, text="Par défaut", command=self.set_default).grid(row=1, column=0, pady=5)
                
                
                fenetre.mainloop()
                self.appliquer_parametres(self.config)
