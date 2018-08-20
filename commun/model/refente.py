# !/usr/bin/env python
# -*- coding: utf-8 -*-


class Refente:

    def __init__(self, code=0, code_perfo=0, dec=0,
                 laize1=None, laize2=None, laize3=None, laize4=None, laize5=None, laize6=None, laize7=None, chute=None):
        self.code = code
        self.code_perfo = code_perfo
        self.dec = dec
        self.laizes = [laize1, laize2, laize3, laize4, laize5, laize6, laize7]
        self.laize = self.get_laize_from_refente(self.laizes, chute)
        self.laize1 = laize1
        self.laize2 = laize2
        self.laize3 = laize3
        self.laize4 = laize4
        self.laize5 = laize5
        self.laize6 = laize6
        self.laize7 = laize7
        self.chute = chute

    @staticmethod
    def get_laize_from_refente(laizes, chute):
        laize_refente = 0
        for laize in laizes:
            if laize:
                laize_refente += laize
        laize_refente += chute if chute else 0
        return round((laize_refente/10))*10

    def get_value(self, value_name):
        if value_name == "code":
            return self.code
        if value_name == "code_perfo":
            return self.code_perfo
        if value_name == "laize":
            return self.laize
        return 0

    def __str__(self):
        return "REFENTE{} / PERFO{} : DEC{}, {}, {}, {}, {}, {}, {}, {}".format(self.code,
                                                                                self.code_perfo,
                                                                                self.dec,
                                                                                self.laizes[0],
                                                                                self.laizes[1],
                                                                                self.laizes[2],
                                                                                self.laizes[3],
                                                                                self.laizes[4],
                                                                                self.laizes[5],
                                                                                self.laizes[6])
