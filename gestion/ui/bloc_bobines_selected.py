# !/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QHBoxLayout, QLabel
from PyQt5.QtCore import pyqtSignal

from commun.constants.colors import color_bleu_gris, color_vert_moyen
from commun.ui.public.mondon_widget import MondonWidget


class BlocBobinesSelected(MondonWidget):
    ON_CLICK_SIGNAL = pyqtSignal(str)

    def __init__(self, parent=None):
        super(BlocBobinesSelected, self).__init__(parent=parent)
        self.background_color = color_vert_moyen
        self.parent = parent
        self.init_ui()

    def init_ui(self):
        master_hbox = QHBoxLayout()
        label = QLabel("Bobines filles")
        label.setFixedSize(650, 30)
        master_hbox.addWidget(label)
        self.setLayout(master_hbox)

    def update_widget(self):
        if self.parent.bloc_focus == "bobine":
            self.background_color = color_vert_moyen
        else:
            self.background_color = color_bleu_gris
        self.update()

    def mouseReleaseEvent(self, e):
        self.ON_CLICK_SIGNAL.emit("bobine")
