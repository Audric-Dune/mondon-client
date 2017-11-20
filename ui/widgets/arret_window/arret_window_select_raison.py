# !/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtCore import QSize
from PyQt5.QtGui import QPainter, QIcon
from PyQt5.QtWidgets import QPushButton, QLabel, QHBoxLayout, QVBoxLayout

from constants.colors import color_bleu_gris
from constants.param import LIST_CHOIX_RAISON_PREVU, LIST_CHOIX_RAISON_IMPREVU
from constants.stylesheets import \
    check_box_off_stylesheet, \
    check_box_on_stylesheet, \
    check_box_unselected_stylesheet, \
    white_title_label_stylesheet, \
    disable_16_label_stylesheet
from ui.utils.drawing import draw_rectangle
from ui.widgets.public.dropdown import Dropdown
from ui.widgets.public.mondon_widget import MondonWidget


class ArretWindowSelectRaison(MondonWidget):
    def __init__(self, arret, parent=None):
        super(ArretWindowSelectRaison, self).__init__(parent=parent)
        arret.ARRET_RAISON_CHANGED_SIGNAL.connect(self.update_widget)
        self.arret = arret
        self.list_choix = LIST_CHOIX_RAISON_PREVU if self.arret.type_cache == "Prévu" else LIST_CHOIX_RAISON_IMPREVU
        self.items = []
        self.buttons = []
        self.raison_index_selected = -1
        self.last_raison_index = -1
        self.text_drop_down_selected = None
        self.vbox = QVBoxLayout()
        self.init_widget()

    def draw_fond(self, p):
        draw_rectangle(p, 0, 0, self.width(), self.height(), color_bleu_gris)

    def on_data_changed(self):
        self.update()

    def update_widget(self):
        print("update_widget")
        index = 0
        while index < len(self.buttons):
            print(index)
            if self.raison_index_selected < 0:
                self.buttons[index].setStyleSheet(check_box_off_stylesheet)
                self.buttons[index].setIcon(QIcon())
                if self.items[index][0] == "label":
                    self.items[index][1].setStyleSheet(white_title_label_stylesheet)
                if self.items[index][0] == "dropdown":
                    self.items[index][1].set_activated(False)
            elif self.raison_index_selected == index:
                self.buttons[index].setStyleSheet(check_box_on_stylesheet)
                img = QIcon("assets/images/white_cross.png")
                self.buttons[index].setIcon(img)
                size = QSize(24, 24)
                self.buttons[index].setIconSize(size)
                if self.items[index][0] == "label":
                    self.items[index][1].setStyleSheet(white_title_label_stylesheet)
                if self.items[index][0] == "dropdown":
                    self.items[index][1].set_activated(True)
            else:
                self.buttons[index].setStyleSheet(check_box_unselected_stylesheet)
                self.buttons[index].setIcon(QIcon())
                if self.items[index][0] == "label":
                    self.items[index][1].setStyleSheet(disable_16_label_stylesheet)
                if self.items[index][0] == "dropdown":
                    self.items[index][1].set_activated(False)
            index += 1

    def onclick(self, index):
        self.raison_index_selected = index
        if self.last_raison_index == index:
            self.raison_index_selected = -1
            self.last_raison_index = -1
        else:
            self.last_raison_index = index
        self.text_drop_down_selected = None
        self.arret.add_raison_cache(index, None)

    def connect_button(self, button, index):
        button.clicked.connect(lambda: self.onclick(index))

    def style_choice(self, text):
        self.text_drop_down_selected = text
        self.arret.add_raison_cache(self.raison_index_selected, text)

    def init_widget(self):
        index = 0
        for tupple in self.list_choix:
            format = tupple[0]
            value = tupple[1]
            if format == "label":
                self.items.append((format, self.create_label(value)))
                self.buttons.append(self.create_check_button(index))
            elif format == "dropdown":
                self.items.append((format, self.create_dropdown(value[1], value[0])))
                self.buttons.append(self.create_check_button(index))
            hbox = QHBoxLayout()
            hbox.addWidget(self.buttons[index])
            hbox.addWidget(self.items[index][1])
            hbox.addStretch(1)
            self.vbox.addLayout(hbox)
            index += 1
        self.setLayout(self.vbox)

    def create_check_button(self, index):
        button = QPushButton("")
        button.setFixedSize(24, 24)
        button.setStyleSheet(check_box_off_stylesheet)
        self.connect_button(button, index)
        return button

    @staticmethod
    def create_label(text):
        label = QLabel(text)
        label.setStyleSheet(white_title_label_stylesheet)
        return label

    def create_dropdown(self, array, placeholder=None):
        dropdown = Dropdown()
        if placeholder:
            dropdown.set_placeholder(placeholder)
        for value in array:
            dropdown.add_item(value)
        # dropdown.activated[str].connect(self.style_choice)
        dropdown.set_activated(False)
        return dropdown

    def paintEvent(self, event):
        p = QPainter()
        p.begin(self)
        self.draw(p)
        p.end()

    def draw(self, p):
        self.draw_fond(p)
