# !/usr/bin/env python
# -*- coding: utf-8 -*-

from lib.logger import logger

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication

from constants.dimensions import window_height, window_width, width_windown_live_speed
from stores.data_store_manager import data_store_manager


class Application(QApplication):

    def __init__(self, argv=[]):
        super(Application, self).__init__(argv)
        self.main_window = None
        self.tracker_window = None

    def on_close_main_window(self):
        self.main_window = None
        self.close_data_store_manager()

    def on_close_tracker_window(self):
        self.tracker_window = None
        self.close_data_store_manager()

    def close_data_store_manager(self):
        # Fonction qui se charge de stopper le refresh data lorsque
        # la derniere fenetre de l'application est fermée
        if not self.main_window and self.tracker_window:
            data_store_manager.cancel_refresh()

    @staticmethod
    def focus_window(window):
        window.setWindowState(window.windowState() & ~Qt.WindowMinimized | Qt.WindowActive)
        window.raise_()
        window.activateWindow()

    def create_main_window(self):
        if self.main_window:
            self.focus_window(self.main_window)
        else:
            from ui.widgets.main_window import MainWindow
            logger.log("INITIALISATION", "Création de la Window")
            self.main_window = MainWindow(self.on_close_main_window)

            logger.log("INITIALISATION", "Configuration de la Window")
            self.main_window.initialisation()
            self.main_window.setWindowTitle("DUNE Production bobine")
            self.main_window.resize(window_width, window_height)
            self.main_window.setMinimumSize(window_width, window_height)

            logger.log("INITIALISATION", "Affichage de MainWindow")
            self.main_window.show()

    def create_tracker_window(self):
        if self.tracker_window:
            self.focus_window(self.tracker_window)
        else:
            from ui.widgets.tracker_window import TrackerWindow
            self.tracker_window = TrackerWindow(self.on_close_tracker_window)
            self.tracker_window.setFixedSize(width_windown_live_speed, 60)
            self.tracker_window.setWindowTitle("DUNE Tracker")
            self.tracker_window.show()

app = Application()
