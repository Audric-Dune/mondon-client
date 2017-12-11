# !/usr/bin/env python
# -*- coding: utf-8 -*-

import random

from PyQt5.QtCore import QObject, pyqtSignal
from lib.base_de_donnee import Database
from constants.param import LIST_CHOIX_RAISON_PREVU, LIST_CHOIX_RAISON_IMPREVU
from models.raison import Raison


class Arret(QObject):
    # Création du signal qui indique que le type d'arret selectionné a changé
    ARRET_TYPE_CHANGED_SIGNAL = pyqtSignal()
    # Création du signal qui indique qu'il y a une modification sur la sélection des raisons
    ARRET_RAISON_CHANGED_SIGNAL = pyqtSignal()

    """
    Object model qui stocke des information sur un arret
    S'occupe de modifier la base de donnée si besoin
    """
    def __init__(self, arret_data):
        super(Arret, self).__init__(None)
        self.start = arret_data[0]
        self.end = arret_data[1]
        self.raisons = []
        self.type_cache = None
        self.raison_cache_index = {}
        self.create_on_database()

    def create_on_database(self):
        """
        S'occupe de créer l'arret en base de donnée
        """
        Database.create_arret(start_arret=self.start, end_arret=self.end)

    def update_arret(self):
        """
        S'occupe de mettre a jours l'arret en base de donnée
        """
        Database.update_arret(start_arret=self.start, end_arret=self.end)

    def add_raison_on_database(self):
        """
        Est appelé lorsque l'on click sur ajouter dans la window arret
        S'occupe de créer les objects raisons
        """
        # On parcour tous les index sélectionner
        for index, value_item in self.raison_cache_index.items():
            # On génère un id aléatoire
            random_id = random.randint(0, 1e15)
            # Le dictionnaire raison_cache_index contient en clé l'index et en valeur
            # la valeur de la dropdown sélectionné (ou None si c'est pas une dropdown)
            # Si il y a une valeur dans value item
            if value_item:
                # La raison est la valeur de l'item
                raison_arret = value_item
            # Sinon on sélectionne la liste des arrets en fonction du type d'aret
            else:
                list_raison = LIST_CHOIX_RAISON_PREVU if self.type_cache == "Prévu" else LIST_CHOIX_RAISON_IMPREVU
                # On récupère la valeur de l'index dans la liste
                raison_arret = list_raison[index][1]
            # On range les données définient ci-dessus
            data_raison = [random_id, self.start, self.type_cache, raison_arret, None]
            # On crée notre object raison
            self.raisons.append(Raison(data_raison))
        self.raisons = self.raison_store(self.raisons)

    @staticmethod
    def raison_store(raisons):
        list_raison = []
        list_raison_not_imprevu = []
        list_raison_not_prevu = []
        for raison in raisons:
            if raison.type == "Imprévu":
                list_raison.append(raison)
            else:
                list_raison_not_imprevu.append(raison)
        for raison in list_raison_not_imprevu:
            if raison.type == "Prévu":
                list_raison.append(raison)
            else:
                list_raison_not_prevu.append(raison)
        for raison in list_raison_not_prevu:
            list_raison.append(raison)
        return list_raison

    def add_type_cache(self, type):
        """
        Garde en mémoire le type sélectionné
        :param type: Le type sélectionné
        """
        self.type_cache = type
        # Emet un signal lorsque le type d'arret change
        self.ARRET_TYPE_CHANGED_SIGNAL.emit()

    def add_raison_cache(self, index_raison, text_dropdown):
        """
        Stock les raisons sélectionnées dans un tableau
        :param index_raison: l'index de la raison sélectionné
        :param text_dropdown: La valeur de la dropdown ou None si ce n'est pas une dropdown
        """
        self.raison_cache_index[index_raison] = text_dropdown
        # Emet un signal qui indique qu'il y a une modification sur la sélection des raisons
        self.ARRET_RAISON_CHANGED_SIGNAL.emit()

    def remove_raison_cache(self, index_raison=None):
        """
        Supprime l'index du tableau des indexs sélectionnés lorsqu'on le déselectionne
        :param index_raison: Index a supprimer
        """
        if index_raison and self.raison_cache_index:
            del self.raison_cache_index[index_raison]
        else:
            self.raison_cache_index = {}

    def remove_type(self):
        """
        Reinitialise le type d'arret sélectionné
        """
        self.type_cache = None

    def remove_raison(self, raison):
        """
        Supprime l'object du tableau des raisons
        """
        # On parcour la liste des objects raisons
        for object_raison in self.raisons:
            # On regarde si la raison de l'object = la raison recherché
            if object_raison.raison == raison:
                object_raison.del_raison_on_database()
                self.raisons.remove(object_raison)
                object_raison.deleteLater()
                break
