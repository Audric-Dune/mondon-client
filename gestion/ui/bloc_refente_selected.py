# !/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QHBoxLayout, QLabel
from PyQt5.QtCore import pyqtSignal

from commun.utils.layout import clear_layout
from commun.constants.colors import color_bleu_gris, color_vert_moyen
from commun.ui.public.mondon_widget import MondonWidget
from gestion.ui.line_refente import LigneRefente


class BlocRefenteSelected(MondonWidget):
    ON_CLICK_SIGNAL = pyqtSignal(str)

    def __init__(self, parent=None):
        super(BlocRefenteSelected, self).__init__(parent=parent)
        self.background_color = color_bleu_gris
        self.master_hbox = QHBoxLayout()
        self.parent = parent
        self.init_ui()

    def init_ui(self):
        clear_layout(self.master_hbox)
        if self.parent.plan_prod.refente_selected:
            line_refente = LigneRefente(parent=self, refente=self.parent.plan_prod.refente_selected)
            self.master_hbox.addWidget(line_refente)
        else:
            label = QLabel("Refente")
            label.setFixedSize(650, 30)
            self.master_hbox.addWidget(label)
        self.setLayout(self.master_hbox)

    def update_widget(self):
        if self.parent.bloc_focus == "refente":
            self.background_color = color_vert_moyen
        else:
            self.background_color = color_bleu_gris
        self.init_ui()
        self.update()

    def mouseReleaseEvent(self, e):
        self.ON_CLICK_SIGNAL.emit("refente")
