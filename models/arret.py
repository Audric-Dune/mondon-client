# !/usr/bin/env python
# -*- coding: utf-8 -*-

import random

from PyQt5.QtCore import QObject, pyqtSignal
from lib.base_de_donnee import Database
from constants.param import LIST_CHOIX_RAISON_PREVU, LIST_CHOIX_RAISON_IMPREVU
from models.raison import Raison


class Arret(QObject):
    ARRET_TYPE_CHANGED_SIGNAL = pyqtSignal()
    ARRET_RAISON_CHANGED_SIGNAL = pyqtSignal()

    def __init__(self, arret_data):
        super(Arret, self).__init__(None)
        self.start = arret_data[0]
        self.end = arret_data[1]
        self.raisons = []
        self.type_cache = None
        self.raison_cache_index = {}
        # self.create_on_database()

    def create_on_database(self):
        Database.create_arret(start_arret=self.start, end_arret=self.end)

    def update_arret(self):
        Database.update_arret(start_arret=self.start, end_arret=self.end)

    def add_raison_on_database(self):
        for index, raison in self.raison_cache_index.items():
            random_id = random.randint(0, 1e15)
            if raison:
                raison_arret = raison
            else:
                list_raison = LIST_CHOIX_RAISON_PREVU if self.type_cache == "Prévu" else LIST_CHOIX_RAISON_IMPREVU
                raison_arret = list_raison[index][1]
            data_raison = [random_id, self.start, self.type_cache, raison_arret, None]
            self.raisons.append(Raison(data_raison))

    def add_type_cache(self, type):
        self.type_cache = type
        self.ARRET_TYPE_CHANGED_SIGNAL.emit()

    def add_raison_cache(self, index_raison, text_dropdown):
        self.raison_cache_index[index_raison] = text_dropdown
        self.ARRET_RAISON_CHANGED_SIGNAL.emit()

    def remove_raison_cache(self, index_raison):
        del self.raison_cache_index[index_raison]

    def remove_type(self):
        self.type_cache = None

    def remove_raison(self):
        self.raison_cache_index = {}
