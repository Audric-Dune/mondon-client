# !/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt

from constants.colors import color_gris_moyen, color_gris_clair, color_gris_moyen
from constants.stylesheets import green_20_label_stylesheet, white_label_stylesheet, white_title_label_stylesheet, green_title_label_stylesheet
from ui.widgets.public.mondon_widget import MondonWidget
from ui.utils.layout import clear_layout
from ui.utils.data import affiche_entier
from ui.widgets.prod.chart_stat.bar import Bar
from stores.stat_store import stat_store


class DataTab(MondonWidget):

    def __init__(self, parent=None):
        super(DataTab, self).__init__(parent=parent)
        self.background_color = color_gris_clair
        self.title_label = QLabel()
        self.content_stat = QVBoxLayout()
        self.vbox_master = QVBoxLayout(self)
        self.init_widget()
        self.update_widget()

    def init_widget(self):
        self.title_label.setStyleSheet(green_20_label_stylesheet)
        self.title_label.setFixedHeight(40)
        self.vbox_master.addWidget(self.title_label)
        self.create_stat_metrage()
        self.vbox_master.addLayout(self.content_stat)
        self.setLayout(self.vbox_master)

    def on_data_stat_changed(self):
        self.update_widget()

    def on_settings_stat_changed(self):
        self.update_widget()

    def update_widget(self):
        text_title = "Statistique {stat} : {time_stat}".format(stat=stat_store.stat, time_stat=stat_store.time_stat)
        self.title_label.setText(text_title)
        self.title_label.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        clear_layout(self.content_stat)
        self.create_stat_metrage()

    def create_stat_metrage(self):
        vbox = QVBoxLayout()
        vbox.addLayout(self.create_line("Equipes cumulées", index_data=2))
        vbox.addLayout(self.create_line("Equipe matin", index_data=0))
        vbox.addLayout(self.create_line("Equipe soir", index_data=1))
        self.content_stat.addLayout(vbox)

    def create_line(self, titre, index_data):
        hbox = QHBoxLayout()

        team_label = QLabel(titre)
        team_label.setStyleSheet(white_title_label_stylesheet)
        team_label.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        team_label.setFixedWidth(150)
        hbox.addWidget(team_label)

        vbox_text = QVBoxLayout()
        vbox_text.setSpacing(0)
        total_label = QLabel("Total metrage")
        total_label.setStyleSheet(white_label_stylesheet)
        total_label.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        vbox_text.addWidget(total_label)
        moyenne_label = QLabel("Moyenne par jours")
        moyenne_label.setStyleSheet(white_label_stylesheet)
        moyenne_label.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        vbox_text.addWidget(moyenne_label)
        hbox.addLayout(vbox_text)

        vbox_value = QVBoxLayout()
        vbox_value.setSpacing(0)
        sum_value = sum(stat_store.data[index_data]["values"])
        total_value = QLabel(affiche_entier(sum_value))
        total_value.setStyleSheet(white_label_stylesheet)
        total_value.setFixedHeight(20)
        total_value.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        vbox_value.addWidget(total_value)
        team_moyenne = stat_store.data[index_data]["moyenne"]
        label_moyenne = QLabel(affiche_entier(team_moyenne))
        label_moyenne.setStyleSheet(white_label_stylesheet)
        label_moyenne.setFixedHeight(20)
        label_moyenne.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        vbox_value.addWidget(label_moyenne)
        hbox.addLayout(vbox_value)

        bar = Bar(parent=None, percent=stat_store.data[index_data]["percent"])
        hbox.addWidget(bar)

        return hbox
