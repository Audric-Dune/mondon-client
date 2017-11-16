# !/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QPushButton

from constants.colors import color_bleu_gris

from constants.dimensions import padding_button, window_arret_width, button_size

from constants.stylesheets import button_stylesheet, button_stylesheet_unselected

from ui.utils.drawing import draw_rectangle
from ui.widgets.mondon_widget import MondonWidget


class ArretWindowSelectType(MondonWidget):
    def __init__(self, arret, parent=None):
        super(ArretWindowSelectType, self).__init__(parent=parent)
        self.arret = arret
        self.type_selected = None
        self.bt_prevu = QPushButton("Arrêt prévu", self)
        self.bt_prevu.clicked.connect(self.on_click_bt_prevu)
        self.bt_imprevu = QPushButton("Arrêt imprévu", self)
        self.bt_imprevu.clicked.connect(self.on_click_bt_imprevu)
        self.init_button()

    def draw_fond(self, p):
        draw_rectangle(p, 0, 0, self.width(), self.height(), color_bleu_gris)

    def on_data_changed(self):
        self.update()

    def on_click_bt_prevu(self):
        self.bt_prevu.setStyleSheet(button_stylesheet)
        self.bt_imprevu.setStyleSheet(button_stylesheet_unselected)
        self.arret.add_type_cache("Prévu")

    def on_click_bt_imprevu(self):
        self.bt_prevu.setStyleSheet(button_stylesheet_unselected)
        self.bt_imprevu.setStyleSheet(button_stylesheet)
        self.arret.add_type_cache("Imprévu")

    def init_button(self):
        button_width = 200
        button_height = button_size
        self.bt_prevu.setStyleSheet(button_stylesheet)
        self.bt_prevu.setGeometry(padding_button*2,
                                  15,
                                  button_width,
                                  button_height)
        self.bt_imprevu.setStyleSheet(button_stylesheet)
        self.bt_imprevu.setGeometry(window_arret_width-padding_button*3-button_width,
                                    15,
                                    button_width,
                                    button_height)

    def paintEvent(self, event):
        p = QPainter()
        p.begin(self)
        self.draw(p)
        p.end()

    def draw(self, p):
        self.draw_fond(p)
