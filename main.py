# !/usr/bin/env python
# -*- coding: utf-8 -*-

from object.logger import logger
logger.log_app_start()

import sys
import sqlite3
import _thread
import locale
import time

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication

from object.base_de_donnee import *
from object.window import *
from object.chart import *
from object.chart_menu import *

from fonction.gestion_timestamp import *

from param.param import *

logger.log("INITIALISATION", "Création de la QApplication avec les paramètres: {}".format(sys.argv))
app = QApplication(sys.argv)

logger.log("INITIALISATION", "Définition de l'icone de l'application")
app.setWindowIcon(QIcon("img/logo_dune_production.ico"))

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
