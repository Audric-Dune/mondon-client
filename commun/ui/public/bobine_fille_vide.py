# !/usr/bin/env python
# -*- coding: utf-8 -*-

from commun.ui.public.mondon_widget import MondonWidget
from commun.utils.drawing import draw_rectangle, draw_text
from commun.constants.colors import color_gris_fonce, color_noir


class BobineFilleVide(MondonWidget):
    BOBINE_HEIGHT = 200

    def __init__(self, parent=None, laize=0, number=0, ech=1):
        super(BobineFilleVide, self).__init__(parent=parent)
        self.laize = laize
        self.number = number
        self.ech = ech
        self.setFixedSize(self.laize*self.ech, self.BOBINE_HEIGHT)

    def draw_bobine(self, p):
        x = 0
        y = 0
        w = self.laize * self.ech - 1
        h = self.BOBINE_HEIGHT - 1 * self.ech
        draw_rectangle(p, x, y, w, h, color=color_gris_fonce, border_color=color_noir)

    def draw_label_number(self, p):
        x = 0
        y = -30 * self.ech
        w = self.laize * self.ech
        h = self.BOBINE_HEIGHT * self.ech
        font_size = 20 * self.ech
        text = "Laize {}".format(self.number)
        draw_text(p, x, y, w, h, color=color_noir, align="C", font_size=font_size, text=text)

    def draw_label_laize(self, p):
        x = 0
        y = 10 * self.ech
        w = self.laize * self.ech
        h = self.BOBINE_HEIGHT * self.ech
        font_size = 28 * self.ech
        draw_text(p, x, y, w, h, color=color_noir, align="C", font_size=font_size, text=str(self.laize))

    def draw(self, p):
        self.draw_bobine(p)
        self.draw_label_number(p)
        self.draw_label_laize(p)
