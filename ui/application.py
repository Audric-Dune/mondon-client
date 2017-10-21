# !/usr/bin/env python
# -*- coding: utf-8 -*-
from lib.logger import logger

from PyQt5.QtWidgets import QApplication

from constants.dimensions import window_height, window_width
from ui.widgets.main_window import MainWindow


class Application(QApplication):

    def __init__(self, argv=None):
        super(Application, self).__init__(argv)
        self.windows = []
        self.__create_main_window()

    def __create_main_window(self):
        logger.log("INITIALISATION", "Création de la Window")
        main_window = MainWindow()

        logger.log("INITIALISATION", "Configuration de la Window")
        main_window.initialisation()
        main_window.setWindowTitle("DUNE Production bobine")
        main_window.resize(window_width, window_height)
        main_window.setMinimumSize(window_width, window_height)

        logger.log("INITIALISATION", "Affichage de MainWindow")
        main_window.show()
        self.windows.append(main_window)

    def create_window_live_speed(self):
        # Fonction que j'aimerais bien appeler lorsque je double clik sur la vitesse actuelle
        print("create_window_live_speed")
