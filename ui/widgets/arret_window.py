# !/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QMainWindow

from constants.dimensions import (
    width_windown_live_speed
)

from ui.widgets.live_speed import LiveSpeed


class ArretWindow(QMainWindow):
    def __init__(self, on_close):
        super(ArretWindow, self).__init__(None)
        # self.arret = arret
        self.live_speed = LiveSpeed(self)
        self.on_close = on_close
        self.init_widget()

    def init_widget(self):
        live_speed_width = width_windown_live_speed
        live_speed_height = 50
        self.live_speed.setGeometry(5, 5, live_speed_width-10, live_speed_height)

    def closeEvent(self, event):
        # self.on_close(self.arret.start)
        pass
