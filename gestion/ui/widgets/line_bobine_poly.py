# !/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QHBoxLayout, QLabel, QWidget
from PyQt5.QtCore import pyqtSignal

from commun.ui.public.mondon_widget import MondonWidget
from commun.constants.colors import color_blanc


class LineBobinePoly(MondonWidget):
    ON_DBCLICK_SIGNAL = pyqtSignal(QWidget)

    def __init__(self, parent=None, bobine=None):
        super(LineBobinePoly, self).__init__(parent=parent)
        self.set_background_color(color_blanc)
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
        lenght = QLabel(str(self.bobine.lenght))
        hbox.addWidget(lenght)

    def mouseDoubleClickEvent(self, e):
        self.ON_DBCLICK_SIGNAL.emit(self.bobine)
