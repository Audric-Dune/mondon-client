# !/usr/bin/env python
# -*- coding: utf-8 -*-
import time
t1 = time.time()

from lib.logger import logger
logger.log_app_start()

import sys
import sqlite3  # Import obligatoire pour la création du .exe
import statistics  # Import obligatoire pour la création du .exe
from PyQt5.QtGui import QIcon

mode = 'ui'
if len(sys.argv) > 1:
    mode = sys.argv[1]

from ui.application import app
from stores.data_store_manager import data_store_manager
data_store_manager.refresh_data()
from ui.utils.update_data_metrage import update_data_metrage
update_data_metrage()

if mode == 'ui':
    logger.log("INITIALISATION", "Définition de l'icone de l'application")
    app.setWindowIcon(QIcon("assets/icons/logo_dune_production.ico"))
    from ui.application import app
    app.create_popup_user()

if mode in ('-r', '--rapport', 'rapport'):
    from ui.widgets.rapport.menu_rapport import RapportMenu
    rapport_menu = RapportMenu()
    rapport_menu._get_pdf()

if mode == 'ui':
    sys.exit(app.exec_())
