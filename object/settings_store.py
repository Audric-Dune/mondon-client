# !/usr/bin/env python
# -*- coding: utf-8 -*-


class SettingsStore:
    def __init__(self):
        self.listeners = []
        self.live = True
        self.day_ago = 0
        self.zoom = 1

    def add_listener(self, fonction):
        self.listeners.append(fonction)

    def set(self, live=None, day_ago=None, zoom=None):
        prev_live, prev_day_ago, prev_zoom = self.live, self.day_ago, self.zoom
        if live is not None:
            self.live = live
        if day_ago is not None:
            self.day_ago = day_ago
        if zoom is not None:
            self.zoom = zoom
        for fonction in self.listeners:
            fonction(prev_live, prev_day_ago, prev_zoom)

    def set_live(self, live):
        self.set(live=live)

    def set_day_ago(self, day_ago):
        self.set(day_ago=day_ago, zoom=1)

    def set_zoom(self, zoom):
        self.set(zoom=zoom)

settings_store = SettingsStore()
