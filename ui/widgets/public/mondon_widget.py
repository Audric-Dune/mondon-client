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
from stores.user_store import user_store
from ui.application import app


class MondonWidget(QWidget):
    def __init__(self, parent=None):
        super(QWidget, self).__init__(parent=parent)
        self.background_color = None
        self.border_color = None
        self.border_size = None
        self.border_manager = None
        self.padding = 0
        data_store_manager.DATA_CHANGED_SIGNAL.connect(self._handle_data_changed)
        settings_store.SETTINGS_CHANGED_SIGNAL.connect(self._handle_settings_changed)
        settings_stat_store.SETTINGS_STAT_CHANGED_SIGNAL.connect(self._handle_settings_stat_changed)
        settings_stat_store.SETTINGS_CHART_CHANGED_SIGNAL.connect(self._handle_settings_chart_changed)
        stat_store.ON_DATA_STAT_CHANGED_SIGNAL.connect(self._handle_data_stat_changed)
        user_store.ON_USER_CHANGED_SIGNAL.connect(self._handle_user_changed)
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

    def on_settings_chart_changed(self):
        pass

    def on_user_changed(self):
        pass

    def set_background_color(self, color):
        self.background_color = color

    def set_border(self, color, size=1, left=True, top=True, right=True, bottom=True):
        self.border_color = color
        self.border_size = size
        self.border_manager = {"left": left, "top": top, "right": right, "bottom": bottom}

    def set_padding(self, padding):
        self.padding = padding

    def _handle_user_changed(self):
        try:
            self.on_user_changed()
        except Exception as e:
            logger.log(type(self), "Erreur pendant l'exécution de `on_user_changed`: {}".format(e))

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

    def _handle_settings_chart_changed(self):
        try:
            self.on_settings_chart_changed()
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

    def _draw_border(self, p):
        """
        Dessine une bordure de la taille du bloc
        :param p: parametre de dessin
        """
        if self.border_color:
            from constants.colors import color_blanc
            draw_rectangle(p,
                           0 + self.padding,
                           0 + self.padding,
                           self.width() - self.padding * 2,
                           self.height() - self.padding * 2,
                           self.border_color)
            background_color = self.background_color if self.background_color else color_blanc
            border_left = self.border_size if self.border_manager["left"] else 0
            border_top = self.border_size if self.border_manager["top"] else 0
            border_right = self.border_size if self.border_manager["right"] else 0
            border_bottom = self.border_size if self.border_manager["bottom"] else 0
            draw_rectangle(p,
                           0 + self.padding + border_left,
                           0 + self.padding + border_top,
                           self.width() - self.padding - border_right * 2,
                           self.height() - self.padding - border_bottom * 2,
                           background_color)
        pass

    def paintEvent(self, event):
        p = QPainter()
        p.begin(self)
        self.draw(p)
        p.end()

    def draw(self, p):
        self._draw_fond(p)
        self._draw_border(p)
