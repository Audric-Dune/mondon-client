# !/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QHBoxLayout, QWidget, QScrollArea
from PyQt5.QtCore import Qt

from constants.colors import color_bleu_gris
from constants.stylesheets import scroll_bar_stylesheet
from ui.widgets.public.mondon_widget import MondonWidget
from ui.widgets.rapport.rapport import Rapport


class PreviewRapport(MondonWidget):
    def __init__(self, parent=None):
        super(PreviewRapport, self).__init__(parent)
        self.set_background_color(color_bleu_gris)
        self.rapport = Rapport(parent=self)
        self.init_widget()

    def init_widget(self):
        hbox = QHBoxLayout()
        self.rapport.setFixedSize(771, 1100)
        content_scroll = QHBoxLayout()
        content_scroll.addWidget(self.rapport)
        widget = QWidget(parent=self)
        widget.setLayout(content_scroll)
        widget.setStyleSheet("background-color:white;")
        scroll_bar = QScrollArea()
        scroll_bar.setWidget(widget)
        scroll_bar.setStyleSheet(scroll_bar_stylesheet)
        scroll_bar.setAlignment(Qt.AlignCenter)
        hbox.addWidget(scroll_bar)
        self.setLayout(hbox)
