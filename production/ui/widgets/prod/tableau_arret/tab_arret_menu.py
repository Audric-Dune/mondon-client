# !/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel

from commun.constants.stylesheets import white_title_label_stylesheet
from commun.ui.public.mondon_widget import MondonWidget

from production.stores.settings_store import settings_store
from production.ui.widgets.prod.tableau_arret.tab_arret import TabArret


class TabArretMenu(MondonWidget):
    def __init__(self, parent=None, scrollbar=True):
        super(TabArretMenu, self).__init__(parent=parent)
        self.scrollbar = scrollbar
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
        hbox.setSpacing(10)

        vbox_matin = QVBoxLayout()
        vbox_matin.setSpacing(0)
        vbox_matin.setContentsMargins(0, 0, 0, 0)
        titre = QLabel("Liste des arrêts machine (Equipe du matin)")
        titre.setAlignment(Qt.AlignCenter)
        titre.setFixedHeight(20)
        titre.setStyleSheet(white_title_label_stylesheet)
        vbox_matin.addWidget(titre)
        tab_arret_matin = TabArret(parent=self, moment="matin", scrollbar=self.scrollbar)
        vbox_matin.addWidget(tab_arret_matin)

        hbox.addLayout(vbox_matin)

        vbox_soir = QVBoxLayout()
        vbox_soir.setSpacing(0)
        vbox_soir.setContentsMargins(0, 0, 0, 0)
        titre = QLabel("Liste des arrêts machine (Equipe du soir)")
        titre.setAlignment(Qt.AlignCenter)
        titre.setFixedHeight(20)
        titre.setStyleSheet(white_title_label_stylesheet)
        vbox_soir.addWidget(titre)
        tab_arret_soir = TabArret(parent=self, moment="soir", scrollbar=self.scrollbar)
        vbox_soir.addWidget(tab_arret_soir)

        hbox.addLayout(vbox_soir)

        self.setLayout(hbox)
