# !/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QPushButton, QHBoxLayout

from constants.colors import color_bleu_gris
from constants.dimensions import button_size
from constants.stylesheets import button_stylesheet
from ui.utils.drawing import draw_rectangle
from ui.widgets.public.mondon_widget import MondonWidget


class ArretWindowValidation(MondonWidget):
    def __init__(self, parent=None):
        super(ArretWindowValidation, self).__init__(parent=parent)
        self.bt_validation = QPushButton("Validation", self)
        self.bt_validation.clicked.connect(self.on_click_bt_validation)
        self.init_widget()

    def draw_fond(self, p):
        draw_rectangle(p, 0, 0, self.width(), self.height(), color_bleu_gris)

    def on_data_changed(self):
        self.update()

    def on_click_bt_validation(self):
        print("VALIDATION_CLICK")

    def init_widget(self):
        hbox = QHBoxLayout()
        self.bt_validation.setFixedSize(200, button_size)
        self.bt_validation.setStyleSheet(button_stylesheet)
        hbox.addWidget(self.bt_validation)

        self.setLayout(hbox)

    def paintEvent(self, event):
        p = QPainter()
        p.begin(self)
        self.draw(p)
        p.end()

    def draw(self, p):
        self.draw_fond(p)
