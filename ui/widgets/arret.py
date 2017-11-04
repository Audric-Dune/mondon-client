# !/usr/bin/env python
# -*- coding: utf-8 -*-

from ui.widgets.mondon_widget import MondonWidget
from lib.base_de_donnee import Database


class Arret(MondonWidget):
    def __init__(self, arret_data):
        super(Arret, self).__init__(None)
        self.start = arret_data[0]
        self.end = arret_data[1]
        self.type = arret_data[2] or "NULL"
        self.raison = arret_data[3] or "NULL"
        self.create_on_database()

    def create_on_database(self):
        Database.create_arret(start_arret=self.start, end_arret=self.end)

    def update_arret(self):
        Database.update_arret(start_arret=self.start,
                              end_arret=self.end,
                              type_arret=self.type,
                              raison_arret=self.raison)