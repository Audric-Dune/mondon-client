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
        self.length = bobine.length
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

    def get_value(self, value_name):
        if value_name == "code":
            return self.code
        if value_name == "laize":
            return self.laize
        if value_name == "length":
            return self.length
        if value_name == "color":
            return self.color
        if value_name == "gr":
            return self.gr
        if value_name == "stock":
            return self.stock
        if value_name == "stock_therme":
            return self.stock_therme
        if value_name == "vente_mensuelle":
            return self.vente_mensuelle
        return 0

    def __repr__(self):
        return 'B({}, {}, {}, {}, {}, {})'.format(self.code, self.laize, self.pose, self.color, self.gr, self.length)

    def __lt__(self, other):
        return self.pose < other.pose if self.code == other.code else self.code < other.code

    def __hash__(self):
        h = hash('{}({})'.format(self.code, self.pose))
        return h
