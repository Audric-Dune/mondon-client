# !/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QPushButton

from constants.dimensions import (
    padding_button,
    width_windown_live_speed
)
from constants.stylesheets import button_stylesheet
from ui.application import app
from ui.widgets.chart.live_speed import LiveSpeed


class TrackerWindow(QMainWindow):
    def __init__(self, on_close):
        super(TrackerWindow, self).__init__(None)
        self.on_close = on_close
        self.live_speed = LiveSpeed(self)
        self.init_widget()
        self.bt_retour = QPushButton("", self)
        self.init_button()

    def init_widget(self):
        live_speed_width = width_windown_live_speed
        live_speed_height = 50
        self.live_speed.setGeometry(5, 5, live_speed_width-10, live_speed_height)

    @staticmethod
    def new_main_window():
        app.create_main_window()

    def init_button(self):
        little_button_size = 30
        size = QSize(little_button_size - padding_button, little_button_size - padding_button)
        self.bt_retour.clicked.connect(self.new_main_window)
        self.bt_retour.setStyleSheet(button_stylesheet)
        img = QIcon("assets/images/fleche_precedent.png")
        self.bt_retour.setIcon(img)
        self.bt_retour.setIconSize(size)
        self.bt_retour.setGeometry(width_windown_live_speed - little_button_size - 15,
                                   15,
                                   little_button_size,
                                   little_button_size)

    def closeEvent(self, event):
        self.on_close()
