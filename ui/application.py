# !/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QApplication

from constants.dimensions import window_height, window_width
from lib.logger import logger
from stores.data_store_manager import data_store_manager
from ui.utils.window import focus_window


class Application(QApplication):
    RESIZED_SIGNAL = pyqtSignal()

    def __init__(self, argv=None):
        if argv is None:
            argv = []
        super(Application, self).__init__(argv)
        self.main_window = None
        self.tracker_window = None
        self.dic_arret_window = {}
        data_store_manager.NEW_ARRET_SIGNAL.connect(self.create_arret_window)

    def on_resize_main_window(self):
        self.RESIZED_SIGNAL.emit()

    def on_close_main_window(self):
        self.main_window = None
        self.close_data_store_manager()

    def on_close_tracker_window(self):
        self.tracker_window = None
        self.close_data_store_manager()

    def on_close_arret_window(self, start_arret):
        if self.dic_arret_window:
            del self.dic_arret_window[start_arret]
        self.close_data_store_manager()

    def close_data_store_manager(self):
        # Fonction qui se charge de stopper le refresh data lorsque
        # la derniere fenetre de l'application est fermée
        if not self.main_window and not self.tracker_window and not self.dic_arret_window:
            data_store_manager.cancel_refresh()

    def create_main_window(self):
        if self.main_window:
            focus_window(self.main_window)
        else:
            from ui.windows.main_window import MainWindow
            logger.log("INITIALISATION", "Création de la Window")
            self.main_window = MainWindow(self.on_close_main_window, self.on_resize_main_window)

            logger.log("INITIALISATION", "Configuration de la Window")
            self.main_window.initialisation()
            self.main_window.setWindowTitle("DUNE Production bobine")
            self.main_window.resize(window_width, window_height)
            self.main_window.setMinimumSize(window_width, window_height)

            logger.log("INITIALISATION", "Affichage de MainWindow")
            self.main_window.show()

    def create_tracker_window(self):
        if self.tracker_window:
            focus_window(self.tracker_window)
        else:
            from ui.windows.tracker_window import TrackerWindow
            self.tracker_window = TrackerWindow(self.on_close_tracker_window)
            self.tracker_window.setWindowTitle("DUNE Tracker")
            self.tracker_window.setFixedSize(self.tracker_window.sizeHint())
            self.tracker_window.show()

    def create_arret_window(self, start_arret, day_ago):
        if self.dic_arret_window.get(start_arret):
            focus_window(self.dic_arret_window[start_arret])
        else:
            object_arret = data_store_manager.get_store_at_day_ago(day_ago).dic_arret[start_arret]
            from ui.windows.arret_window import ArretWindow
            arret_window = ArretWindow(self.on_close_arret_window, object_arret)
            self.dic_arret_window[start_arret] = arret_window
            arret_window.setWindowTitle("Gestion d'un arrêt")
            x = self.main_window.pos().x() + (self.main_window.width() - arret_window.width()) / 2
            y = self.main_window.pos().y() + 50
            arret_window.move(x, y)
            arret_window.show()


app = Application()
