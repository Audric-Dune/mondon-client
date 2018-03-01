# !/usr/bin/env python
# -*- coding: utf-8 -*-

from commun.ui.public.mondon_widget import MondonWidget


class Refente(MondonWidget):

    def __init__(self, parent=None, code=0, code_perfo=0, dec=0,
                 laize1=0, laize2=0, laize3=0, laize4=0, laize5=0, laize6=0, laize7=0):
        super(Refente, self).__init__(parent=parent)
        self.code = code
        self.code_perfo = code_perfo
        self.dec = dec
        self.laize1 = laize1
        self.laize2 = laize2
        self.laize3 = laize3
        self.laize4 = laize4
        self.laize5 = laize5
        self.laize6 = laize6
        self.laize7 = laize7

    def __str__(self):
        return "REFENTE{} / PERFO{} : DEC{}, {}, {}, {}, {}, {}, {}, {}".format(self.code,
                                                                                self.code_perfo,
                                                                                self.dec,
                                                                                self.laize1,
                                                                                self.laize2,
                                                                                self.laize3,
                                                                                self.laize4,
                                                                                self.laize5,
                                                                                self.laize6,
                                                                                self.laize7)
