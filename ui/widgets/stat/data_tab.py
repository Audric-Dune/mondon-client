# !/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QHBoxLayout, QLabel

from constants.colors import color_bleu
from constants.stylesheets import white_label_stylesheet
from ui.widgets.public.mondon_widget import MondonWidget


class DataTab(MondonWidget):

    def __init__(self, parent=None):
        super(DataTab, self).__init__(parent=parent)
        self.background_color = color_bleu
        self.hbox = QHBoxLayout(self)
        self.init_widget()

    def init_widget(self):
        label = QLabel("DATA_TAB")
        label.setStyleSheet(white_label_stylesheet)
        self.hbox.addWidget(label)
        self.setLayout(self.hbox)
