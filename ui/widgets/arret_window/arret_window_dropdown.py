# !/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QHBoxLayout
from ui.widgets.public.mondon_widget import MondonWidget

from constants.colors import color_bleu_gris
from ui.utils.drawing import draw_rectangle
from ui.widgets.public.dropdown import Dropdown


class ArretWindowDropdown(MondonWidget):
    def __init__(self, parent=None):
        super(ArretWindowDropdown, self).__init__(parent=parent)
        self.init_widget()

    def init_widget(self):
        hbox = QHBoxLayout()
        dropdown = Dropdown(parent=self)
        dropdown.setFixedWidth(300)
        dropdown.set_placeholder("Sélectionner un castor")
        dropdown.add_item("Test1")
        dropdown.add_item("Test2")
        dropdown.add_item("Test3")
        dropdown.add_item("Test4")
        dropdown.add_item("Castor")
        hbox.addWidget(dropdown)
        self.setLayout(hbox)

    def draw_fond(self, p):
        draw_rectangle(p, 0, 0, self.width(), self.height(), color_bleu_gris)

    def paintEvent(self, event):
        p = QPainter()
        p.begin(self)
        self.draw(p)
        p.end()

    def draw(self, p):
        self.draw_fond(p)
