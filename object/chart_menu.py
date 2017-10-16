# !/usr/bin/env python
# -*- coding: utf-8 -*-

# Importation des module PyQt5
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtCore import Qt, QRectF, QTimer, QSize
from PyQt5.QtGui import QBrush, QColor, QPainter, QPen, QIcon
from param.param import *
from object.data_store_manager import *
from object.settings_store import *
from fonction.gestion_timestamp import *
from fonction.draw_fonction import draw_rectangle, draw_text


class ChartMenu(QWidget):
    def __init__(self, parent):
        super(ChartMenu, self).__init__(parent=parent)
        settings_store.add_listener(self.get_setting)
        self.day_ago = 0
        self.zoom = 0
        self.draw_button()
        self.update_button()

    def get_setting(self, prev_live, prev_day_ago, prev_zoom):
        self.day_ago = settings_store.day_ago
        self.zoom = settings_store.zoom
        self.update_button()
        self.update()

    def paintEvent(self, event):
        p = QPainter()
        p.begin(self)
        self.draw(p)
        p.end()

    def draw_fond(self, p):
        draw_rectangle(p, 0, 0, self.width(), self.height(), color_bleu_gris)

    def draw_date(self, p):
        ts = timestamp_at_day_ago(self.day_ago)
        date = timestamp_to_date(ts)
        text_width = 400
        text_height = 50
        draw_text(p,
                  x=(self.width() - text_width) / 2,
                  y=(self.height() - text_height) / 2,
                  width=text_width,
                  height=text_height,
                  color=color_blanc,
                  align="C",
                  font_size=22,
                  text=date)

    @staticmethod
    def zoom_moins():
        new_zoom = max(1, settings_store.zoom / 2)
        settings_store.set_zoom(new_zoom)

    @staticmethod
    def zoom_plus():
        settings_store.set_zoom(settings_store.zoom * 2)

    @staticmethod
    def jour_moins():
        settings_store.set_day_ago(settings_store.day_ago + 1)

    @staticmethod
    def jour_plus():
        settings_store.set_day_ago(settings_store.day_ago - 1)

    @staticmethod
    def live():
        settings_store.set_day_ago(0)

    def update_button(self):
        self.bt_jour_plus.setEnabled(self.day_ago > 0)
        self.bt_zoom_moins.setEnabled(self.zoom > 1)
        self.bt_zoom_plus.setEnabled(32 > self.zoom)

    def set_buttons_geometry(self):
        self.bt_jour_plus.setGeometry((self.width() - button_size + 400) / 2,
                                      (self.height() - button_size) / 2,
                                      button_size,
                                      button_size)
        self.bt_jour_moins.setGeometry((self.width() - button_size - 400) / 2,
                                       (self.height() - button_size) / 2,
                                       button_size,
                                       button_size)
        self.bt_zoom_plus.setGeometry(self.width() - 50,
                                      (self.height() - button_size) / 2,
                                      button_size,
                                      button_size)
        self.bt_zoom_moins.setGeometry(self.width() - 100,
                                       (self.height() - button_size) / 2,
                                       button_size,
                                       button_size)
        self.bt_live.setGeometry(10,
                                (self.height() - button_size) / 2,
                                100,
                                button_size)

    def draw_button(self):
        size = QSize(button_size - padding_button, button_size - padding_button)
        # Bouton jour plus
        self.bt_jour_plus = QPushButton("", self)
        self.bt_jour_plus.clicked.connect(self.jour_plus)
        self.bt_jour_plus.setStyleSheet(style_button)
        img = QIcon("img/fleche_suivant.png")
        self.bt_jour_plus.setIconSize(size)
        self.bt_jour_plus.setIcon(img)

        # Bouton jour moins
        self.bt_jour_moins = QPushButton("", self)
        self.bt_jour_moins.clicked.connect(self.jour_moins)
        self.bt_jour_moins.setStyleSheet(style_button)
        img = QIcon("img/fleche_precedent.png")
        self.bt_jour_moins.setIcon(img)
        self.bt_jour_moins.setIconSize(size)

        # Bouton zoom plus
        self.bt_zoom_plus = QPushButton("", self)
        self.bt_zoom_plus.clicked.connect(self.zoom_plus)
        self.bt_zoom_plus.setStyleSheet(style_button)
        img = QIcon("img/zoom_plus.png")
        self.bt_zoom_plus.setIcon(img)
        self.bt_zoom_plus.setIconSize(size)

        # Bouton zoom moins
        self.bt_zoom_moins = QPushButton("", self)
        self.bt_zoom_moins.clicked.connect(self.zoom_moins)
        self.bt_zoom_moins.setStyleSheet(style_button)
        img = QIcon("img/zoom_moins.png")
        self.bt_zoom_moins.setIcon(img)
        self.bt_zoom_moins.setIconSize(size)

        # Bouton live
        self.bt_live = QPushButton("En direct", self)
        self.bt_live.clicked.connect(self.live)
        self.bt_live.setStyleSheet(style_button)

    def draw(self, p):
        self.draw_fond(p)
        self.draw_date(p)
        self.set_buttons_geometry()
