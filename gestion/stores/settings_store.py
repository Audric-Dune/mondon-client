# !/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime

from PyQt5.QtCore import pyqtSignal, QObject

from commun.utils.timestamp import timestamp_at_day_ago, timestamp_at_time
from commun.constants.param import DEBUT_PROD_MATIN
from commun.lib.base_de_donnee import Database


class SettingsStore(QObject):
    SETTINGS_CHANGED_SIGNAL = pyqtSignal()

    def __init__(self):
        super(SettingsStore, self).__init__()
        self.day_ago = 0
        self.plan_prod = None

    def set(self, day_ago=None, plan_prod=None):
        if day_ago or day_ago == 0:
            self.day_ago = day_ago
        if plan_prod:
            self.plan_prod = plan_prod
        self.SETTINGS_CHANGED_SIGNAL.emit()

    def create_new_plan(self):
        from gestion.stores.plan_prod_store import plan_prod_store
        from commun.model.plan_prod import PlanProd
        if plan_prod_store.plans_prods:
            last_plan_prod = plan_prod_store.plans_prods[-1]
            plan_prod = PlanProd(start=last_plan_prod.end, index=len(plan_prod_store.plans_prods) + 1)
        else:
            start_day = timestamp_at_day_ago(self.day_ago)
            plan_prod = PlanProd(start=timestamp_at_time(ts=start_day, hours=DEBUT_PROD_MATIN))
        self.set(plan_prod=plan_prod)

    def save_plan_prod(self):
        code_bobines_selected = ""
        for bobine in self.plan_prod.bobines_filles_selected:
            code_bobines_selected += str(bobine.code)
            code_bobines_selected += "_"
            code_bobines_selected += str(bobine.pose)
            code_bobines_selected += "_"
        Database.create_plan_prod(bobine_papier=self.plan_prod.bobine_papier_selected.code,
                                  code_bobines_selected=code_bobines_selected,
                                  refente=self.plan_prod.refente_selected.code,
                                  start=self.plan_prod.start,
                                  longueur=self.plan_prod.longueur,
                                  tours=self.plan_prod.tours)
        self.plan_prod = None
        self.SETTINGS_CHANGED_SIGNAL.emit()

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
