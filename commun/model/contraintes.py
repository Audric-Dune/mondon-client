# !/usr/bin/env python
# -*- coding: utf-8 -*-

from commun.ui.public.mondon_widget import MondonWidget


class Contrainte(MondonWidget):

    def __init__(self, parent=None,
                 bobine_poly=None,
                 perfo=None,
                 bobine_papier=None,
                 refente=None,
                 bobines_fille=None):
        super(Contrainte, self).__init__(parent=parent)
        self.bobines_poly = bobine_poly
        self.perfos = perfo
        self.bobines_papier = bobine_papier
        self.refentes = refente
        self.bobines_fille = bobines_fille if bobines_fille else []