# !/usr/bin/env python
# -*- coding: utf-8 -*-
from lib.logger import logger

from PyQt5.QtWidgets import QApplication

from constants.dimensions import window_height, window_width
from stores.data_store_manager import data_store_manager
from stores.windows_store import windows_store
from ui.widgets.tracker_window import TrackerWindow
from ui.widgets.main_window import MainWindow


class Application(QApplication):

    def __init__(self, argv=None):
        super(Application, self).__init__(argv)
        self.windows = []
        self.__create_main_window()
        windows_store.NEW_WINDOWS_CHANGED_SIGNAL.connect(self._handle_new_windows_changed)

    def on_new_windows_changed(self):
        self.create_window_live_speed()

    def _handle_new_windows_changed(self):
        try:
            self.on_new_windows_changed()
        except Exception as e:
            logger.log(type(self), "Erreur pendant l'exécution de `on_windows_changed`: {}".format(e))

    def on_close_window(self):
        # Fonction qui se charge de stopper le refresh data lorsque la derniere fenetre de l'application est fermée
        if not self.windows:
            data_store_manager.cancel_refresh()

    def __create_main_window(self):
        logger.log("INITIALISATION", "Création de la Window")
        main_window = MainWindow(self)

        logger.log("INITIALISATION", "Configuration de la Window")
        main_window.initialisation()
        main_window.setWindowTitle("DUNE Production bobine")
        main_window.resize(window_width, window_height)
        main_window.setMinimumSize(window_width, window_height)

        logger.log("INITIALISATION", "Affichage de MainWindow")
        main_window.show()
        self.windows.append(main_window)

    def create_window_live_speed(self):
        tracker_window = TrackerWindow(self)

        tracker_window.initialisation()
        tracker_window.setFixedSize(160, 60)

        tracker_window.setWindowTitle("Tracker")

        tracker_window.show()
        self.windows.append(tracker_window)
