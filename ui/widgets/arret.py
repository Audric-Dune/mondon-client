# !/usr/bin/env python
# -*- coding: utf-8 -*-

from ui.widgets.mondon_widget import MondonWidget
from lib.base_de_donnee import Database


class Arret(MondonWidget):
    def __init__(self, arret_data):
        super(Arret, self).__init__()
        self.start = arret_data[0]
        self.end = arret_data[1]
        self.type = arret_data[2]
        self.raison = arret_data[3]
        self.dechet = []

    def save_on_base_de_donnee(self):
        Database.save_arret(start=self.start, end=self.end, type=self.type, raison=self.raison)
        for dechet in self.dechet:
            dechet.save_on_base_de_donnee()
