# !/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPen, QPainter, QColor, QBrush

from commun.ui.public.mondon_widget import QWidget
from commun.utils.drawing import draw_rectangle, draw_text
from commun.constants.colors import color_gris, color_noir, color_gris_noir


class ChuteUi(QWidget):
    BOBINE_HEIGHT = 150

    def __init__(self, parent=None, chute=0, ech=1):
        super(ChuteUi, self).__init__(parent=parent)
        self.chute = chute
        self.ech = ech
        self.setFixedSize(self.chute*self.ech, self.BOBINE_HEIGHT*self.ech)

    def paintEvent(self, e):
        p = QPainter(self)
        color = color_noir.rgb_components
        qcolor_gris = QColor(color[0], color[1], color[2])
        pen = QPen()
        pen.setColor(qcolor_gris)
        p.setPen(pen)
        self.draw(p)

    def draw_chute(self, p):
        x = 0
        y = 0
        w = self.chute * self.ech - 1
        h = (self.BOBINE_HEIGHT - 1) * self.ech
        color = color_gris
        draw_rectangle(p, x, y, w, h, color=color, border_color=color_noir)
        color = color_gris_noir.rgb_components
        background_color = QColor(color[0], color[1], color[2])
        brush = QBrush()
        brush.setStyle(Qt.BDiagPattern)
        brush.setColor(background_color)
        p.setBrush(brush)
        p.drawRect(0, 0, self.width(), self.height())

    def draw_label_chute(self, p):
        font_size = 22 * self.ech
        x = 5 * self.ech
        h = font_size + 5 * self.ech
        y = self.BOBINE_HEIGHT / 2 - h / 2
        w = self.chute * self.ech - 2 * x
        draw_text(p, x, y, w, h, color=color_noir, align="C", font_size=font_size, text=str(int(self.chute)))

    def draw(self, p):
        self.draw_chute(p)
        self.draw_label_chute(p)
