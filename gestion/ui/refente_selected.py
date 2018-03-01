# !/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QVBoxLayout
from commun.constants.colors import color_bleu_gris
from commun.ui.public.mondon_widget import MondonWidget


class RefenteSelected(MondonWidget):

    def __init__(self, plan_prod, parent=None):
        super(RefenteSelected, self).__init__(parent=parent)
        self.background_color = color_bleu_gris
        self.plan_prod = plan_prod
        self.master_vbox = QVBoxLayout()
        self.init_widget()

    def init_widget(self):
        self.master_vbox.addWidget(self.init_dropdown())
        self.setLayout(self.master_vbox)

    def init_dropdown(self):
        from commun.ui.public.dropdown import Dropdown
        dropdown = Dropdown(parent=self)
        for refente in self.plan_prod.refente_store.refentes:
            dropdown.add_item(self.get_label_from_renfente(refente))
        return dropdown

    @staticmethod
    def get_label_from_renfente(refente):
        code_perfo = refente.code_perfo
        label = "Perfo." + chr(96+code_perfo).capitalize()
        laize1 = refente.laize1
        if laize1:
            label += "  " + str(laize1)
        laize2 = refente.laize2
        if laize2:
            label += "-" + str(laize2)
        laize3 = refente.laize3
        if laize3:
            label += "-" + str(laize3)
        laize4 = refente.laize4
        if laize4:
            label += "-" + str(laize4)
        laize5 = refente.laize5
        if laize5:
            label += "-" + str(laize5)
        laize6 = refente.laize6
        if laize6:
            label += "-" + str(laize6)
        laize7 = refente.laize7
        if laize7:
            label += "-" + str(laize7)
        return label
