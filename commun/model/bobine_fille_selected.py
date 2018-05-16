# !/usr/bin/env python
# -*- coding: utf-8 -*-


class BobineFilleSelected:
    def __init__(self, bobine, pose, index=None):
        self.bobine = bobine
        self.name = bobine.name
        self.code = bobine.code
        self.codes_cliche = bobine.codes_cliche
        self.colors_cliche = bobine.colors_cliche
        self.laize = bobine.laize
        self.lenght = bobine.lenght
        self.color = bobine.color
        self.stock = bobine.stock
        self.stock_therme = bobine.stock_therme
        self.creation_time = bobine.creation_time
        self.gr = bobine.gr
        self.poses = bobine.poses
        self.sommeil = bobine.sommeil
        self.index = index
        self.pose = pose
        self.vente_annuelle = bobine.vente_annuelle
        self.vente_mensuelle = bobine.vente_mensuelle
        self.etat = bobine.etat

    def __repr__(self):
        return 'B({}, {}, {}, {}, {}, {})'.format(self.code, self.laize, self.pose, self.color, self.gr, self.lenght)
