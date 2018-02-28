# !/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QVBoxLayout, QLabel
from PyQt5.QtCore import pyqtSignal
from commun.constants.colors import color_bleu_gris
from commun.constants.stylesheets import red_16_label_stylesheet
from commun.ui.public.mondon_widget import MondonWidget


class BobineFilleSelected(MondonWidget):

    def __init__(self, parent=None):
        super(BobineFilleSelected, self).__init__(parent=parent)
        self.background_color = color_bleu_gris
        self.master_vbox = QVBoxLayout()
        self.label = QLabel("Aucune bobine sélectionnée")
        self.label.setStyleSheet(red_16_label_stylesheet)
        self.init_widget()

    def init_widget(self):
        self.master_vbox.addWidget(self.label)
        self.setLayout(self.master_vbox)

    def set_text(self, text):
        self.label.setText(text)
