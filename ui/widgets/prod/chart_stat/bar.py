# !/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtGui import QPainter

from constants.colors import (
    color_blanc,
    color_rouge,
    color_orange,
    color_vert,
    color_bleu,
    color_bleu_gris,
)
from ui.utils.drawing import draw_rectangle, draw_text
from ui.widgets.public.mondon_widget import MondonWidget


class Bar(MondonWidget):
    def __init__(self, parent, percent):
        super(Bar, self).__init__(parent=parent)
        self.percent = percent

    def paintEvent(self, event):
        p = QPainter()
        p.begin(self)
        self.draw(p)
        p.end()

    def get_percent(self, percent):
        self.percent = percent
        if percent > 100:
            self.percent = 100
        self.update()

    def draw(self, p):
        draw_rectangle(p, 0, 0, self.width(), self.height()/2, color_blanc)
        scale = self.width() / 100
        if self.percent != 0:
            if self.percent < 25:
                color = color_rouge
            elif self.percent < 50:
                color = color_orange
            else:
                color = color_vert
            draw_rectangle(p, 0, 0, self.percent*scale, self.height()/2, color)
        draw_rectangle(p, 82.12 * scale, 0, 2, self.height(), color_bleu)
        width = 220
        draw_text(p,
                  x=82.12*scale-width-5,
                  y=self.height()/2,
                  width=width,
                  height=self.height()/2,
                  color=color_bleu,
                  align="D",
                  font_size=10,
                  text="Max sans réglage de prod 82%")
        width = 150
        margin_text = 5
        if self.percent > 22:
            color_text = color_blanc
            pos_text_x = self.percent*scale-width - margin_text
            align = "D"
        else:
            color_text = color_bleu_gris
            pos_text_x = self.percent*scale + margin_text
            align = "G"
        draw_text(p,
                  x=pos_text_x,
                  y=0,
                  width=width,
                  height=self.height()/2,
                  color=color_text,
                  align=align,
                  font_size=12,
                  text='{result}%'.format(result=round(self.percent, 2)))
