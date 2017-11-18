# !/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QPushButton, QHBoxLayout

from constants.colors import color_bleu_gris

from constants.dimensions import button_size

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
        self.init_widget()

    def draw_fond(self, p):
        draw_rectangle(p, 0, 0, self.width(), self.height(), color_bleu_gris)

    def on_data_changed(self):
        self.update()

    def on_click_bt_prevu(self):
        self.bt_prevu.setStyleSheet(button_stylesheet)
        self.bt_imprevu.setStyleSheet(button_stylesheet_unselected)
        if self.arret.type_cache == "Prévu":
            self.bt_prevu.setStyleSheet(button_stylesheet)
            self.bt_imprevu.setStyleSheet(button_stylesheet)
        self.arret.add_type_cache("Prévu")

    def on_click_bt_imprevu(self):
        self.bt_prevu.setStyleSheet(button_stylesheet_unselected)
        self.bt_imprevu.setStyleSheet(button_stylesheet)
        if self.arret.type_cache == "Imprévu":
            self.bt_prevu.setStyleSheet(button_stylesheet)
            self.bt_imprevu.setStyleSheet(button_stylesheet)
        self.arret.add_type_cache("Imprévu")

    def init_widget(self):
        hbox = QHBoxLayout()
        self.bt_prevu.setFixedSize(200, button_size)
        self.bt_prevu.setStyleSheet(button_stylesheet)
        hbox.addWidget(self.bt_prevu)
        self.bt_imprevu.setFixedSize(200, button_size)
        self.bt_imprevu.setStyleSheet(button_stylesheet)
        hbox.addWidget(self.bt_imprevu)

        self.setLayout(hbox)

    def paintEvent(self, event):
        p = QPainter()
        p.begin(self)
        self.draw(p)
        p.end()

    def draw(self, p):
        self.draw_fond(p)
