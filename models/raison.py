# !/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtCore import QObject
from lib.base_de_donnee import Database


class Raison(QObject):
    def __init__(self, raison_data):
        super(Raison, self).__init__(None)
        self.id = raison_data[0]
        self.start = raison_data[1]
        self.type = raison_data[2]
        self.raison = raison_data[3]
        self.primaire = raison_data[4] or "0"
        self.add_raison_on_database()

    def add_raison_on_database(self):
        Database.create_raison_arret(
            id=self.id,
            start_arret=self.start,
            type_arret=self.type,
            raison_arret=self.raison,
            primaire=self.primaire)

    def del_raison_on_database(self):
        Database.delete_raison_arret(self.id)
