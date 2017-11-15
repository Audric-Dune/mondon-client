# !/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtCore import QObject
from lib.base_de_donnee import Database


class Arret(QObject):
    def __init__(self, arret_data):
        super(Arret, self).__init__(None)
        self.start = arret_data[0]
        self.end = arret_data[1]
        self.raisons = []
        self.create_on_database()

    def create_on_database(self):
        Database.create_arret(start_arret=self.start, end_arret=self.end)

    def update_arret(self):
        Database.update_arret(start_arret=self.start, end_arret=self.end)
