# !/usr/bin/env python
# -*- coding: utf-8 -*-

# Importation des module PyQt5
from PyQt5.QtWidgets import QWidget, QLabel, QHBoxLayout, QVBoxLayout, QSizePolicy, QTextEdit
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtCore import Qt, QRectF, QTimer, QSize
from PyQt5.QtGui import QBrush, QColor, QPainter, QPen, QIcon
from param.param import *
from datetime import datetime, timedelta
from object.data_store_manager import *
from object.base_de_donnee import *
from object.bar import *
from object.settings_store import *
from fonction.gestion_timestamp import *
from fonction.draw_fonction import draw_rectangle, draw_text, draw_rectangle_radius


class StatLegend(QWidget):
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


