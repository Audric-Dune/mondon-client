# !/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtCore import pyqtSignal, QObject

from commun.utils.timestamp import timestamp_at_week_ago, timestamp_to_week


class SettingsTeamGestionStore(QObject):
    SETTINGS_TEAM_GESTION_CHANGED_SIGNAL = pyqtSignal()

    def __init__(self):
        super(SettingsTeamGestionStore, self).__init__()
        self.week_ago = 0
        self.time_stat = timestamp_to_week(timestamp_at_week_ago(self.week_ago)).capitalize()

    def update_week_ago(self, delta):
        self.set_new_settings(self.week_ago + delta)

    def update_param(self):
        self.time_stat = timestamp_to_week(timestamp_at_week_ago(self.week_ago)).capitalize()

    def set_new_settings(self, week_ago):
        self.week_ago = week_ago
        print(week_ago)
        self.update_param()
        self.SETTINGS_TEAM_GESTION_CHANGED_SIGNAL.emit()


settings_team_gestion_store = SettingsTeamGestionStore()
