# !/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtCore import pyqtSignal

from commun.model.perfo import Perfo
from commun.ui.public.bobine_fille_selected_ui import BobineFilleSelected
from commun.ui.public.bobine_fille_ui import BobineFille
from commun.ui.public.mondon_widget import MondonWidget
from commun.constants.colors import color_blanc


class RefenteUi(MondonWidget):

    def __init__(self, parent=None, refente=None, bobines_selected=None, ech=1):
        super(RefenteUi, self).__init__(parent=parent)
        self.set_background_color(color_blanc)
        self.ech = ech
        self.refente = refente
        self.hbox = QHBoxLayout()
        self.bobines_selected = bobines_selected
        self.init_widget(refente)

    def init_widget(self, refente):
        print("__________ init_widget __________")
        self.hbox.setSpacing(0)
        self.hbox.setContentsMargins(0, 0, 0, 0)
        index = 0
        while index < len(refente.laizes):
            laize = refente.laizes[index]
            if laize:
                bobine_selected = self.get_bobine_for_index_in_laize(index=index, laize=laize)
                if bobine_selected:
                    self.hbox.addWidget(BobineFilleSelected(parent=self, bobine_selected=bobine_selected))
                    bobine_selected.index = index
                    index += bobine_selected.pose if bobine_selected.pose else 1
                else:
                    self.hbox.addWidget(BobineFille(parent=self, laize=laize, number=index+1))
                    index += 1
            else:
                index += 1
        self.hbox.addStretch()
        self.setLayout(self.hbox)

    def get_bobine_for_index_in_laize(self, index, laize):
        if self.bobines_selected is None:
            return False
        for bobine in self.bobines_selected:
            if bobine.index == index:
                return bobine
        for bobine in self.bobines_selected:
            if bobine.laize == laize and bobine.index is None:
                if self.is_valid_bobine_in_refente_at_index(bobine=bobine, index=index):
                    return bobine
                else:
                    continue
        return False

    def is_valid_bobine_in_refente_at_index(self, bobine, index):
        init_index = index
        if bobine.pose == 0:
            return True
        while index < init_index+bobine.pose:
            if bobine.laize == self.refente.laizes[index]:
                index += 1
            else:
                return False
        return True
