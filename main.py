# !/usr/bin/env python
# -*- coding: utf-8 -*-
import time
t1 = time.time()

from lib.logger import logger
logger.log_app_start()

import sys
import sqlite3  # Import obligatoire pour la création du .exe
from PyQt5.QtGui import QIcon

from ui.application import app
from stores.data_store_manager import data_store_manager
data_store_manager.refresh_data()
from ui.utils.update_data_metrage import update_data_metrage
update_data_metrage()

logger.log("INITIALISATION", "Définition de l'icone de l'application")
app.setWindowIcon(QIcon("assets/icons/logo_dune_production.ico"))
app.create_main_window()

sys.exit(app.exec_())
