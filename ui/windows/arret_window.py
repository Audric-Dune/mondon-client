# !/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout

from constants.dimensions import padding_arret, window_arret_width

from ui.widgets.arret_window_title import ArretWindowTitle
from ui.widgets.arret_window_select_type import ArretWindowSelectType


class ArretWindow(QMainWindow):
    def __init__(self, on_close, arret):
        super(ArretWindow, self).__init__(None)
        arret.ARRET_CHANGED_SIGNAL.connect(self.update_widget)
        self.arret = arret
        self.on_close = on_close
        self.central_widget = QWidget(self)
        self.vbox = QVBoxLayout(self.central_widget)
        self.arret_window_title = ArretWindowTitle(self.arret, parent=self.central_widget)
        self.arret_window_select_type = ArretWindowSelectType(self.arret, parent=self.central_widget)
        self.init_widget()

    def init_widget(self):
        self.arret_window_title.setFixedHeight(60)
        self.vbox.addWidget(self.arret_window_title)
        self.vbox.addWidget(self.arret_window_select_type)

        self.central_widget.setLayout(self.vbox)
        self.setCentralWidget(self.central_widget)

    def update_widget(self):
        pass

    def closeEvent(self, event):
        self.on_close(self.arret.start)
