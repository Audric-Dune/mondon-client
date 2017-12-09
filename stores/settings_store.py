# !/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtCore import pyqtSignal, QObject


class SettingsStore(QObject):
    SETTINGS_CHANGED_SIGNAL = pyqtSignal(
        bool,  # live
        'unsigned long long',  # day_ago
        'unsigned long long',  # zoom
    )

    def __init__(self):
        super(SettingsStore, self).__init__()
        self.live = True
        self.day_ago = 0
        self.zoom = 1

    def set(self, live=None, day_ago=None, zoom=None):
        prev_live, prev_day_ago, prev_zoom = self.live, self.day_ago, self.zoom
        if live is not None:
            self.live = live
        if day_ago is not None:
            self.day_ago = day_ago
        if zoom is not None:
            self.zoom = zoom
        self.SETTINGS_CHANGED_SIGNAL.emit(prev_live, prev_day_ago, round(prev_zoom))

    def set_live(self, live):
        self.set(live=live)

    def set_day_ago(self, day_ago):
        self.set(day_ago=day_ago, zoom=1)

    def set_zoom(self, zoom):
        self.set(zoom=zoom)


settings_store = SettingsStore()
