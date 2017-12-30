# !/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QWidget

from ui.utils.drawing import draw_rectangle
from lib.logger import logger
from stores.settings_store import settings_store
from stores.data_store_manager import data_store_manager
from stores.stat_store import stat_store
from stores.settings_stat_store import settings_stat_store
from ui.application import app


class MondonWidget(QWidget):
    def __init__(self, parent=None):
        super(QWidget, self).__init__(parent=parent)
        self.background_color = None
        self.padding = 0
        data_store_manager.DATA_CHANGED_SIGNAL.connect(self._handle_data_changed)
        settings_store.SETTINGS_CHANGED_SIGNAL.connect(self._handle_settings_changed)
        settings_stat_store.SETTINGS_STAT_CHANGED_SIGNAL.connect(self._handle_settings_stat_changed)
        stat_store.ON_DATA_STAT_CHANGED_SIGNAL.connect(self._handle_data_stat_changed)
        app.RESIZED_SIGNAL.connect(self._handle_size_main_window_changed)

    def on_data_changed(self):
        pass

    def on_settings_changed(self, prev_live, prev_day_ago, prev_zoom):
        pass

    def on_settings_stat_changed(self):
        pass

    def on_data_stat_changed(self):
        pass

    def on_size_main_window_changed(self):
        pass

    def set_background_color(self, color):
        self.background_color = color

    def set_padding(self, padding):
        self.padding = padding

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

    def _handle_settings_stat_changed(self):
        try:
            self.on_settings_stat_changed()
        except Exception as e:
            logger.log(type(self), "Erreur pendant l'exécution de `on_settings_stat_changed`: {}".format(e))

    def _handle_data_stat_changed(self):
        try:
            self.on_data_stat_changed()
        except Exception as e:
            logger.log(type(self), "Erreur pendant l'exécution de `on_data_stat_changed`: {}".format(e))

    def _handle_size_main_window_changed(self):
        try:
            self.on_size_main_window_changed()
        except Exception as e:
            logger.log(type(self), "Erreur pendant l'exécution de `on_data_stat_changed`: {}".format(e))

    def _draw_fond(self, p):
        """
        Dessine un rectangle de la taille du bloc
        :param p: parametre de dessin
        """
        if self.background_color:
            draw_rectangle(p,
                           0 + self.padding,
                           0 + self.padding,
                           self.width() - self.padding * 2,
                           self.height() - self.padding * 2,
                           self.background_color)
        pass

    def paintEvent(self, event):
        p = QPainter()
        p.begin(self)
        self.draw(p)
        p.end()

    def draw(self, p):
        self._draw_fond(p)
