# !/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout
# from ui.widgets.arret_window.arret_window_dropdown import ArretWindowDropdown
from ui.widgets.arret_window.arret_window_title import ArretWindowTitle
from ui.widgets.arret_window.arret_window_select_raison import ArretWindowSelectRaison
from ui.widgets.arret_window.arret_window_select_type import ArretWindowSelectType


class ArretWindow(QMainWindow):
    def __init__(self, on_close, arret):
        super(ArretWindow, self).__init__(None)
        arret.ARRET_TYPE_CHANGED_SIGNAL.connect(self.update_widget)
        self.arret = arret
        self.on_close = on_close
        self.central_widget = QWidget(self)
        self.vbox = QVBoxLayout(self.central_widget)
        self.arret_window_title = ArretWindowTitle(self.arret, parent=self.central_widget)
        self.arret_window_select_type = ArretWindowSelectType(self.arret, parent=self.central_widget)
        self.arret_window_raison = None
        self.last_type_selected = None
        self.init_widget()

    def init_widget(self):
        self.arret_window_title.setFixedHeight(60)
        self.vbox.addWidget(self.arret_window_title)
        self.vbox.addWidget(self.arret_window_select_type)

        self.central_widget.setLayout(self.vbox)
        self.setCentralWidget(self.central_widget)

    def update_widget(self):
        if not self.arret_window_raison:
            self.arret_window_raison = ArretWindowSelectRaison(self.arret, parent=self.central_widget)
            self.vbox.addWidget(self.arret_window_raison)
            self.last_type_selected = self.arret.type_cache
        elif self.arret.type_cache == self.last_type_selected:
            self.vbox.removeWidget(self.arret_window_raison)
            self.arret_window_raison.deleteLater()
            self.arret.remove_type()
            self.arret.remove_raison()
            self.arret_window_raison = None
            self.last_type_selected = None
        else:
            self.vbox.removeWidget(self.arret_window_raison)
            self.arret_window_raison.deleteLater()
            self.arret.remove_raison()
            self.arret_window_raison = ArretWindowSelectRaison(self.arret, parent=self.central_widget)
            self.vbox.addWidget(self.arret_window_raison)
            self.last_type_selected = self.arret.type_cache
        # Utilisation d'un QTimer pour redimensionner la window
        QTimer.singleShot(0, self.resize_window)

    def resize_window(self):
        self.setFixedSize(self.minimumSizeHint())

    def closeEvent(self, event):
        self.on_close(self.arret.start)
