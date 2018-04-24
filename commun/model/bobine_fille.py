# !/usr/bin/env python
# -*- coding: utf-8 -*-

from commun.ui.public.mondon_widget import MondonWidget


class BobineFille(MondonWidget):

    def __init__(self, parent=None,
                 code=0,
                 name="",
                 laize=0,
                 lenght=0,
                 color="",
                 alerte=False,
                 cliche_id_1=None,
                 cliche_id_2=None,
                 stock=0,
                 stock_therme=0,
                 creation_time="",
                 gr=0,
                 poses=None,
                 pose=None,
                 sommeil=False):
        super(BobineFille, self).__init__(parent=parent)
        self.name = name
        self.code = code
        self.laize = float(laize)
        self.lenght = int(lenght)
        self.color = color
        self.cliche_id_1 = cliche_id_1
        self.cliche_id_2 = cliche_id_2
        self.stock = stock
        self.stock_therme = stock_therme
        self.creation_time = creation_time
        self.alert = alerte
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
        if value_name == "alert":
            return self.alert
        if value_name == "pose":
            return self.pose
        return 0

    def __str__(self):
        return "B{}({}, {}, {}m, {} poses, {}, {}, {})".format(self.code,
                                                               self.color.capitalize(),
                                                               self.laize,
                                                               self.lenght,
                                                               self.pose,
                                                               self.gr,
                                                               self.alert,
                                                               self.sommeil)
