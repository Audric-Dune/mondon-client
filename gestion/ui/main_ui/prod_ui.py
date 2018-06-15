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
        # self.context_menu = ContextMenu()
        # self.init_context_menu()
        self.init_ui()
        self.show()

    # def init_context_menu(self):
    #     self.context_menu.add_action(literal_name="Editer", callback=self.edit_prod)
    #     self.context_menu.add_action(literal_name="Supprimer", callback=self.delete_prod, risk_style=True)

    def delete_prod(self):
        settings_store_gestion.delete_plan_prod(self.prod)

    def edit_prod(self):
        pass

    def init_ui(self):
        self.setFixedWidth(ceil(self.ech*(self.prod.end-self.prod.start)))
        self.setFixedHeight(50)

    def paintEvent(self, e):
        p = QPainter(self)
        color = self.color.rgb_components
        qcolor = QColor(color[0], color[1], color[2])
        brush = QBrush()
        brush.setStyle(Qt.SolidPattern)
        brush.setColor(qcolor)
        p.setBrush(brush)
        p.drawRect(0, 0, self.width()-1, self.height()-1)
        color = self.border_color.rgb_components
        qborder_color = QColor(color[0], color[1], color[2])
        pen = QPen()
        pen.setColor(qborder_color)
        p.setPen(pen)
        p.drawRect(0, 0, self.width()-1, self.height()-1)

    # def mouseReleaseEvent(self, e):
    #     if e.button() == Qt.RightButton:
    #         self.context_menu.show()

    def focusInEvent(self, e):
        self.border_color = color_rouge
        self.update()
        settings_store_gestion.set_item_focus(item=self.prod)

    def focusOutEvent(self, e):
        self.border_color = color_noir
        self.update()
        settings_store_gestion.set_item_focus(item=None)
