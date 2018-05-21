# !/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPen, QPainter, QColor, QFont

from commun.utils.drawing import draw_rectangle, draw_text, draw_triangle
from commun.constants.colors import color_gris_noir, color_rouge


class DecBobineRefente(QWidget):
    FONT_SIZE_INFO = 15

    def __init__(self, dec, ech=1, parent=None):
        super(DecBobineRefente, self).__init__(parent=parent)
        self.dec = dec
        self.ech = ech
        self.setFixedWidth(self.dec*ech+self.FONT_SIZE_INFO)
        self.update()

    def paintEvent(self, e):
        p = QPainter(self)
        color = color_gris_noir.rgb_components
        qcolor_gris = QColor(color[0], color[1], color[2])
        pen = QPen()
        pen.setColor(qcolor_gris)
        p.setPen(pen)
        h = self.height()/2+16
        w = self.width()-self.FONT_SIZE_INFO
        p.drawLine(0, h, w, h)
        p.setFont(QFont('Decorative', 16))
        p.drawText(0, 0, self.width()-self.FONT_SIZE_INFO, self.height(), Qt.AlignCenter, str(self.dec))
        color = color_rouge.rgb_components
        qcolor_red = QColor(color[0], color[1], color[2])
        pen.setColor(qcolor_red)
        p.setPen(pen)
        p.drawLine(w, 0, w, self.height())
        p.setFont(QFont('Decorative', self.FONT_SIZE_INFO-5))
        p.translate(self.width(), 55)
        p.rotate(-90)
        p.drawText(0, 0, "Coté mur")

