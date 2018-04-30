# !/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QHBoxLayout, QLabel
from PyQt5.QtCore import pyqtSignal
from commun.ui.public.mondon_widget import MondonWidget
from commun.constants.colors import color_blanc
from commun.model.bobine_fille import BobineFille


class LineBobine(MondonWidget):
    ON_DBCLICK_SIGNAL = pyqtSignal(BobineFille)

    def __init__(self, parent=None, bobine=None):
        super(LineBobine, self).__init__(parent=parent)
        self.set_background_color(color_blanc)
        self.state = None
        self.installEventFilter(self)
        self.bobine = bobine
        self.background_color = color_blanc
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
        lenght = QLabel("{}m".format(self.bobine.lenght))
        hbox.addWidget(lenght)
        gr = QLabel("{}g".format(self.bobine.gr))
        hbox.addWidget(gr)
        color = QLabel(str(self.bobine.color))
        hbox.addWidget(color)
        code_cliche = QLabel(str(self.bobine.codes_cliche))
        hbox.addWidget(code_cliche)
        poses = QLabel(str(self.bobine.poses))
        hbox.addWidget(poses)

    def mouseDoubleClickEvent(self, e):
        self.ON_DBCLICK_SIGNAL.emit(self.bobine)
