# !/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime

from PyQt5.QtCore import pyqtSignal, QObject

from commun.utils.timestamp import timestamp_at_day_ago


class SettingsStore(QObject):
    SETTINGS_CHANGED_SIGNAL = pyqtSignal()

    def __init__(self):
        super(SettingsStore, self).__init__()
        self.day_ago = 0
        self.plan_prod_id = None

    def set(self, day_ago=None, plan_prod_id=None):
        if day_ago:
            self.day_ago = day_ago
        if plan_prod_id:
            self.plan_prod_id = plan_prod_id
        self.SETTINGS_CHANGED_SIGNAL.emit()

    def create_new_plan(self):
        self.set(plan_prod_id=1)

    def set_day_ago(self, day_ago):
        # Test si nouveau jour est un samedi ou dimanche
        new_day = timestamp_at_day_ago(day_ago)
        week_day = datetime.fromtimestamp(new_day).weekday()
        if 5 <= week_day <= 6:
            if self.day_ago < day_ago:
                self.set_day_ago(day_ago+1)
            else:
                self.set_day_ago(day_ago-1)
        else:
            self.set(day_ago=day_ago)


settings_store_gestion = SettingsStore()
