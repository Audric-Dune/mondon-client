# !/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QTextEdit, QVBoxLayout, QWidget

from param import color_bleu_gris
from ui.utils.drawing import draw_rectangle
from ui.widgets.mondon_widget import MondonWidget


class StatLegend(MondonWidget):
    def __init__(self, parent):
        super(StatLegend, self).__init__(parent=parent)
        self.init_widgets()

    def init_widgets(self):
        vbox = QVBoxLayout(self)

        titre = QTextEdit("Notes:", self)
        titre.setReadOnly(True)
        titre.setAlignment(Qt.AlignVCenter)
        titre.setFixedHeight(30)
        titre.setStyleSheet("QTextEdit {background-color: #2c3e50; color: rgb(255, 255, 255); font-size: 14px;}")
        vbox.addWidget(titre)

        info_max = QTextEdit("100%: Production théorique à 172.5m/min de moyenne", self)
        info_max.setReadOnly(True)
        info_max.setAlignment(Qt.AlignVCenter)
        info_max.setStyleSheet("QTextEdit {background-color: #2c3e50; color: rgb(255, 255, 255); font-size: 14px;}")
        vbox.addWidget(info_max)

        info_82 = QTextEdit("82%: Production théorique avec changement de bobine mère", self)
        info_82.setReadOnly(True)
        info_82.setAlignment(Qt.AlignVCenter)
        info_82.setStyleSheet("QTextEdit {background-color: #2c3e50; color: rgb(255, 255, 255); font-size: 14px;}")
        vbox.addWidget(info_82)

        vbox.addStretch()

    def paintEvent(self, event):
        p = QPainter()
        p.begin(self)
        self.draw(p)
        p.end()

    def draw(self, p):
        draw_rectangle(p, 0, 0, self.width(), self.height(), color_bleu_gris)


