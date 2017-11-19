# !/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel

from constants.colors import color_blanc
from constants.stylesheets import white_title_label_stylesheet
from stores.settings_store import settings_store
from ui.utils.drawing import draw_rectangle
from ui.widgets.public.mondon_widget import MondonWidget
from ui.widgets.tableau_arret.tab_arret import TabArret


class TabArretMenu(MondonWidget):
    def __init__(self, parent):
        super(TabArretMenu, self).__init__(parent=parent)
        self.day_ago = 0
        self.init_widgets()

    def on_settings_changed(self, prev_live, prev_day_ago, prev_zoom):
        self.day_ago = settings_store.day_ago
        self.update()

    def on_data_changed(self):
        self.update()

    def init_widgets(self):
        hbox = QHBoxLayout(self)
        hbox.setContentsMargins(0, 0, 0, 0)

        vbox_matin = QVBoxLayout()
        titre = QLabel("Liste des arrêts machine (Equipe du matin)")
        titre.setAlignment(Qt.AlignCenter)
        titre.setFixedHeight(30)
        titre.setStyleSheet(white_title_label_stylesheet)
        vbox_matin.addWidget(titre)
        tab_arret_matin = TabArret(self, moment="matin")
        tab_arret_matin.setMinimumHeight(100)
        vbox_matin.addWidget(tab_arret_matin)

        hbox.addLayout(vbox_matin)

        vbox_soir = QVBoxLayout()
        titre = QLabel("Liste des arrêts machine (Equipe du soir)")
        titre.setAlignment(Qt.AlignCenter)
        titre.setFixedHeight(30)
        titre.setStyleSheet(white_title_label_stylesheet)
        vbox_soir.addWidget(titre)
        tab_arret_soir = TabArret(self, moment="soir")
        tab_arret_soir.setMinimumHeight(100)
        vbox_soir.addWidget(tab_arret_soir)

        hbox.addLayout(vbox_soir)

        self.setLayout(hbox)

    def paintEvent(self, event):
        p = QPainter()
        p.begin(self)
        self.draw(p)
        p.end()

    def draw_fond(self, p):
        draw_rectangle(p, 0, 0, self.width(), self.height(), color_blanc)

    def draw(self, p):
        self.draw_fond(p)
        pass
