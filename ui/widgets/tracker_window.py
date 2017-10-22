# !/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QMainWindow

from ui.widgets.live_speed import LiveSpeed


class TrackerWindow(QMainWindow):
    def __init__(self, parentApp, parent=None):
        super(TrackerWindow, self).__init__(parent)
        self.parentApp = parentApp

    def initialisation(self):
        live_speed = LiveSpeed(self)
        live_speed_width = 150
        live_speed_height = 50
        live_speed.setGeometry(5,
                               5,
                               live_speed_width,
                               live_speed_height)

    def closeEvent(self, event):
        self.parentApp.windows.remove(self)
        self.parentApp.on_close_window()
