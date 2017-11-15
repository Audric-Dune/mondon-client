# !/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtCore import QSize

from constants.colors import color_bleu_gris

from constants.dimensions import padding_button

from constants.stylesheets import button_stylesheet

from ui.utils.drawing import draw_rectangle
from ui.widgets.mondon_widget import MondonWidget


class ArretWindowSelectType(MondonWidget):
    def __init__(self, parent=None):
        super(ArretWindowSelectType, self).__init__(parent=parent)
        self.update()
        self.bt_prevu = QPushButton("Arrêt prévu", self)
        self.bt_imprevu = QPushButton("Arrêt imprévu", self)
        self.init_button()

    def draw_fond(self, p):
        draw_rectangle(p, 0, 0, self.width(), self.height(), color_bleu_gris)

    def on_data_changed(self):
        self.update()

    def init_button(self):
        button_width = 100
        button_height = self.height()
        self.bt_prevu.setStyleSheet(button_stylesheet)
        self.bt_prevu.setGeometry(10,
                                  10,
                                  button_width,
                                  button_height)
        self.bt_imprevu.setStyleSheet(button_stylesheet)
        self.bt_imprevu.setGeometry(self.width()-10-button_width,
                                    10,
                                    button_width,
                                    button_height)

    def paintEvent(self, event):
        p = QPainter()
        p.begin(self)
        self.draw(p)
        p.end()

    def draw(self, p):
        self.draw_fond(p)
