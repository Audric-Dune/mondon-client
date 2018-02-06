# !/usr/bin/env python
# -*- coding: utf-8 -*-

import statistics
import sqlite3

from commun.lib.logger import logger
logger.log_app_start()

import sys
from PyQt5.QtGui import QIcon

mode = 'ui'
if len(sys.argv) > 1:
    mode = sys.argv[1]

from production.ui.application import app
from production.stores.data_store_manager import data_store_manager
data_store_manager.refresh_data()
from commun.utils.update_data_metrage import update_data_metrage
update_data_metrage()

if mode == 'ui':
    logger.log("INITIALISATION", "Définition de l'icone de l'application")
    app.setWindowIcon(QIcon("commun/assets/icons/logo_dune_production.ico"))
    from production.ui.application import app
    app.create_popup_user()

if mode in ('-r', '--rapport', 'rapport'):
    from production.ui.widgets.rapport.menu_rapport import RapportMenu
    rapport_menu = RapportMenu()
    rapport_menu.externat_get_pdf()

if mode == 'ui':
    sys.exit(app.exec_())
