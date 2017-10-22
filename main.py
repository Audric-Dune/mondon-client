# !/usr/bin/env python
# -*- coding: utf-8 -*-

from lib.logger import logger
logger.log_app_start()

import sys
import sqlite3  # Import obligatoire pour la création du .exe
from PyQt5.QtGui import QIcon

from ui.application import app

logger.log("INITIALISATION", "Définition de l'icone de l'application")
app.setWindowIcon(QIcon("assets/icons/logo_dune_production.ico"))
app.create_main_window()

sys.exit(app.exec_())
