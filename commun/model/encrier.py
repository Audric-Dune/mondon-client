# !/usr/bin/env python
# -*- coding: utf-8 -*-


class Encrier:

    def __init__(self, color=None, bobines_filles_selected=None, refente=None):
        self.color = color
        self.bobines_filles_selected = bobines_filles_selected
        self.refente = refente

    def set_color(self, color):
        self.color = color

    def reset_color(self):
        self.color = None

    def __repr__(self):
        return "Encrier: couleur {}, bobines {}, refente {}".format(self.color,
                                                                    self.bobines_filles_selected,
                                                                    self.refente)
