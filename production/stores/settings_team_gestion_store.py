# !/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtCore import pyqtSignal, QObject

from commun.utils.timestamp import timestamp_at_week_ago, timestamp_to_week
from commun.utils.day import is_weekend
from commun.lib.base_de_donnee import Database


class SettingsTeamGestionStore(QObject):
    SETTINGS_TEAM_GESTION_CHANGED_SIGNAL = pyqtSignal()

    def __init__(self):
        super(SettingsTeamGestionStore, self).__init__()
        self.week_ago = 0
        self.add_defaut_day()
        self.time_stat = timestamp_to_week(timestamp_at_week_ago(self.week_ago)).capitalize()

    def update_week_ago(self, delta):
        self.set_new_settings(self.week_ago + delta)

    def update_param(self):
        self.time_stat = timestamp_to_week(timestamp_at_week_ago(self.week_ago)).capitalize()

    def add_defaut_day(self):
        start_week = timestamp_at_week_ago(self.week_ago)
        start_next_week = timestamp_at_week_ago(self.week_ago - 1)
        ts_day_ago = start_week
        while ts_day_ago <= start_next_week:
            if is_weekend(ts_day_ago):
                break
            else:
                Database.add_defaut_day(ts_day_ago)
            ts_day_ago += 86400

    def set_new_settings(self, week_ago):
        self.week_ago = week_ago
        self.update_param()
        self.add_defaut_day()
        self.SETTINGS_TEAM_GESTION_CHANGED_SIGNAL.emit()


settings_team_gestion_store = SettingsTeamGestionStore()
