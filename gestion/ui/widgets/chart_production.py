# !/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter

from commun.utils.timestamp import hour_in_timestamp,\
    timestamp_at_day_ago,\
    timestamp_at_time,\
    timestamp_au_debut_de_hour
from commun.constants.colors import color_blanc,\
    color_bleu_gris,\
    color_gris_clair,\
    color_gris_fonce,\
    color_gris_moyen,\
    color_noir,\
    color_rouge,\
    color_vert
from commun.constants.dimensions import chart_min_hour, chart_max_hour, width_grille
from commun.ui.public.mondon_widget import MondonWidget
from commun.utils.drawing import draw_rectangle, draw_text

from production.stores.data_store_manager import data_store_manager
from production.stores.settings_store import settings_store


class ChartProd(MondonWidget):
    MARGIN = 10
    MARGIN_TEXT_H = 10
    MARGIN_START_CHART_H = 180
    MARGIN_END_CHART_H = 10
    MARGIN_START_CHART_V = 10
    MARGIN_END_CHART_V = 20
    HEIGHT_LINE = 40
    MARGIN_INTER_LINE = 10

    def __init__(self, parent=None, prods=None):
        super(ChartProd, self).__init__(parent=parent)
        self.prods = prods
        self.setFixedHeight(self.MARGIN*2+self.MARGIN_INTER_LINE*4+self.HEIGHT_LINE*5+self.MARGIN_END_CHART_V+self.MARGIN_START_CHART_V)

    def draw_background(self, p):
        draw_rectangle(p, x=0, y=0, width=self.width(), height=self.height(), color=color_bleu_gris)

    def draw_fond_chart(self, p):
        draw_rectangle(p,
                       x=self.MARGIN,
                       y=self.MARGIN,
                       width=self.width()-self.MARGIN*2,
                       height=self.height()-self.MARGIN*2,
                       color=color_blanc)

    def draw_legend_H(self, p, index, text):
        draw_text(p,
                  x=self.MARGIN,
                  y=self.MARGIN+self.MARGIN_START_CHART_V+self.HEIGHT_LINE*index+self.MARGIN_INTER_LINE*index,
                  width=self.MARGIN_START_CHART_H-self.MARGIN_TEXT_H,
                  height=self.HEIGHT_LINE,
                  color=color_noir,
                  align="D",
                  font_size=12,
                  text=text)

    def draw_content_chart(self, p):
        draw_rectangle(p,
                       x=self.MARGIN+self.MARGIN_START_CHART_H,
                       y=self.MARGIN+self.MARGIN_START_CHART_V,
                       width=self.width()-self.MARGIN*2-self.MARGIN_START_CHART_H-self.MARGIN_END_CHART_H,
                       height=self.height()-self.MARGIN*2-self.MARGIN_END_CHART_V-self.MARGIN_START_CHART_V,
                       color=color_gris_moyen)

    def draw(self, p):
        self.draw_background(p)
        self.draw_fond_chart(p)
        self.draw_legend_H(p, 0, "Production")
        self.draw_legend_H(p, 1, "Réglage")
        self.draw_legend_H(p, 2, "Nettoyage")
        self.draw_legend_H(p, 3, "Maintenance")
        self.draw_legend_H(p, 4, "Sans production")
        self.draw_content_chart(p)
