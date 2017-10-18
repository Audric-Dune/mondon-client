# !/usr/bin/env python
# -*- coding: utf-8 -*-

from lib.logger import logger
logger.log_app_start()

import sys
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication

from param import window_height, window_width
from ui.window import Window


logger.log("INITIALISATION", "Création de la QApplication avec les paramètres: {}".format(sys.argv))
app = QApplication(sys.argv)

logger.log("INITIALISATION", "Définition de l'icone de l'application")
app.setWindowIcon(QIcon("assets/icons/logo_dune_production.ico"))

logger.log("INITIALISATION", "Création de la Window")
window = Window()

logger.log("INITIALISATION", "Configuration de la Window")
window.initialisation()
window.setWindowTitle("DUNE Production bobine")
window.resize(window_width, window_height)
window.setMinimumSize(window_width, window_height)

logger.log("INITIALISATION", "Affichage de MainWindow")
window.show()

sys.exit(app.exec_())
