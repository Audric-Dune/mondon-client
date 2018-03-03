# !/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QHBoxLayout, QLabel, QWidget
from PyQt5.QtCore import pyqtSignal
from commun.ui.public.mondon_widget import MondonWidget
from commun.ui.public.bobine_fille_vide import BobineFilleVide


class LigneRefente(MondonWidget):
    ON_DBCLICK_SIGNAL = pyqtSignal(QWidget)

    def __init__(self, parent=None, refente=None):
        super(LigneRefente, self).__init__(parent=parent)
        self.refente = refente
        self.hbox = QHBoxLayout()
        self.init_widget(refente)

    def init_widget(self, refente):
        self.hbox.setSpacing(0)
        label_perfo = QLabel("Perfo." + chr(96 + refente.code_perfo).capitalize())
        label_perfo.setFixedWidth(50)
        self.hbox.addWidget(label_perfo)
        laize1 = refente.laize1
        if laize1:
            self.hbox.addWidget(BobineFilleVide(parent=self, laize=laize1, number=1))
        laize2 = refente.laize2
        if laize2:
            self.hbox.addWidget(BobineFilleVide(parent=self, laize=laize2, number=2))
        laize3 = refente.laize3
        if laize3:
            self.hbox.addWidget(BobineFilleVide(parent=self, laize=laize3, number=3))
        laize4 = refente.laize4
        if laize4:
            self.hbox.addWidget(BobineFilleVide(parent=self, laize=laize4, number=4))
        laize5 = refente.laize5
        if laize5:
            self.hbox.addWidget(BobineFilleVide(parent=self, laize=laize5, number=5))
        laize6 = refente.laize6
        if laize6:
            self.hbox.addWidget(BobineFilleVide(parent=self, laize=laize6, number=6))
        laize7 = refente.laize7
        if laize7:
            self.hbox.addWidget(BobineFilleVide(parent=self, laize=laize7, number=7))
        self.hbox.addStretch(0)
        self.setLayout(self.hbox)

    def mouseDoubleClickEvent(self, e):
        self.ON_DBCLICK_SIGNAL.emit(self.refente)
