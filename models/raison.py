# !/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtCore import QObject


class Raison(QObject):
    def __init__(self, raison_data):
        super(Raison, self).__init__(None)
        self.id = raison_data[0]
        self.start = raison_data[1]
        self.type = raison_data[2]
        self.raison = raison_data[3]
        self.duree = raison_data[4] or "NULL"
