# !/usr/bin/env python
# -*- coding: utf-8 -*-


class BobineFille:

    def __init__(self,
                 code=0,
                 name="",
                 laize=0.,
                 lenght=0,
                 color="",
                 stock=0,
                 stock_therme=0,
                 creation_time=0,
                 codes_cliche=None,
                 colors_cliche=None,
                 gr=0,
                 poses=None,
                 sommeil=False):
        self.name = name
        self.code = code
        self.codes_cliche = codes_cliche
        self.colors_cliche = colors_cliche
        self.laize = float(laize)
        self.lenght = int(lenght)
        self.color = color
        self.stock = stock
        self.stock_therme = stock_therme
        self.creation_time = creation_time
        self.gr = gr
        self.poses = poses if poses else [0]
        self.sommeil = sommeil
        self.vente_annuelle = None

    def update_bobine_from_cliche(self):
        if self.codes_cliche:
            for code_cliche in self.codes_cliche:
                poses_and_colors = self.get_poses_and_colors_from_code_cliche(code_cliche)
                if poses_and_colors:
                    self.poses = poses_and_colors[0]
                    if self.colors_cliche:
                        self.colors_cliche += poses_and_colors[1]
                    else:
                        self.colors_cliche = poses_and_colors[1]

    @staticmethod
    def get_poses_and_colors_from_code_cliche(code_cliche):
        from commun.stores.cliche_store import cliche_store
        for cliche in cliche_store.cliches:
            if cliche.code == code_cliche:
                return cliche.poses, cliche.colors

    def get_value(self, value_name):
        if value_name == "code":
            return self.code
        if value_name == "laize":
            return self.laize
        if value_name == "lenght":
            return self.lenght
        if value_name == "color":
            return self.color
        return 0

    def __str__(self):
        return "B{} ({}, {}, {}m, {} poses, {}, {}), {}g, {}".format(self.code,
                                                                         self.color,
                                                                         self.laize,
                                                                         self.lenght,
                                                                         self.poses,
                                                                         self.codes_cliche,
                                                                         self.colors_cliche,
                                                                         self.gr,
                                                                         self.sommeil)
