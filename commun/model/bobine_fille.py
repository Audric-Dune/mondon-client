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
                 code_cliche=None,
                 gr=0,
                 poses=None,
                 pose=None,
                 sommeil=False):
        self.name = name
        self.code = code
        self.code_cliche = code_cliche
        self.laize = float(laize)
        self.lenght = int(lenght)
        self.color = color
        self.stock = stock
        self.stock_therme = stock_therme
        self.creation_time = creation_time
        self.gr = gr
        self.poses = poses if poses else [0]
        self.pose = pose
        self.sommeil = sommeil

    def get_value(self, value_name):
        if value_name == "code":
            return self.code
        if value_name == "laize":
            return self.laize
        if value_name == "lenght":
            return self.lenght
        if value_name == "color":
            return self.color
        if value_name == "pose":
            return self.pose
        return 0

    def __copy__(self):
        return BobineFille(self.code,
                           self.name,
                           self.laize,
                           self.lenght,
                           self.color,
                           self.stock,
                           self.stock_therme,
                           self.creation_time,
                           self.gr,
                           self.poses,
                           self.pose,
                           self.sommeil)

    def __str__(self):
        return "B{}({}, {}, {}m, {} poses, {}, {}, {})".format(self.code,
                                                               self.color.capitalize(),
                                                               self.laize,
                                                               self.lenght,
                                                               self.pose,
                                                               self.gr,
                                                               self.alert,
                                                               self.sommeil)
