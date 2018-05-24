# !/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPen, QPainter, QColor

from commun.constants.colors import color_gris, color_gris_moyen
from commun.constants.stylesheets import black_16_label_stylesheet
from commun.utils.color_bobine import get_color_bobine


class BobineMereUI(QWidget):

    def __init__(self, bobine, ech=1, parent=None):
        super(BobineMereUI, self).__init__(parent=parent)
        self.bobine = bobine
        self.ech = ech
        self.setFixedHeight(100)
        self.setFixedWidth(self.bobine.laize*ech)
        self.update()
        self.init_widget()

    def init_widget(self):
        hbox = QHBoxLayout()
        hbox.addWidget(self.get_label(self.bobine.code), alignment=Qt.AlignCenter)
        hbox.addWidget(self.get_label(self.bobine.laize), alignment=Qt.AlignCenter)
        if self.bobine.color == "Poly":
            hbox.addWidget(self.get_label("Polypro 20µ"), alignment=Qt.AlignCenter)
        else:
            hbox.addWidget(self.get_label(self.bobine.color), alignment=Qt.AlignCenter)
            hbox.addWidget(self.get_label(self.bobine.gr, "g"), alignment=Qt.AlignCenter)
        hbox.addWidget(self.get_label(self.bobine.length, "m"), alignment=Qt.AlignCenter)
        self.setLayout(hbox)

    @staticmethod
    def get_label(text, suffixe=None):
        if suffixe:
            text = "{}{}".format(text, suffixe)
        label = QLabel(str(text))
        label.setStyleSheet(black_16_label_stylesheet)
        return label

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
