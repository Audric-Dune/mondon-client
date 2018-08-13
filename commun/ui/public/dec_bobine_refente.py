# !/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt, QPointF
from PyQt5.QtGui import QPen, QPainter, QColor, QFont, QPolygonF, QBrush

from commun.constants.colors import color_gris_noir, color_rouge


class DecBobineRefente(QWidget):

    def __init__(self, dec, ech=1, parent=None):
        super(DecBobineRefente, self).__init__(parent=parent)
        self.ech = ech
        self.dec = dec * ech
        if dec <= 20:
            self.ARROW_SIZE = 3 * ech
            self.FONT_SIZE_DATA = 8 * ech
        else:
            self.ARROW_SIZE = 5 * ech
            self.FONT_SIZE_DATA = 16 * ech
        self.FONT_SIZE_INFO = 15 * ech
        self.setFixedWidth(self.dec+self.FONT_SIZE_INFO)
        self.update()

    def paintEvent(self, e):
        p = QPainter(self)
        color = color_gris_noir.rgb_components
        qcolor_gris = QColor(color[0], color[1], color[2])
        pen = QPen()
        pen.setColor(qcolor_gris)
        p.setPen(pen)
        h = self.height()/2+(16*self.ech)
        w = self.width()-self.FONT_SIZE_INFO
        # _____ DRAW COTE _____
        p.drawLine(0, h, w, h)
        p.setFont(QFont('Decorative', self.FONT_SIZE_DATA))
        p.drawText(0, 0, self.width()-self.FONT_SIZE_INFO, self.height(), Qt.AlignCenter, str(self.dec))
        if self.dec > 0:
            brush = QBrush(qcolor_gris)
            p.setBrush(brush)
            left_arrow_polygon = QPolygonF()
            left_arrow_polygon.append(QPointF(0, h))
            left_arrow_polygon.append(QPointF(self.ARROW_SIZE, h+self.ARROW_SIZE/2))
            left_arrow_polygon.append(QPointF(self.ARROW_SIZE, h-self.ARROW_SIZE/2))
            p.drawPolygon(left_arrow_polygon)
            right_arrow_polygon = QPolygonF()
            right_arrow_polygon.append(QPointF(w, h))
            right_arrow_polygon.append(QPointF(w-self.ARROW_SIZE, h+self.ARROW_SIZE/2))
            right_arrow_polygon.append(QPointF(w-self.ARROW_SIZE, h-self.ARROW_SIZE/2))
            p.drawPolygon(right_arrow_polygon)
        color = color_rouge.rgb_components
        qcolor_red = QColor(color[0], color[1], color[2])
        pen.setColor(qcolor_red)
        p.setPen(pen)
        # _____ DRAW RIVE DROITE _____
        p.drawLine(w, 0, w, self.height())
        p.setFont(QFont('Decorative', self.FONT_SIZE_INFO-(5*self.ech)))
        p.translate(self.width(), (55 * self.ech))
        p.rotate(-90)
        p.drawText(0, 0, "Coté mur")
