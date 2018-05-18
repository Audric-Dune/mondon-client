# !/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPen, QPainter, QColor

from commun.constants.colors import color_gris, color_gris_moyen
from commun.utils.color_bobine import get_color_bobine


class BobineMere(QWidget):

    def __init__(self, bobine, ech=1, parent=None):
        super(BobineMere, self).__init__(parent=parent)
        self.bobine = bobine
        self.ech = ech
        self.setFixedHeight(100)
        self.setFixedWidth(self.bobine.laize*ech)
        self.update()

    def paintEvent(self, e):
        p = QPainter(self)
        qcolor_font = self.get_qcolor_of_bobine(self.bobine)
        color = color_gris_moyen.rgb_components
        qcolor_gris = QColor(color[0], color[1], color[2])
        pen = QPen()
        pen.setColor(qcolor_gris)
        p.setPen(pen)
        p.fillRect(0, 0, self.width(), self.height(), qcolor_font)
        p.drawRect(0, 0, self.width()-1, self.height()-1)

    @staticmethod
    def get_qcolor_of_bobine(bobine):
        if bobine.color == "Poly":
            color = color_gris.rgb_components
        else:
            color = get_color_bobine(bobine_color=bobine.color).rgb_components
        return QColor(color[0], color[1], color[2])
