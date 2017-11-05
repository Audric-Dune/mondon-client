# !/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QMainWindow, QPushButton

from constants.dimensions import padding_arret, window_arret_width

from ui.application import app
from ui.widgets.arret_window_title import ArretWindowTitle
from ui.widgets.arret_window_select_type import ArretWindowSelectType


class ArretWindow(QMainWindow):
    def __init__(self, on_close, arret):
        super(ArretWindow, self).__init__(None)
        self.arret = arret
        self.arret_window_title = ArretWindowTitle(self)
        self.arret_window_select_type = ArretWindowSelectType(self)
        self.on_close = on_close
        self.init_widget()

    def init_widget(self):
        self.arret_window_title.setGeometry(padding_arret,
                                            padding_arret,
                                            window_arret_width-padding_arret*2,
                                            60-padding_arret*2)
        self.arret_window_select_type.setGeometry(padding_arret,
                                                  60,
                                                  window_arret_width-padding_arret*2,
                                                  80-padding_arret*2)

    def test(self):
        app.agrandi_arret_window(self.arret.start)

    def closeEvent(self, event):
        self.on_close(self.arret.start)
