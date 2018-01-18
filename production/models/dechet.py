# !/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtCore import QObject

from commun.lib.base_de_donnee import Database


class Dechet(QObject):
    def __init__(self, dechet_data):
        super(Dechet, self).__init__()
        self.id = dechet_data[0]
        self.start_arret = dechet_data[1]
        self.type = dechet_data[2]
        self.masse = dechet_data[3]
        self.piste = dechet_data[4]
        self.couleur = dechet_data[5]
        self.grammage_papier = dechet_data[6]
        self.grammage_polypro = dechet_data[7]

    def save_on_base_de_donnee(self):
        Database.save_dechet(id=self.id,
                             arret_start=self.start_arret,
                             type=self.type,
                             masse=self.masse,
                             piste=self.piste,
                             couleur=self.couleur,
                             grammage_papier=self.grammage_papier,
                             grammage_polypro=self.grammage_polypro)
