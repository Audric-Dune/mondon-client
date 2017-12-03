# !/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtCore import QSize
from PyQt5.QtGui import QPainter, QIcon
from PyQt5.QtWidgets import QPushButton

from constants.colors import (
    color_blanc,
    color_bleu_gris,
)
from constants.dimensions import (
    button_size,
    padding_button,
    chart_menu_height,
)
from constants.stylesheets import button_stylesheet
from stores.settings_store import settings_store
from ui.application import app
from ui.utils.drawing import draw_rectangle, draw_text
from ui.utils.timestamp import timestamp_at_day_ago, timestamp_to_date
from ui.widgets.chart.live_speed import LiveSpeed
from ui.widgets.public.mondon_widget import MondonWidget
from ui.widgets.public.pixmap_button import PixmapButton


class ChartMenu(MondonWidget):
    def __init__(self, parent):
        super(ChartMenu, self).__init__(parent=parent)
        self.day_ago = 0
        self.zoom = 0
        self.bt_jour_plus = PixmapButton(parent=self)
        self.bt_jour_moins = PixmapButton(parent=self)
        self.bt_zoom_plus = PixmapButton(parent=self)
        self.bt_zoom_moins = PixmapButton(parent=self)
        self.bt_live = QPushButton("En direct", self)
        self.init_widget()
        self.update_button()

    def on_settings_changed(self, prev_live, prev_day_ago, prev_zoom):
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
        text_width = 450
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

    @staticmethod
    def create_window_live_speed(event):
        app.create_tracker_window()

    def update_button(self):
        self.bt_jour_plus.setEnabled(self.day_ago > 0)
        self.bt_zoom_moins.setEnabled(self.zoom > 1)
        self.bt_zoom_plus.setEnabled(32 > self.zoom)

    def set_buttons_geometry(self):
        self.bt_jour_plus.setGeometry((self.width() - button_size + 450) / 2,
                                      (self.height() - button_size) / 2,
                                      button_size,
                                      button_size)
        self.bt_jour_moins.setGeometry((self.width() - button_size - 450) / 2,
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

    def init_button(self):
        # Bouton jour plus
        self.bt_jour_plus.clicked.connect(self.jour_plus)
        self.bt_jour_plus.setStyleSheet(button_stylesheet)
        self.bt_jour_plus.set_image("assets/images/fleche_suivant.png")

        # Bouton jour moins
        self.bt_jour_moins.clicked.connect(self.jour_moins)
        self.bt_jour_moins.setStyleSheet(button_stylesheet)
        self.bt_jour_moins.set_image("assets/images/fleche_precedent.png")

        # Bouton zoom plus
        self.bt_zoom_plus.clicked.connect(self.zoom_plus)
        self.bt_zoom_plus.setStyleSheet(button_stylesheet)
        self.bt_zoom_plus.set_image("assets/images/zoom_plus.png")

        # Bouton zoom moins
        self.bt_zoom_moins.clicked.connect(self.zoom_moins)
        self.bt_zoom_moins.setStyleSheet(button_stylesheet)
        self.bt_zoom_moins.set_image("assets/images/zoom_moins.png")

        # Bouton live
        self.bt_live.clicked.connect(self.live)
        self.bt_live.setStyleSheet(button_stylesheet)

    def init_widget(self):
        self.init_button()
        live_speed = LiveSpeed(self)
        live_speed.mouseDoubleClickEvent = self.create_window_live_speed
        live_speed_width = 180
        live_speed_height = 50
        live_speed.setGeometry(150,
                               (chart_menu_height - live_speed_height) / 2,
                               live_speed_width,
                               live_speed_height)

    def draw(self, p):
        self.draw_fond(p)
        self.draw_date(p)
        self.set_buttons_geometry()
