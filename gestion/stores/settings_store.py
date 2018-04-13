# !/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime

from PyQt5.QtCore import pyqtSignal, QObject

from commun.utils.timestamp import timestamp_at_day_ago
from commun.lib.base_de_donnee import Database


class SettingsStore(QObject):
    SETTINGS_CHANGED_SIGNAL = pyqtSignal()

    def __init__(self):
        super(SettingsStore, self).__init__()
        self.day_ago = 0
        self.plan_prod = None

    def set(self, day_ago=None, plan_prod=None):
        if day_ago:
            self.day_ago = day_ago
        if plan_prod:
            self.plan_prod = plan_prod
        self.SETTINGS_CHANGED_SIGNAL.emit()

    def create_new_plan(self):
        from commun.model.plan_prod import PlanProd
        plan_prod = PlanProd(start=0)
        self.set(plan_prod=plan_prod)

    def save_plan_prod(self):
        print(self.plan_prod.bobine_papier_selected.code)
        print(self.plan_prod.refente_selected.code)
        code_bobines_selected = ""
        for bobine in self.plan_prod.bobines_filles_selected:
            code_bobines_selected += str(bobine.code)
            code_bobines_selected += "_"
            code_bobines_selected += str(bobine.pose)
            code_bobines_selected += "_"
        print(code_bobines_selected)
        Database.create_plan_prod(bobine_papier=self.plan_prod.bobine_papier_selected.code,
                                  code_bobines_selected=code_bobines_selected,
                                  refente=self.plan_prod.refente_selected.code,
                                  start=self.plan_prod.start)

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
