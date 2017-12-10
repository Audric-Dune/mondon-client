# !/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QHBoxLayout, QLabel

from constants.colors import color_rouge
from constants.stylesheets import white_label_stylesheet
from ui.widgets.public.mondon_widget import MondonWidget


class ChartBarMenu(MondonWidget):

    def __init__(self, parent=None):
        super(ChartBarMenu, self).__init__(parent=parent)
        self.background_color = color_rouge
        self.hbox = QHBoxLayout(self)
        self.init_widget()

    def init_widget(self):
        label = QLabel("MENU CHART BAR")
        label.setStyleSheet(white_label_stylesheet)
        self.hbox.addWidget(label)
        self.setLayout(self.hbox)
