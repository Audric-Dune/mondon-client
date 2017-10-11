# !/usr/bin/env python
# -*- coding: utf-8 -*-

# Importation des module PyQt5
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QSizePolicy, QLabel
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtCore import Qt, QRectF, QTimer, QSize
from PyQt5.QtGui import QBrush, QColor, QPainter, QPen, QIcon
from param.param import *
from datetime import datetime, timedelta
from object.data_store_manager import *
from object.base_de_donnee import *
from object.stat_legend import StatLegend
from object.stat_bar import StatBar
from object.settings_store import *
from fonction.gestion_timestamp import *
from fonction.draw_fonction import draw_rectangle, draw_text, draw_rectangle_radius


class StatMenu(QWidget):
    def __init__(self, parent):
        super(StatMenu, self).__init__(parent=parent)
        self.day_ago = 0
        self.init_widgets()
        settings_store.add_listener(self.get_setting)
        data_store_manager.add_listener(self.update)

    def init_widgets(self):
        hbox = QHBoxLayout(self)
        hbox.setContentsMargins(0, 0, 0, 0)

        stat_legend = StatLegend(parent=self)
        stat_legend.setFixedWidth(250)
        hbox.addWidget(stat_legend)

        stat_bar = StatBar(parent=self, titre="Equipe du matin", moment="matin")
        stat_bar.setSizePolicy(QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding))
        hbox.addWidget(stat_bar)

        stat_bar2 = StatBar(parent=self, titre="Equipe du soir", moment="soir")
        stat_bar2.setSizePolicy(QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding))
        hbox.addWidget(stat_bar2)

        stat_bar3 = StatBar(parent=self, titre="Journée complète", moment="total")
        stat_bar3.setSizePolicy(QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding))
        hbox.addWidget(stat_bar3)

        self.setLayout(hbox)

    def get_setting(self, prev_live, prev_day_ago, prev_zoom):
        self.day_ago = settings_store.day_ago
        self.update()

    def paintEvent(self, event):
        p = QPainter()
        p.begin(self)
        self.draw(p)
        p.end()

    def draw(self, p):
        pass
