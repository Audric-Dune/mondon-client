# !/usr/bin/env python
# -*- coding: utf-8 -*-


class Contrainte:

    def __init__(self,
                 bobine_poly=None,
                 perfo=None,
                 bobine_papier=None,
                 refente=None,
                 bobines_fille=None):
        self.bobine_poly = bobine_poly
        self.perfo = perfo
        self.bobine_papier = bobine_papier
        self.refente = refente
        self.bobines_fille = bobines_fille if bobines_fille else []
