# !/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QHBoxLayout, QLabel, QWidget
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QPainter, QPen

from commun.constants.colors import color_noir
from commun.constants.stylesheets import black_14_label_stylesheet


class LegendBobineSelected(QWidget):

    def __init__(self, parent=None):
        super(LegendBobineSelected, self).__init__(parent=parent)
        self.init_widget()

    def init_widget(self):
        hbox = QHBoxLayout()
        hbox.setContentsMargins(0, 5, 0, 5)
        hbox.addWidget(self.get_label("Code", center=False, width=200))
        hbox.addWidget(self.get_label("Laize", width=80))
        hbox.addWidget(self.get_label("Piste", width=80))
        hbox.addWidget(self.get_label("Stock actuel"))
        hbox.addWidget(self.get_label("Stock à therme"))
        hbox.addWidget(self.get_label("Production"))
        hbox.addWidget(self.get_label("Stock prévisionnel"))
        hbox.addWidget(self.get_label("Etat prévisionnel"))
        self.setLayout(hbox)

    @staticmethod
    def get_label(text, vcenter=True, center=True, width=None):
        label = QLabel(text)
        if center and not vcenter:
            label.setAlignment(Qt.AlignVCenter)
        elif vcenter and not center:
            label.setAlignment(Qt.AlignCenter)
        else:
            label.setAlignment(Qt.AlignVCenter | Qt.AlignCenter)
        label.setStyleSheet(black_14_label_stylesheet)
        if width is not None:
            label.setFixedWidth(width)
        return label

    def paintEvent(self, event):
        p = QPainter(self)
        color = color_noir.rgb_components
        qcolor_noir = QColor(color[0], color[1], color[2])
        pen = QPen()
        pen.setColor(qcolor_noir)
        p.setPen(pen)
        p.drawLine(1, self.height()-1, self.width()-1, self.height()-1)
