# !/usr/bin/env python
# -*- coding: utf-8 -*-

from commun.ui.public.mondon_widget import MondonWidget
from commun.utils.drawing import draw_rectangle, draw_text
from commun.constants.colors import color_gris_moyen, color_noir


class EntretoisePerfo(MondonWidget):
    ENTRETOISE_HEIGHT = 60
    BORDER_SIZE = 1

    def __init__(self, parent=None, width_value=80, ech=1):
        super(EntretoisePerfo, self).__init__(parent=parent)
        self.width_value = width_value
        self.ech = ech
        self.setFixedSize(self.width_value*self.ech, self.ENTRETOISE_HEIGHT*self.ech)

    def draw_entretoise(self, p, width, height):
        x = 0
        y = 0
        w = width - 1
        h = height - 1
        draw_rectangle(p, x, y, w, h, color=color_gris_moyen, border_color=color_noir)
        font_size = 14 * self.ech
        draw_text(p, x, y, w, h, color=color_noir, align="C", font_size=font_size, text=str(self.width_value))

    def draw(self, p):
        width = self.width_value * self.ech
        height = self.ENTRETOISE_HEIGHT * self.ech
        self.draw_entretoise(p, width, height)
