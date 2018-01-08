# !/usr/bin/env python
# -*- coding: utf-8 -*-

import random

from PyQt5.QtCore import QObject, pyqtSignal
from lib.base_de_donnee import Database
from constants.param import LIST_CHOIX_RAISON_PREVU, LIST_CHOIX_RAISON_IMPREVU, LIST_CHOIX_ENTRETIEN
from models.raison import Raison


class Arret(QObject):
    # Création du signal qui indique que le type d'arret selectionné a changé
    ARRET_TYPE_CHANGED_SIGNAL = pyqtSignal()
    # Création du signal qui indique qu'il y a une modification sur la sélection des raisons
    ARRET_RAISON_CHANGED_SIGNAL = pyqtSignal()

    """
    Object model qui stocke des informations sur un arret
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
        self.get_raisons()

    def create_on_database(self):
        """
        S'occupe de créer l'arret en base de donnée
        Vérifie si l'arrêt est déja présent en base de donnée
        """
        Database.create_arret(start_arret=self.start, end_arret=self.end)

    def update_arret(self):
        """
        S'occupe de mettre a jours l'arret en base de donnée
        """
        Database.update_arret(start_arret=self.start, end_arret=self.end)

    def get_raisons(self):
        list_raisons = Database.get_raison(self.start, self.end)
        # On parcour les raisons de la base de donnée
        for raison in list_raisons:
            start_raison = raison[1]
            id_raison = raison[0]
            # Test si le start de la raison correspond au start de l'arret
            if start_raison == self.start:
                # Test si la raison est déja renseigné dans la liste des raisons
                if self.check_id_raison(id_raison):
                    # Si oui on ne fait rien
                    continue
                else:
                    # Sinon on crée un models raison est on l'insert dans le tableau de raison de l'arret
                    raison_object = Raison(raison)
                    self.raisons.append(raison_object)
                self.raison_store()

    def check_id_raison(self, id):
        """
        Permet de checker si une raison est déja présente dans le tableau de raison d'un arret
        :param arret_object: Object arret ou l'on test
        :param id: Id que l'on recherche dans l'arret
        :return: True si la raison est présente, False si on ne l'a trouve pas
        """
        for raison in self.raisons:
            raison_id = raison.id
            if raison_id == id:
                return True
        return False

    def add_commentaire_on_database(self, commentaire):
        # On génère un id aléatoire
        random_id = random.randint(0, 1e15)
        Database.create_raison_arret(
            id=random_id,
            start_arret=self.start,
            type_arret="Commentaire",
            raison_arret=commentaire,
            primaire=0)

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
                list_raison = self.select_list_raison()
                # On récupère la valeur de l'index dans la liste
                raison_arret = list_raison[index][1]
            # On range les données définient ci-dessus
            data_raison = [random_id, self.start, self.type_cache, raison_arret, None]
            # On crée notre object raison
            self.raisons.append(Raison(data_raison))
        self.raison_store()

    def select_list_raison(self):
        if self.type_cache == "Prévu":
            return LIST_CHOIX_RAISON_PREVU
        elif self.type_cache == "Imprévu":
            return LIST_CHOIX_RAISON_IMPREVU
        else:
            return LIST_CHOIX_ENTRETIEN

    def raison_store(self):
        # On détermine la raison primaire
        raison_primaire = None
        for raison in self.raisons:
            if raison.primaire == 1:
                raison_primaire = raison
        # On détermine le type principal
        type_primaire = None
        for raison in self.raisons:
            if raison.type == "Imprévu":
                type_primaire = "Imprévu"
                break
            elif raison.type == "Prévu" and type_primaire != "Imprévu":
                type_primaire = "Prévu"
            elif raison.type == "Entretien" and not type_primaire:
                type_primaire = "Entretien"
        # On remove la raison primaire si le type de la raison primaire et le type primaire ne corresponde pas
        if raison_primaire:
            if raison_primaire.type != type_primaire:
                raison_primaire.remove_to_raison_primaire()
        # On commence le trie des raisons
        list_raison = []
        list_raison_not_primaire = []
        list_raison_not_imprevu = []
        list_raison_not_prevu = []
        # On parcour l'ensemble des raisons pour trouver la raison principale si il y en a une
        for raison in self.raisons:
            if raison.primaire == 1:
                list_raison.append(raison)
            else:
                list_raison_not_primaire.append(raison)
        # Ensuite on parcour les raisons restante est on les tries dans l'ordre imprevu puis prevu puis entretien
        for raison in list_raison_not_primaire:
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
        self.raisons = list_raison

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
        if index_raison and self.raison_cache_index.get(index_raison):
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
