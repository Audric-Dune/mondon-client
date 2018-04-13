# !/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QHBoxLayout, QLabel, QWidget
from PyQt5.QtCore import pyqtSignal

from commun.ui.public.mondon_widget import MondonWidget
from commun.ui.public.bobine_fille_ui import BobineFille
from commun.constants.colors import color_blanc


class LineRefente(MondonWidget):
    ON_DBCLICK_SIGNAL = pyqtSignal(QWidget)

    def __init__(self, parent=None, refente=None, ech=1, bobines=None):
        super(LineRefente, self).__init__(parent=parent)
        self.set_background_color(color_blanc)
        self.bobines = bobines
        self.ech = ech
        self.refente = refente
        self.hbox = QHBoxLayout()
        self.init_widget(refente)

    def init_widget(self, refente):
        self.hbox.setSpacing(0)
        label_perfo = QLabel("Perfo." + chr(96 + refente.code_perfo).capitalize())
        label_perfo.setFixedWidth(50)
        self.hbox.addWidget(label_perfo)
        number = 1
        for laize in refente.laizes:
            bobine_in_refente = self.get_bobine_from_laize(laize)
            if bobine_in_refente:
                self.del_bobine_in_list_bobines(bobine_in_refente)
            if laize:
                self.hbox.addWidget(BobineFille(parent=self, laize=laize, number=number, ech=self.ech, bobine=bobine_in_refente))
                number += 1
        self.hbox.addStretch(0)
        self.setLayout(self.hbox)

    def get_bobine_from_laize(self, laize):
        if self.bobines:
            for bobine in self.bobines:
                if bobine.laize == laize:
                    return bobine
        return None

    def del_bobine_in_list_bobines(self, bobine_to_del):
        new_bobines = []
        del_bobine = False
        for bobine in self.bobines:
            if bobine == bobine_to_del and not del_bobine:
                del_bobine = True
                pass
            else:
                new_bobines.append(bobine)
        self.bobines = new_bobines

    def mouseDoubleClickEvent(self, e):
        self.ON_DBCLICK_SIGNAL.emit(self.refente)
