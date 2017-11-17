# !/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QFormLayout, QPushButton, QLabel

from constants.colors import color_bleu_gris
from constants.param import LIST_CHOIX_RAISON_PREVU

from constants.dimensions import button_size

from constants.stylesheets import button_stylesheet, button_stylesheet_unselected, white_label_stylesheet

from ui.utils.drawing import draw_rectangle
from ui.widgets.mondon_widget import MondonWidget


class ArretWindowSelectRaison(MondonWidget):
    def __init__(self, arret, parent=None):
        super(ArretWindowSelectRaison, self).__init__(parent=parent)
        self.arret = arret
        self.raison_index_selected = None
        self.init_widget()

    def draw_fond(self, p):
        draw_rectangle(p, 0, 0, self.width(), self.height(), color_bleu_gris)

    def on_data_changed(self):
        self.update()

    @staticmethod
    def onclick(index):
        print(index)

    def connect_button(self, button, index):
        button.clicked.connect(lambda: self.onclick(index))

    def init_widget(self):
        list_label = LIST_CHOIX_RAISON_PREVU
        button = []
        qformlayout = QFormLayout()
        index = 0
        for label_text in list_label:
            button.append(QPushButton(str(index)))
            self.connect_button(button[index], index)
            label = QLabel(label_text)
            label.setStyleSheet(white_label_stylesheet)
            qformlayout.addRow(button[index], label)
            index += 1
        self.setLayout(qformlayout)

    def paintEvent(self, event):
        p = QPainter()
        p.begin(self)
        self.draw(p)
        p.end()

    def draw(self, p):
        self.draw_fond(p)
