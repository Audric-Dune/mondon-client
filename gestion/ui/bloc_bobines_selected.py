# !/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QVBoxLayout, QLabel
from PyQt5.QtCore import pyqtSignal

from commun.constants.colors import color_bleu_gris, color_vert_moyen
from commun.ui.public.mondon_widget import MondonWidget
from commun.utils.layout import clear_layout
from gestion.ui.line_bobine import LineBobine


class BlocBobinesSelected(MondonWidget):
    ON_CLICK_SIGNAL = pyqtSignal(str)

    def __init__(self, parent=None):
        super(BlocBobinesSelected, self).__init__(parent=parent)
        self.background_color = color_vert_moyen
        self.parent = parent
        self.master_hbox = QVBoxLayout()
        self.init_ui()

    def init_ui(self):
        clear_layout(self.master_hbox)
        if self.parent.plan_prod.bobine_fille_selected:
            for bobine in self.parent.plan_prod.bobine_fille_selected:
                line_bobine = LineBobine(parent=self, bobine=bobine)
                self.master_hbox.addWidget(line_bobine)
        else:
            label = QLabel("Bobines filles")
            label.setFixedSize(650, 30)
            self.master_hbox.addWidget(label)
        self.setLayout(self.master_hbox)

    def update_widget(self):
        if self.parent.bloc_focus == "bobine" or not self.parent.bloc_focus:
            self.background_color = color_vert_moyen
        else:
            self.background_color = color_bleu_gris
        self.init_ui()
        self.update()

    def mouseReleaseEvent(self, e):
        self.ON_CLICK_SIGNAL.emit("bobine")
