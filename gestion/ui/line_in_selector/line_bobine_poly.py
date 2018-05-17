# !/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QHBoxLayout, QLabel
from PyQt5.QtCore import pyqtSignal, Qt

from gestion.ui.line_in_selector.line_selector import LineSelector
from commun.constants.stylesheets import black_14_label_stylesheet
from commun.model.bobine_mere import BobineMere
from commun.constants.colors import color_blanc
from commun.constants.dimensions import dict_width_selector_poly


class LineBobinePoly(LineSelector):
    ON_DBCLICK_SIGNAL = pyqtSignal(BobineMere)

    def __init__(self, parent=None, bobine=None):
        super(LineBobinePoly, self).__init__(parent=parent)
        self.set_background_color(color_blanc)
        self.setObjectName(bobine.code)
        self.setFixedHeight(20)
        self.state = None
        self.installEventFilter(self)
        self.bobine = bobine
        self.init_widget()

    def init_widget(self):
        hbox = QHBoxLayout()
        hbox.setContentsMargins(5, 0, 0, 0)
        hbox.setSpacing(10)
        self.setLayout(hbox)
        code = QLabel(str(self.bobine.code))
        code.setStyleSheet(black_14_label_stylesheet)
        code.setAlignment(Qt.AlignCenter)
        hbox.addWidget(code)
        laize = QLabel(str(int(self.bobine.laize)))
        laize.setStyleSheet(black_14_label_stylesheet)
        laize.setAlignment(Qt.AlignCenter)
        hbox.addWidget(laize)
        lenght = QLabel(str(self.bobine.lenght))
        lenght.setStyleSheet(black_14_label_stylesheet)
        lenght.setAlignment(Qt.AlignCenter)
        hbox.addWidget(lenght)
        famille = QLabel("Polypro 20µ")
        famille.setStyleSheet(black_14_label_stylesheet)
        famille.setAlignment(Qt.AlignCenter)
        hbox.addWidget(famille)
        for key in dict_width_selector_poly.keys():
            vars()[key].setMinimumWidth(dict_width_selector_poly[key])

    def mouseDoubleClickEvent(self, e):
        self.ON_DBCLICK_SIGNAL.emit(self.bobine)
