# !/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QVBoxLayout, QPushButton
from PyQt5.QtGui import QFont, QColor, QPen,QBrush
from PyQt5.QtCore import Qt

from constants.colors import color_bleu_gris, color_blanc
from constants.stylesheets import button_white_stylesheet
from ui.widgets.public.mondon_widget import MondonWidget
from ui.utils.drawing import draw_text
from stores.stat_store import stat_store
from ui.utils.data import affiche_entier


class StatChartBar(MondonWidget):

    def __init__(self, value, color, parent=None):
        super(StatChartBar, self).__init__(parent=parent)
        self.set_background_color(color)
        self.value = str(affiche_entier(value))

    def draw_label(self, p):
        p.rotate(90)
        draw_text(p, 5, -self.width()/2-10.5, 200, 20, color=color_blanc, align="G", font_size=12, text=self.value)

    def draw(self, p):
        self._draw_fond(p)
        self.draw_label(p)
