# !/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QVBoxLayout, QPushButton

from constants.colors import color_bleu_gris
from constants.stylesheets import button_white_stylesheet
from ui.widgets.public.mondon_widget import MondonWidget
from stores.stat_store import stat_store


class StatMenu(MondonWidget):
    BUTTON_HEIGHT = 30

    def __init__(self, parent=None):
        super(StatMenu, self).__init__(parent=parent)
        self.background_color = color_bleu_gris
        self.vbox = QVBoxLayout()
        self.bt_metrage_semaine=QPushButton("Metrage par semaine")
        self.bt_metrage_semaine.clicked.connect(self.on_click_metrage_semaine)
        self.bt_metrage_mois=QPushButton("Metrage par mois")
        self.bt_metrage_mois.clicked.connect(self.on_click_metrage_mois)
        self.init_widget()

    def init_widget(self):
        self.vbox.setSpacing(0)
        self.bt_metrage_semaine.setStyleSheet(button_white_stylesheet)
        self.bt_metrage_semaine.setFixedHeight(self.BUTTON_HEIGHT)
        self.bt_metrage_mois.setStyleSheet(button_white_stylesheet)
        self.bt_metrage_mois.setFixedHeight(self.BUTTON_HEIGHT)
        self.vbox.addWidget(self.bt_metrage_semaine)
        self.vbox.addWidget(self.bt_metrage_mois)
        self.vbox.addStretch(1)
        self.setLayout(self.vbox)

    def on_click_metrage_semaine(self):
        stat_store.set_new_settings(week_ago=0)

    def on_click_metrage_mois(self):
        stat_store.set_new_settings(month_ago=0)
