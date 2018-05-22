# !/usr/bin/env python
# -*- coding: utf-8 -*-

from commun.ui.public.mondon_widget import MondonWidget
from commun.utils.drawing import draw_rectangle, draw_text
from commun.utils.color_bobine import get_color_bobine
from commun.constants.colors import color_gris, color_noir


class BobineFille(MondonWidget):
    BOBINE_HEIGHT = 150

    def __init__(self, parent=None, laize=0, number=0, ech=1, bobine=None):
        super(BobineFille, self).__init__(parent=parent)
        self.bobine = bobine
        self.laize = laize
        self.number = number
        self.ech = ech
        self.setFixedSize(self.laize*self.ech, self.BOBINE_HEIGHT*self.ech)

    def draw_bobine(self, p):
        x = 0
        y = 0
        w = self.laize * self.ech - 1
        h = (self.BOBINE_HEIGHT - 1) * self.ech
        if self.bobine:
            color = get_color_bobine(self.bobine.color)
        else:
            color = color_gris
        draw_rectangle(p, x, y, w, h, color=color, border_color=color_noir)

    def draw_label_number(self, p):
        x = 0
        y = -30 * self.ech
        w = self.laize * self.ech
        h = self.BOBINE_HEIGHT * self.ech
        font_size = 14 * self.ech
        text = "Laize {}".format(self.number)
        draw_text(p, x, y, w, h, color=color_noir, align="C", font_size=font_size, text=text)

    def draw_label_laize(self, p):
        x = 0
        y = 10 * self.ech
        w = self.laize * self.ech
        h = self.BOBINE_HEIGHT * self.ech
        font_size = 22 * self.ech
        draw_text(p, x, y, w, h, color=color_noir, align="C", font_size=font_size, text=str(self.laize))

    def draw_code(self, p):
        x = 0
        y = -30 * self.ech
        w = self.laize * self.ech
        h = self.BOBINE_HEIGHT * self.ech
        font_size = 12 * self.ech
        text = self.bobine.code
        draw_text(p, x, y, w, h, color=color_noir, align="C", font_size=font_size, text=text)

    def draw_gr(self, p):
        x = 0
        y = -30 * self.ech
        w = self.laize * self.ech
        h = self.BOBINE_HEIGHT * self.ech
        font_size = 12 * self.ech
        text = self.bobine.code
        draw_text(p, x, y, w, h, color=color_noir, align="C", font_size=font_size, text=text)

    def draw_length(self, p):
        x = 0
        y = -30 * self.ech
        w = self.laize * self.ech
        h = self.BOBINE_HEIGHT * self.ech
        font_size = 12 * self.ech
        text = self.bobine.code
        draw_text(p, x, y, w, h, color=color_noir, align="C", font_size=font_size, text=text)

    def draw(self, p):
        self.draw_bobine(p)
        self.draw_label_laize(p)
        if self.bobine:
            self.draw_code(p)
            self.draw_gr(p)
            self.draw_length(p)
        else:
            self.draw_label_number(p)
