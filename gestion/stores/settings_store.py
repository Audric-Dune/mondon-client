# !/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime

from PyQt5.QtCore import pyqtSignal, QObject

from commun.utils.timestamp import timestamp_at_day_ago, timestamp_at_time, timestamp_to_hour_little
from commun.constants.param import DEBUT_PROD_MATIN, FIN_PROD_SOIR
from commun.lib.base_de_donnee import Database


class SettingsStore(QObject):
    SETTINGS_CHANGED_SIGNAL = pyqtSignal()
    CREATE_EVENT_CONFIG_WINDOW = pyqtSignal(str)
    CREATE_PLAN_PROD_WINDOW = pyqtSignal()

    def __init__(self):
        super(SettingsStore, self).__init__()
        self.day_ago = 0
        self.plan_prod = None
        self.ech = 1

    def update_plans_prods(self):
        from gestion.stores.plan_prod_store import plan_prod_store
        plans_prods = self.sort_plan_prod(plan_prod_store.plans_prods)
        plans_prods_update = []
        for plan_prod in plans_prods:
            plan_prod.start = self.get_start(plans_prods=plans_prods_update)
            plan_prod.get_end()
            self.update_plan_prod_on_database(plan_prod)
            plans_prods_update.append(plan_prod)

    @staticmethod
    def sort_plan_prod(plan_prods):
        plan_prods = sorted(plan_prods, key=lambda b: b.get_start(), reverse=False)
        return plan_prods

    def set(self, day_ago=None, plan_prod=None):
        if day_ago is not None:
            self.day_ago = day_ago
        if plan_prod:
            self.plan_prod = plan_prod
            from gestion.stores.filter_store import filter_store
            filter_store.set_plan_prod(plan_prod)
        self.SETTINGS_CHANGED_SIGNAL.emit()

    def create_new_plan(self):
        from commun.model.plan_prod import PlanProd
        start_prod = self.get_start()
        if start_prod:
            plan_prod = PlanProd(start=start_prod)
            self.set(plan_prod=plan_prod)
            self.CREATE_PLAN_PROD_WINDOW.emit()

    def get_start(self, start=None, plans_prods=None):
        if start is None:
            start_day = timestamp_at_day_ago(self.day_ago)
            start = timestamp_at_time(ts=start_day, hours=DEBUT_PROD_MATIN)
        new_start = self.get_new_start(start=start, plans_prods=plans_prods)
        if new_start:
            print("new_start = ", timestamp_to_hour_little(new_start))
            return self.get_start(start=new_start, plans_prods=plans_prods)
        else:
            max_end = self.get_max_end(start)
            print("max_end = ", timestamp_to_hour_little(max_end))
            if max_end - start < 900:
                if max_end == timestamp_at_time(ts=max_end, hours=FIN_PROD_SOIR):
                    return False
                return self.get_start(start=max_end, plans_prods=plans_prods)
            return start

    def get_new_start(self, start, plans_prods):
        from gestion.stores.event_store import event_store
        if plans_prods is None:
            from gestion.stores.plan_prod_store import plan_prod_store
            plans_prods = plan_prod_store.plans_prods
        for prod in plans_prods:
            if prod.start == start:
                return prod.end
        for event in event_store.events:
            if event.start == start:
                return self.get_end_at_start(start, end=event.end)
        return False

    @staticmethod
    def get_end_at_start(start, end):
        from gestion.stores.event_store import event_store
        end = end
        for event in event_store.events:
            if end >= event.start >= start:
                if event.end > end:
                    end = event.end
        return end

    @staticmethod
    def get_max_end(start):
        from gestion.stores.event_store import event_store
        next_start_event = timestamp_at_time(ts=start, hours=FIN_PROD_SOIR)
        end_day = timestamp_at_time(ts=start, hours=FIN_PROD_SOIR)
        for event in event_store.events:
            if event.start > end_day or event.start < start:
                continue
            elif next_start_event is None:
                next_start_event = event.start
            elif next_start_event > event.start:
                next_start_event = event.start
        return next_start_event

    def create_new_event(self, type_event):
        self.CREATE_EVENT_CONFIG_WINDOW.emit(type_event)

    @staticmethod
    def get_code_bobine_selected(bobines_filles_selected):
        code_bobines_selected = ""
        for bobine in bobines_filles_selected:
            code_bobines_selected += str(bobine.code)
            code_bobines_selected += "_"
            code_bobines_selected += str(bobine.pose)
            code_bobines_selected += "_"
        return code_bobines_selected

    def save_plan_prod(self):
        code_bobines_selected = self.get_code_bobine_selected(self.plan_prod.bobines_filles_selected)
        Database.create_plan_prod(bobine_papier=self.plan_prod.bobine_papier_selected.code,
                                  code_bobines_selected=code_bobines_selected,
                                  refente=self.plan_prod.refente_selected.code,
                                  start=self.plan_prod.start,
                                  longueur=self.plan_prod.longueur,
                                  tours=self.plan_prod.tours)
        self.plan_prod = None
        self.SETTINGS_CHANGED_SIGNAL.emit()

    def update_plan_prod_on_database(self, plan_prod):
        code_bobines_selected = self.get_code_bobine_selected(plan_prod.bobines_filles_selected)
        Database.update_plan_prod(p_id=plan_prod.p_id,
                                  bobine_papier=plan_prod.bobine_papier_selected.code,
                                  code_bobines_selected=code_bobines_selected,
                                  refente=plan_prod.refente_selected.code,
                                  start=plan_prod.start,
                                  longueur=plan_prod.longueur,
                                  tours=plan_prod.tours)

    def save_event(self, event):
        Database.create_event_prod(start=event.start, end=event.end, p_type=event.type_event, info=event.info,
                                   ensemble=event.ensemble)
        from gestion.stores.event_store import event_store
        event_store.update()
        self.update_plans_prods()
        settings_store_gestion.SETTINGS_CHANGED_SIGNAL.emit()

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

    def cancel_plan_prod(self):
        self.plan_prod = None
        self.SETTINGS_CHANGED_SIGNAL.emit()

settings_store_gestion = SettingsStore()
