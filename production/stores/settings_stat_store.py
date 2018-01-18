# !/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtCore import pyqtSignal, QObject

from commun.utils.timestamp import (
    timestamp_at_week_ago,
    timestamp_to_week, timestamp_to_month,
    timestamp_at_month_ago, )


class SettingsStatStore(QObject):
    SETTINGS_STAT_CHANGED_SIGNAL = pyqtSignal()
    SETTINGS_CHART_CHANGED_SIGNAL = pyqtSignal()

    def __init__(self):
        super(SettingsStatStore, self).__init__()
        self.data_type = "métrage"
        self.time_stat = ""
        self.format = ""
        self.display_setting = []
        self.week_ago = 0
        self.month_ago = -1
        self.year_ago = -1
        self.update_display_setting()
        self.update_param()

    @staticmethod
    def update_data():
        from production.stores.stat_store import stat_store
        stat_store.update_data()

    def update_display_setting(self):
        if self.week_ago >= 0:
            self.display_setting = [True, True, True]
        if self.month_ago >= 0:
            self.display_setting = [False, False, True]

    def get_format(self):
        if self.week_ago >= 0:
            self.format = "week"
        if self.month_ago >= 0:
            self.format = "month"
        if self.year_ago >= 0:
            self.format = "years"

    def update_time_ago(self, delta):
        if self.week_ago >= 0:
            self.week_ago += delta
        if self.month_ago >= 0:
            self.month_ago += delta
        if self.year_ago >= 0:
            self.year_ago += delta
        self.update_param()
        self.SETTINGS_STAT_CHANGED_SIGNAL.emit()

    def update_param(self):
        if self.week_ago >= 0:
            self.time_stat = timestamp_to_week(timestamp_at_week_ago(self.week_ago)).capitalize()
        if self.month_ago >= 0:
            self.time_stat = timestamp_to_month(timestamp_at_month_ago(self.month_ago)).capitalize()
        self.get_format()

    def on_select_checkbox_display(self, index_checkbox):
        self.display_setting[index_checkbox] = False if self.display_setting[index_checkbox] else True
        self.SETTINGS_CHART_CHANGED_SIGNAL.emit()

    def set_new_settings(self, type, week_ago=-1, month_ago=-1, year_ago=-1):
        self.data_type = type
        self.week_ago = week_ago
        self.month_ago = month_ago
        self.year_ago = year_ago
        self.get_format()
        self.update_param()
        self.update_display_setting()
        self.SETTINGS_STAT_CHANGED_SIGNAL.emit()


settings_stat_store = SettingsStatStore()
