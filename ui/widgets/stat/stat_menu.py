# !/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QHBoxLayout, QLabel

from constants.colors import color_vert_fonce
from constants.stylesheets import white_title_label_stylesheet
from ui.widgets.public.mondon_widget import MondonWidget


class StatMenu(MondonWidget):

    def __init__(self, parent=None):
        super(StatMenu, self).__init__(parent=parent)
        self.background_color = color_vert_fonce
        self.hbox = QHBoxLayout(self)
        self.init_widget()

    def init_widget(self):
        label = QLabel("STAT_MENU")
        label.setStyleSheet(white_title_label_stylesheet)
        self.hbox.addWidget(label)
        self.setLayout(self.hbox)
