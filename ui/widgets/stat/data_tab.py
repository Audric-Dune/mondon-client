# !/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt

from constants.colors import color_gris_clair, color_bleu_gris
from constants.stylesheets import green_20_label_stylesheet, white_label_stylesheet, white_title_label_stylesheet
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
        self.vbox_master = QVBoxLayout()
        self.init_widget()
        self.update_widget()

    def init_widget(self):
        self.title_label.setStyleSheet(green_20_label_stylesheet)
        self.title_label.setFixedHeight(40)
        self.vbox_master.addWidget(self.title_label)
        self.vbox_master.setContentsMargins(0, 0, 0, 0)
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

    def create_stat_metrage(self):
        hbox = QHBoxLayout()
        hbox.addWidget(BlocStat(parent=self, titre="Equipe matin", index_data=0))
        hbox.addWidget(BlocStat(parent=self, titre="Equipe soir", index_data=1))
        hbox.addWidget(BlocStat(parent=self, titre="Equipes cumulées", index_data=2))
        self.content_stat.addLayout(hbox)


class BlocStat(MondonWidget):

    def __init__(self, parent=None, titre=None, index_data=None):
        super(BlocStat, self).__init__(parent=parent)
        self.set_background_color(color_bleu_gris)
        self.titre = titre
        self.index_data = index_data
        self.vbox = QVBoxLayout()
        self.init_widget()

    def update_widget(self):
        clear_layout(self.vbox)
        self.init_widget()

    def init_widget(self):

        team_label = QLabel(self.titre)
        team_label.setStyleSheet(white_title_label_stylesheet)
        team_label.setFixedHeight(30)
        team_label.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        self.vbox.addWidget(team_label)

        content_bar = QHBoxLayout()
        bar = Bar(parent=None, percent=stat_store.data[self.index_data]["percent"])
        bar.setFixedHeight(50)
        content_bar.addWidget(bar)
        self.vbox.addLayout(content_bar)

        total_value_layout = QHBoxLayout()
        sum_value = sum(stat_store.data[self.index_data]["values"])
        titre_total_value = QLabel("Métrage total")
        titre_total_value.setStyleSheet(white_label_stylesheet)
        total_value_layout.addWidget(titre_total_value, alignment=Qt.AlignLeft)
        total_value = QLabel("{} m".format(affiche_entier(sum_value)))
        total_value.setStyleSheet(white_title_label_stylesheet)
        total_value_layout.addWidget(total_value)
        self.vbox.addLayout(total_value_layout)

        label_moyenne_layout = QHBoxLayout()
        team_moyenne = stat_store.data[self.index_data]["moyenne"]
        titre_total_value = QLabel("Moyenne")
        titre_total_value.setStyleSheet(white_label_stylesheet)
        label_moyenne_layout.addWidget(titre_total_value, alignment=Qt.AlignLeft)
        label_moyenne = QLabel("{} m/jour".format(affiche_entier(team_moyenne)))
        label_moyenne.setStyleSheet(white_title_label_stylesheet)
        label_moyenne_layout.addWidget(label_moyenne)
        self.vbox.addLayout(label_moyenne_layout)

        self.setLayout(self.vbox)

    def on_data_stat_changed(self):
        self.update_widget()

    def on_settings_stat_changed(self):
        self.update_widget()
