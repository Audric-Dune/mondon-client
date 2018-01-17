# !/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QVBoxLayout, QPushButton, QLabel

from constants.colors import color_gris_moyen
from constants.stylesheets import button_white_stylesheet, white_title_label_stylesheet, button_green_stylesheet,\
    red_title_label_stylesheet,\
    blue_title_label_stylesheet
from ui.widgets.public.mondon_widget import MondonWidget
from stores.settings_stat_store import settings_stat_store


class StatMenu(MondonWidget):
    BUTTON_HEIGHT = 30

    def __init__(self, parent=None):
        super(StatMenu, self).__init__(parent=parent)
        self.background_color = color_gris_moyen
        self.vbox = QVBoxLayout()

        self.label_stat_metrage = QLabel("Statistique métrage")
        self.bt_metrage_semaine = QPushButton("Par semaine")
        self.bt_metrage_semaine.clicked.connect(self.on_click_metrage_semaine)
        self.bt_metrage_mois = QPushButton("Par mois")
        self.bt_metrage_mois.clicked.connect(self.on_click_metrage_mois)

        self.label_stat_temps = QLabel("Statistique temps d'arrêt")
        self.bt_temps_semaine = QPushButton("Par semaine")
        self.bt_temps_semaine.clicked.connect(self.on_click_temps_semaine)
        self.bt_temps_mois = QPushButton("Par mois")
        self.bt_temps_mois.clicked.connect(self.on_click_temps_mois)

        self.label_stat_raisons = QLabel("Statistique raisons")

        self.label_stat_raisons_prévue = QLabel("Raisons prévu")
        self.bt_raisons_prévue_semaine = QPushButton("Par semaine")
        self.bt_raisons_prévue_semaine.clicked.connect(self.on_click_raisons_prévue_semaine)
        self.bt_raisons_prévue_mois = QPushButton("Par mois")
        self.bt_raisons_prévue_mois.clicked.connect(self.on_click_raisons_prévue_mois)

        self.label_stat_imprévue_raisons = QLabel("Raisons imprévu")
        self.bt_raisons_imprévue_semaine = QPushButton("Par semaine")
        self.bt_raisons_imprévue_semaine.clicked.connect(self.on_click_raisons_imprévue_semaine)
        self.bt_raisons_imprévue_mois = QPushButton("Par mois")
        self.bt_raisons_imprévue_mois.clicked.connect(self.on_click_raisons_imprévue_mois)

        self.init_widget()

    def on_settings_stat_changed(self):
        self.bt_metrage_semaine.setStyleSheet(button_white_stylesheet)
        self.bt_metrage_mois.setStyleSheet(button_white_stylesheet)
        self.bt_temps_semaine.setStyleSheet(button_white_stylesheet)
        self.bt_temps_mois.setStyleSheet(button_white_stylesheet)

        if settings_stat_store.data_type == "métrage":
            if settings_stat_store.week_ago >= 0:
                self.bt_metrage_semaine.setStyleSheet(button_green_stylesheet)
            else:
                self.bt_metrage_mois.setStyleSheet(button_green_stylesheet)
        if settings_stat_store.data_type == "temps":
            if settings_stat_store.week_ago >= 0:
                self.bt_temps_semaine.setStyleSheet(button_green_stylesheet)
            else:
                self.bt_temps_mois.setStyleSheet(button_green_stylesheet)

    def init_widget(self):
        self.vbox.setSpacing(0)
        self.vbox.setContentsMargins(5, 5, 5, 5)

        self.label_stat_metrage.setStyleSheet(white_title_label_stylesheet)
        self.label_stat_metrage.setFixedHeight(self.BUTTON_HEIGHT)

        self.bt_metrage_semaine.setStyleSheet(button_green_stylesheet)
        self.bt_metrage_semaine.setFixedHeight(self.BUTTON_HEIGHT)
        self.bt_metrage_mois.setStyleSheet(button_white_stylesheet)
        self.bt_metrage_mois.setFixedHeight(self.BUTTON_HEIGHT)

        self.label_stat_temps.setStyleSheet(white_title_label_stylesheet)
        self.label_stat_temps.setFixedHeight(self.BUTTON_HEIGHT)

        self.bt_temps_semaine.setStyleSheet(button_white_stylesheet)
        self.bt_temps_semaine.setFixedHeight(self.BUTTON_HEIGHT)
        self.bt_temps_mois.setStyleSheet(button_white_stylesheet)
        self.bt_temps_mois.setFixedHeight(self.BUTTON_HEIGHT)

        self.label_stat_raisons.setStyleSheet(white_title_label_stylesheet)
        self.label_stat_raisons.setFixedHeight(self.BUTTON_HEIGHT)

        self.label_stat_raisons_prévue.setStyleSheet(blue_title_label_stylesheet)
        self.label_stat_raisons_prévue.setFixedHeight(self.BUTTON_HEIGHT)

        self.bt_raisons_prévue_semaine.setStyleSheet(button_white_stylesheet)
        self.bt_raisons_prévue_semaine.setFixedHeight(self.BUTTON_HEIGHT)
        self.bt_raisons_prévue_mois.setStyleSheet(button_white_stylesheet)
        self.bt_raisons_prévue_mois.setFixedHeight(self.BUTTON_HEIGHT)

        self.label_stat_imprévue_raisons.setStyleSheet(red_title_label_stylesheet)
        self.label_stat_imprévue_raisons.setFixedHeight(self.BUTTON_HEIGHT)

        self.bt_raisons_imprévue_semaine.setStyleSheet(button_white_stylesheet)
        self.bt_raisons_imprévue_semaine.setFixedHeight(self.BUTTON_HEIGHT)
        self.bt_raisons_imprévue_mois.setStyleSheet(button_white_stylesheet)
        self.bt_raisons_imprévue_mois.setFixedHeight(self.BUTTON_HEIGHT)

        self.vbox.addWidget(self.label_stat_metrage)
        self.vbox.addWidget(self.bt_metrage_semaine)
        self.vbox.addWidget(self.bt_metrage_mois)
        self.vbox.addStretch(10)
        self.vbox.addWidget(self.label_stat_temps)
        self.vbox.addWidget(self.bt_temps_semaine)
        self.vbox.addWidget(self.bt_temps_mois)
        self.vbox.addStretch(10)
        self.vbox.addWidget(self.label_stat_raisons)
        self.vbox.addStretch(1)
        self.vbox.addWidget(self.label_stat_raisons_prévue)
        self.vbox.addWidget(self.bt_raisons_prévue_semaine)
        self.vbox.addWidget(self.bt_raisons_prévue_mois)
        self.vbox.addStretch(1)
        self.vbox.addWidget(self.label_stat_imprévue_raisons)
        self.vbox.addWidget(self.bt_raisons_imprévue_semaine)
        self.vbox.addWidget(self.bt_raisons_imprévue_mois)

        self.vbox.addStretch(100)
        self.setLayout(self.vbox)

    @staticmethod
    def on_click_metrage_semaine():
        settings_stat_store.set_new_settings(type="métrage", week_ago=0)

    @staticmethod
    def on_click_metrage_mois():
        settings_stat_store.set_new_settings(type="métrage", month_ago=0)

    @staticmethod
    def on_click_temps_semaine():
        settings_stat_store.set_new_settings(type="temps", week_ago=0)

    @staticmethod
    def on_click_temps_mois():
        settings_stat_store.set_new_settings(type="temps", month_ago=0)

    @staticmethod
    def on_click_raisons_prévue_semaine():
        settings_stat_store.set_new_settings(type="raisons prévue", week_ago=0)

    @staticmethod
    def on_click_raisons_prévue_mois():
        settings_stat_store.set_new_settings(type="raisons prévue", month_ago=0)

    @staticmethod
    def on_click_raisons_imprévue_semaine():
        settings_stat_store.set_new_settings(type="raisons imprévue", week_ago=0)

    @staticmethod
    def on_click_raisons_imprévue_mois():
        settings_stat_store.set_new_settings(type="raisons imprévue", month_ago=0)
