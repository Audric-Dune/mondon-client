# !/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtCore import pyqtSignal

from commun.model.perfo import Perfo
from commun.ui.public.bobine_fille_ui import BobineFille
from commun.ui.public.mondon_widget import MondonWidget
from commun.constants.colors import color_blanc


class RefenteUi(MondonWidget):
    ON_DBCLICK_SIGNAL = pyqtSignal(Perfo)

    def __init__(self, parent=None, refente=None, ech=1):
        super(RefenteUi, self).__init__(parent=parent)
        self.set_background_color(color_blanc)
        self.ech = ech
        self.refente = refente
        self.hbox = QHBoxLayout()
        self.init_widget(refente)

    def init_widget(self, refente):
        self.hbox.setSpacing(0)
        self.hbox.setContentsMargins(0, 0, 0, 0)
        number = 1
        for laize in refente.laizes:
            if laize:
                self.hbox.addWidget(BobineFille(parent=self, laize=laize, number=number))
            number += 1
        self.setLayout(self.hbox)
