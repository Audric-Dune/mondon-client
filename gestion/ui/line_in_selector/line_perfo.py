# !/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QHBoxLayout, QLabel

from commun.constants.colors import color_blanc
from commun.constants.stylesheets import black_14_label_stylesheet
from commun.model.perfo import Perfo
from commun.ui.public.perfo_ui import PerfoUi
from gestion.ui.line_in_selector.line_selector import LineSelector


class LinePerfo(LineSelector):
    ON_DBCLICK_SIGNAL = pyqtSignal(Perfo)

    def __init__(self, parent=None, perfo=None, ech=1):
        super(LinePerfo, self).__init__(parent=parent)
        self.set_background_color(color_blanc)
        self.setObjectName(str(perfo.code))
        self.ech = ech
        self.perfo = perfo
        self.hbox = QHBoxLayout()
        self.init_widget(perfo)

    def init_widget(self, perfo):
        self.hbox.setSpacing(30)
        label_perfo = QLabel("Perfo. " + chr(96 + perfo.code).capitalize())
        label_perfo.setStyleSheet(black_14_label_stylesheet)
        self.hbox.addWidget(label_perfo)
        perfo_ui = PerfoUi(parent=self, perfo=self.perfo, ech=self.ech)
        self.hbox.addWidget(perfo_ui)
        self.hbox.addStretch(0)
        self.setLayout(self.hbox)

    def mouseDoubleClickEvent(self, e):
        self.ON_DBCLICK_SIGNAL.emit(self.perfo)
        super(LinePerfo, self).mouseDoubleClickEvent(e)
