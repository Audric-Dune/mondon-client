# !/usr/bin/env python
# -*- coding: utf-8 -*-

from lib.logger import logger
logger.log_app_start()

import sys
import sqlite3  # Import obligatoire pour la création du .exe
from PyQt5.QtGui import QIcon

from ui.application import Application

logger.log("INITIALISATION", "Création de la QApplication avec les paramètres: {}".format(sys.argv))
app = Application(sys.argv)

logger.log("INITIALISATION", "Définition de l'icone de l'application")
app.setWindowIcon(QIcon("assets/icons/logo_dune_production.ico"))

sys.exit(app.exec_())
