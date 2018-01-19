# !/usr/bin/env python
# -*- coding: utf-8 -*-

from commun.ui.public.mondon_widget import MondonWidget
from commun.utils.drawing import draw_rectangle, draw_text, draw_triangle
from commun.constants.colors import color_gris_fonce, color_noir


class BaguePerfo(MondonWidget):
    HEIGHT = 50
    PIC_NUMBER = 10
    BORDER_SIZE = 1

    def __init__(self, parent=None, width_value=80):
        super(BaguePerfo, self).__init__(parent=parent)
        self.width_value = width_value
        self.setFixedSize(self.width_value, self.HEIGHT)

    def draw_bague(self, p, pic_height):
        x = 0
        y = pic_height
        w = self.width() - 1
        h = self.height() - 2 * pic_height
        draw_rectangle(p, x, y, w, h, color=color_gris_fonce, border_color=color_noir)
        font_size = min(self.height(), self.width()) / 3
        draw_text(p, x, y, w, h, color=color_noir, align="C", font_size=font_size, text=str(self.width_value))

    def draw_pic(self, p, pic_height):
        pic_count = 0
        while pic_count < self.PIC_NUMBER:
            y = 0
            w = self.width() / self.PIC_NUMBER
            x = 0 + w * pic_count
            h = pic_height
            draw_triangle(p, x, y, w, h,
                          background_color=color_gris_fonce,
                          border_color=color_noir,
                          border_size=self.BORDER_SIZE)
            y = self.height() - pic_height
            draw_triangle(p, x, y, w, h,
                          background_color=color_gris_fonce,
                          border_color=color_noir,
                          border_size=self.BORDER_SIZE,
                          reverse=True)
            pic_count += 1

    def draw(self, p):
        pic_height = 8
        self.draw_bague(p, pic_height)
        self.draw_pic(p, pic_height)
