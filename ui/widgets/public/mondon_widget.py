# !/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QWidget

from lib.logger import logger
from stores.settings_store import settings_store
from stores.data_store_manager import data_store_manager


class MondonWidget(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent=parent)
        data_store_manager.DATA_CHANGED_SIGNAL.connect(self._handle_data_changed)
        settings_store.SETTINGS_CHANGED_SIGNAL.connect(self._handle_settings_changed)

    def on_data_changed(self):
        pass

    def on_settings_changed(self, prev_live, prev_day_ago, prev_zoom):
        pass

    def _handle_data_changed(self):
        try:
            self.on_data_changed()
        except Exception as e:
            logger.log(type(self), "Erreur pendant l'exécution de `on_data_changed`: {}".format(e))

    def _handle_settings_changed(self, prev_live, prev_day_ago, prev_zoom):
        try:
            self.on_settings_changed(prev_live, prev_day_ago, prev_zoom)
        except Exception as e:
            logger.log(type(self), "Erreur pendant l'exécution de `on_settings_changed`: {}".format(e))