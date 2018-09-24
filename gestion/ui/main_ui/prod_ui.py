# !/usr/bin/env python
# -*- coding: utf-8 -*-

from math import ceil

from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QBrush, QColor, QPen
from PyQt5.QtCore import Qt

from commun.utils.color_bobine import get_color_bobine
from commun.constants.colors import color_noir, color_rouge
# from commun.ui.public.context_menu import ContextMenu

from gestion.stores.settings_store import settings_store_gestion


class ProdUi(QWidget):
    def __init__(self, prod, ech, parent=None):
        super(ProdUi, self).__init__(parent=parent)
        self.setFocusPolicy(Qt.ClickFocus)
        self.ech = ech
        self.prod = prod
        self.selected = True
        self.color = get_color_bobine(bobine_color=self.prod.bobine_papier_selected.color)
        self.border_color = color_noir
        self.init_ui()
        self.show()

    def init_ui(self):
        self.setFixedWidth(ceil(self.ech*(self.prod.end-self.prod.start)))
        self.setFixedHeight(105)

    def paintEvent(self, e):
        p = QPainter(self)
        w = ceil(self.ech*(self.prod.data_reglages.time_reglage*60))
        self.draw_rect(p, x=w, y=0, w=self.width()-w-1, s_brush=Qt.SolidPattern)
        self.draw_rect(p, x=0, y=self.height()/2+5, w=w, s_brush=Qt.BDiagPattern)

    def draw_rect(self, p, x, y, w, s_brush):
        color = self.color.rgb_components
        qcolor = QColor(color[0], color[1], color[2])
        brush = QBrush()
        brush.setStyle(s_brush)
        brush.setColor(qcolor)
        p.setBrush(brush)
        p.drawRect(x, y, w, self.height()/2-5)
        color = self.border_color.rgb_components
        qborder_color = QColor(color[0], color[1], color[2])
        pen = QPen()
        pen.setColor(qborder_color)
        p.setPen(pen)
        p.drawRect(x, y, w, (self.height())/2-5)

    def focusInEvent(self, e):
        self.border_color = color_rouge
        self.update()
        settings_store_gestion.set_item_focus(item=self.prod)

    def focusOutEvent(self, e):
        self.border_color = color_noir
        self.update()
        if not settings_store_gestion.standing_insert:
            settings_store_gestion.set_item_focus(item=None)
