# !/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QHBoxLayout, QLabel
from PyQt5.QtCore import pyqtSignal
from gestion.ui.line_in_selector.line_selector import LineSelector
from commun.model.bobine_mere import BobineMere
from commun.constants.colors import color_blanc


class LineBobinePapier(LineSelector):
    ON_DBCLICK_SIGNAL = pyqtSignal(BobineMere)

    def __init__(self, parent=None, bobine=None):
        super(LineBobinePapier, self).__init__(parent=parent)
        self.set_background_color(color_blanc)
        self.setObjectName(bobine.code)
        self.state = None
        self.installEventFilter(self)
        self.bobine = bobine
        self.init_widget()

    def init_widget(self):
        hbox = QHBoxLayout()
        hbox.setContentsMargins(5, 0, 0, 0)
        self.setLayout(hbox)
        code = QLabel(str(self.bobine.code))
        code.setFixedWidth(150)
        hbox.addWidget(code)
        laize = QLabel(str(int(self.bobine.laize)))
        hbox.addWidget(laize)
        color = QLabel(str(self.bobine.color.capitalize()))
        hbox.addWidget(color)
        gr = QLabel(str(self.bobine.gr))
        hbox.addWidget(gr)
        lenght = QLabel(str(self.bobine.lenght))
        hbox.addWidget(lenght)

    def mouseDoubleClickEvent(self, e):
        self.ON_DBCLICK_SIGNAL.emit(self.bobine)

