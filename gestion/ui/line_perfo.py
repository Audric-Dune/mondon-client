# !/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QHBoxLayout, QLabel
from commun.ui.public.mondon_widget import MondonWidget
from commun.ui.public.bague_perfo import BaguePerfo
from commun.ui.public.entretoise_perfo import EntretoisePerfo


class LinePerfo(MondonWidget):

    def __init__(self, parent=None, perfo=None):
        super(LinePerfo, self).__init__(parent=parent)
        self.hbox = QHBoxLayout()
        self.init_widget(perfo)

    def init_widget(self, perfo):
        self.hbox.setSpacing(0)
        label_perfo = QLabel("Perfo." + chr(96 + perfo.code).capitalize())
        label_perfo.setFixedWidth(50)
        self.hbox.addWidget(label_perfo)
        cale1 = perfo.cale1
        if cale1:
            self.hbox.addWidget(EntretoisePerfo(parent=self, width_value=cale1))
        bague1 = perfo.bague1
        if bague1:
            self.hbox.addWidget(BaguePerfo(parent=self, width_value=bague1))
        cale2 = perfo.cale2
        if cale2:
            self.hbox.addWidget(EntretoisePerfo(parent=self, width_value=cale2))
        bague2 = perfo.bague2
        if bague2:
            self.hbox.addWidget(BaguePerfo(parent=self, width_value=bague2))
        cale3 = perfo.cale3
        if cale3:
            self.hbox.addWidget(EntretoisePerfo(parent=self, width_value=cale3))
        bague3 = perfo.bague3
        if bague3:
            self.hbox.addWidget(BaguePerfo(parent=self, width_value=bague3))
        cale4 = perfo.cale4
        if cale4:
            self.hbox.addWidget(EntretoisePerfo(parent=self, width_value=cale4))
        bague4 = perfo.bague4
        if bague4:
            self.hbox.addWidget(BaguePerfo(parent=self, width_value=bague4))
        cale5 = perfo.cale5
        if cale5:
            self.hbox.addWidget(EntretoisePerfo(parent=self, width_value=cale5))
        bague5 = perfo.bague5
        if bague5:
            self.hbox.addWidget(BaguePerfo(parent=self, width_value=bague5))
        cale6 = perfo.cale6
        if cale6:
            self.hbox.addWidget(EntretoisePerfo(parent=self, width_value=cale6))
        bague6 = perfo.bague6
        if bague6:
            self.hbox.addWidget(BaguePerfo(parent=self, width_value=bague6))
        cale7 = perfo.cale7
        if cale7:
            self.hbox.addWidget(EntretoisePerfo(parent=self, width_value=cale7))
        bague7 = perfo.bague7
        if bague7:
            self.hbox.addWidget(BaguePerfo(parent=self, width_value=bague7))
        self.hbox.addStretch(0)
        self.setLayout(self.hbox)
