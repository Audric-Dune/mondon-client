# !/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QLabel

from constants.colors import color_bleu
from constants.stylesheets import white_label_stylesheet
from ui.widgets.public.mondon_widget import MondonWidget


class DataTab(MondonWidget):

    def __init__(self, parent=None):
        super(DataTab, self).__init__(parent=parent)
        self.background_color = color_bleu
        self.title_label = QLabel()
        self.content_stat = QVBoxLayout()
        self.vbox_master = QHBoxLayout(self)
        self.init_widget()

    def init_widget(self):
        self.title_label.setStyleSheet(white_label_stylesheet)
        self.create_stat_metrage()
        self.vbox_master.addLayout(self.content_stat)
        self.vbox_master.addWidget(self.title_label)
        self.setLayout(self.vbox_master)

    def create_stat_metrage(self):
        vbox = QVBoxLayout()
        vbox.addWidget(self.create_line("Equipe cumule"))
        vbox.addWidget(self.create_line("Equipe matin"))
        vbox.addWidget(self.create_line("Equipe soir"))
        self.content_stat.addLayout(vbox)

    @staticmethod
    def create_line(titre):
        team_label = QLabel(titre)
        return team_label
