# !/usr/bin/env python
# -*- coding: utf-8 -*-

from constants.colors import (
    color_blanc,
    color_rouge,
    color_orange,
    color_vert,
    color_bleu,
    color_bleu_gris,
)
from constants.param import PERCENT_PROD_THEROIQUE_MAXI
from ui.utils.drawing import draw_rectangle, draw_text
from ui.widgets.public.mondon_widget import MondonWidget


class Bar(MondonWidget):
    def __init__(self, parent, percent=0, little=False):
        super(Bar, self).__init__(parent=parent)
        self.percent = percent
        self.little = little

    def set_percent(self, percent):
        self.percent = percent
        if percent > 100:
            self.percent = 100
        self.update()

    def get_scale(self):
        scale = self.width() / 100
        return scale

    def draw_bar_fond(self, p):
        height = self.height() if self.little else self.height() / 2
        draw_rectangle(p, 0, 0, self.width(), height, color_blanc)

    def draw_bar(self, p):
        height = self.height() if self.little else self.height() / 2
        scale = self.get_scale()
        if self.percent != 0:
            if self.percent < 25:
                color = color_rouge
            elif self.percent < 50:
                color = color_orange
            else:
                color = color_vert
            draw_rectangle(p, 0, 0, self.percent*scale, height, color)

    def draw_max_info(self, p):
        scale = self.get_scale()
        width = (100 - PERCENT_PROD_THEROIQUE_MAXI) * scale if self.little else 100
        y = 0 if self.little else self.height() / 2
        height = self.height() if self.little else self.height() / 2
        align = "C" if self.little else "D"
        text = "82% \n (Max.)" if self.little else "Max 82%"
        font_size = 8 if self.little else 10
        x = PERCENT_PROD_THEROIQUE_MAXI*scale+5 if self.little else PERCENT_PROD_THEROIQUE_MAXI*scale-width-5
        draw_rectangle(p, PERCENT_PROD_THEROIQUE_MAXI * scale, 0, 2, self.height(), color_bleu)
        draw_text(p,
                  x=x,
                  y=y,
                  width=width,
                  height=height,
                  color=color_bleu,
                  align=align,
                  font_size=font_size,
                  text=text,
                  bold=self.little)

    def draw_percent(self, p):
        height = self.height() if self.little else self.height() / 2
        scale = self.get_scale()
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
                  height=height,
                  color=color_text,
                  align=align,
                  font_size=12,
                  text='{result}%'.format(result=round(self.percent, 2)))

    def draw(self, p):
        self.draw_bar_fond(p)
        self.draw_bar(p)
        if self.percent < 82.12:
            self.draw_max_info(p)
        self.draw_percent(p)