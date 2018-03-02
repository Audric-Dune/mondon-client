# !/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QHBoxLayout, QLabel
from commun.ui.public.mondon_widget import MondonWidget


class LineBobinePapier(MondonWidget):

    def __init__(self, parent=None, bobine=None):
        super(LineBobinePapier, self).__init__(parent=parent)
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

