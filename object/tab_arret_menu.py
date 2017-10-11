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
from object.tab_arret import TabArret
from object.settings_store import *
from fonction.gestion_timestamp import *
from fonction.draw_fonction import draw_rectangle, draw_text, draw_rectangle_radius


class TabArretMenu(QWidget):
    def __init__(self, parent):
        super(TabArretMenu, self).__init__(parent=parent)
        self.day_ago = 0
        self.init_widgets()
        settings_store.add_listener(self.get_setting)
        data_store_manager.add_listener(self.update)

    def init_widgets(self):
        hbox = QHBoxLayout(self)
        hbox.setContentsMargins(0, 0, 0, 0)

        #hbox.addStretch()

        vbox_matin = QVBoxLayout()
        titre = QLabel("Liste des arrêts machine (Equipe du matin)")
        titre.setAlignment(Qt.AlignCenter)
        titre.setFixedHeight(20)
        titre.setStyleSheet("QLabel {color: rgb(255, 255, 255); font-size: 16px; background-color: #2c3e50}")
        # titre.setContentsMargins(5, 5, 5, 5)
        vbox_matin.addWidget(titre)
        tab_arret_matin = TabArret(self, moment="matin")
        vbox_matin.addWidget(tab_arret_matin)

        hbox.addLayout(vbox_matin)

        #hbox.addStretch()

        vbox_soir = QVBoxLayout()
        titre = QLabel("Liste des arrêts machine (Equipe du soir)")
        titre.setAlignment(Qt.AlignCenter)
        titre.setFixedHeight(20)
        titre.setStyleSheet("QLabel {color: rgb(255, 255, 255); font-size: 16px; background-color: #2c3e50}")
        # titre.setContentsMargins(5, 5, 5, 5)
        vbox_soir.addWidget(titre)
        tab_arret_soir = TabArret(self, moment="soir")
        vbox_soir.addWidget(tab_arret_soir)

        hbox.addLayout(vbox_soir)

        #hbox.addStretch()

        self.setLayout(hbox)

    def get_setting(self, prev_live, prev_day_ago, prev_zoom):
        self.day_ago = settings_store.day_ago
        self.update()

    def paintEvent(self, event):
        p = QPainter()
        p.begin(self)
        self.draw(p)
        p.end()

    def draw_fond(self, p):
        draw_rectangle(p, 0, 0, self.width(), self.height(), color_blanc)

    def draw(self, p):
        # self.draw_fond(p)
        pass
