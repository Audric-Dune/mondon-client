# !/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtCore import pyqtSignal

from commun.model.perfo import Perfo
from commun.ui.public.bague_perfo import BaguePerfo
from commun.ui.public.entretoise_perfo import EntretoisePerfo
from commun.ui.public.mondon_widget import MondonWidget
from commun.constants.colors import color_blanc


class PerfoUi(MondonWidget):
    ON_DBCLICK_SIGNAL = pyqtSignal(Perfo)

    def __init__(self, parent=None, perfo=None, ech=1):
        super(PerfoUi, self).__init__(parent=parent)
        self.set_background_color(color_blanc)
        self.ech = ech
        self.perfo = perfo
        self.setFixedWidth(980)
        self.hbox = QHBoxLayout()
        self.init_widget(perfo)

    def init_widget(self, perfo):
        self.hbox.setSpacing(0)
        self.hbox.setContentsMargins(0, 0, 0, 0)
        cale1 = perfo.cale1
        if cale1:
            self.hbox.addWidget(EntretoisePerfo(parent=self, width_value=cale1, ech=self.ech))
        bague1 = perfo.bague1
        if bague1:
            self.hbox.addWidget(BaguePerfo(parent=self, width_value=bague1, ech=self.ech))
        cale2 = perfo.cale2
        if cale2:
            self.hbox.addWidget(EntretoisePerfo(parent=self, width_value=cale2, ech=self.ech))
        bague2 = perfo.bague2
        if bague2:
            self.hbox.addWidget(BaguePerfo(parent=self, width_value=bague2, ech=self.ech))
        cale3 = perfo.cale3
        if cale3:
            self.hbox.addWidget(EntretoisePerfo(parent=self, width_value=cale3, ech=self.ech))
        bague3 = perfo.bague3
        if bague3:
            self.hbox.addWidget(BaguePerfo(parent=self, width_value=bague3, ech=self.ech))
        cale4 = perfo.cale4
        if cale4:
            self.hbox.addWidget(EntretoisePerfo(parent=self, width_value=cale4, ech=self.ech))
        bague4 = perfo.bague4
        if bague4:
            self.hbox.addWidget(BaguePerfo(parent=self, width_value=bague4, ech=self.ech))
        cale5 = perfo.cale5
        if cale5:
            self.hbox.addWidget(EntretoisePerfo(parent=self, width_value=cale5, ech=self.ech))
        bague5 = perfo.bague5
        if bague5:
            self.hbox.addWidget(BaguePerfo(parent=self, width_value=bague5, ech=self.ech))
        cale6 = perfo.cale6
        if cale6:
            self.hbox.addWidget(EntretoisePerfo(parent=self, width_value=cale6, ech=self.ech))
        bague6 = perfo.bague6
        if bague6:
            self.hbox.addWidget(BaguePerfo(parent=self, width_value=bague6, ech=self.ech))
        cale7 = perfo.cale7
        if cale7:
            self.hbox.addWidget(EntretoisePerfo(parent=self, width_value=cale7, ech=self.ech))
        bague7 = perfo.bague7
        if bague7:
            self.hbox.addWidget(BaguePerfo(parent=self, width_value=bague7, ech=self.ech))
        self.hbox.addStretch()
        self.setLayout(self.hbox)
