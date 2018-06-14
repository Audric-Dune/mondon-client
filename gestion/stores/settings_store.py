# !/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime

from PyQt5.QtCore import pyqtSignal, QObject

from commun.utils.timestamp import timestamp_at_day_ago, timestamp_at_time, timestamp_after_day_ago, timestamp_to_hour_little
from commun.constants.param import DEBUT_PROD_MATIN, FIN_PROD_SOIR
from commun.lib.base_de_donnee import Database


class SettingsStore(QObject):
    SETTINGS_CHANGED_SIGNAL = pyqtSignal()
    FOCUS_CHANGED_SIGNAL = pyqtSignal()
    CREATE_EVENT_CONFIG_WINDOW = pyqtSignal(str)
    CREATE_PLAN_PROD_WINDOW = pyqtSignal()
    ON_DAY_CHANGED = pyqtSignal()

    def __init__(self):
        super(SettingsStore, self).__init__()
        self.day_ago = 0
        self.plan_prod = None
        self.read_plan_prod = None
        self.ech = 1
        self.focus = None
        self.cursor = None

    def update_plans_prods(self):
        self.cursor = None
        from gestion.stores.plan_prod_store import plan_prod_store
        plans_prods = plan_prod_store.plans_prods
        plans_prods_update = []
        last_plan_prod = None
        for plan_prod in plans_prods:
            self.set_plan_prod(plan_prod, plans_prods_update)
            if last_plan_prod is None:
                continue
            else:
                if self.is_meltable_plans_prods(plan_prod_1=last_plan_prod, plan_prod_2=plan_prod):
                    self.merge_plan_prod(plan_prod_1=last_plan_prod, plan_prod_2=plan_prod)
                    del plans_prods_update[-2:-1]
                    plans_prods_update.append(last_plan_prod)
            last_plan_prod = plan_prod
        self.merge_plans_prods(plans_prods_update)
        self.SETTINGS_CHANGED_SIGNAL.emit()

    def merge_plans_prods(self, plans_prods_update):
        last_plan_prod = None
        for plan_prod in plans_prods_update:
            if last_plan_prod is None:
                last_plan_prod = plan_prod
            else:
                if self.is_meltable_plans_prods(plan_prod_1=last_plan_prod, plan_prod_2=plan_prod):
                    self.merge_plan_prod(plan_prod_1=last_plan_prod, plan_prod_2=plan_prod)
                else:
                    last_plan_prod = plan_prod

    def merge_plan_prod(self, plan_prod_1, plan_prod_2):
        plan_prod_1.end = plan_prod_2.end
        plan_prod_1.tours += plan_prod_2.tours
        self.update_plan_prod_on_database(plan_prod_1)
        self.delete_plan_prod(plan_prod_2, update=False)

    def is_meltable_plans_prods(self, plan_prod_1, plan_prod_2):
        code_bob_1 = self.get_code_bobine_selected(plan_prod_1.bobines_filles_selected)
        code_bob_2 = self.get_code_bobine_selected(plan_prod_2.bobines_filles_selected)
        if code_bob_1 == code_bob_2 and plan_prod_1.end == plan_prod_2.start:
            return True
        return False

    def set_plan_prod(self, plan_prod, plans_prods_update):
        plan_prod.start = self.get_start(plans_prods=plans_prods_update)
        plan_prod.get_end()
        start_split = self.is_there_an_event_or_end_day_in_plan_prod(plan_prod)
        if start_split:
            self.split_plan_prod(plan_prod, start_split=start_split, plans_prods_update=plans_prods_update)
        else:
            self.cursor = plan_prod.end
            self.update_plan_prod_on_database(plan_prod)
            plans_prods_update.append(plan_prod)

    def split_plan_prod(self, plan_prod, start_split, plans_prods_update):
        total_tours = plan_prod.tours
        plan_prod.tours = plan_prod.get_max_tour(end=start_split)
        self.set_plan_prod(plan_prod, plans_prods_update)
        from commun.model.plan_prod import PlanProd
        new_plan_prod = PlanProd(start=None)
        new_plan_prod.get_plan_prod_param(plan_prod)
        new_plan_prod.tours = total_tours-plan_prod.tours
        self.create_new_plan_prod(new_plan_prod)
        p_id = Database.get_last_id_plan_prod()
        new_plan_prod.p_id = p_id
        self.set_plan_prod(new_plan_prod, plans_prods_update)

    @staticmethod
    def is_there_an_event_or_end_day_in_plan_prod(plan_prod):
        from gestion.stores.event_store import event_store
        for event in event_store.events:
            if plan_prod.end > event.start > plan_prod.start:
                return event.start
        if plan_prod.end > timestamp_at_time(plan_prod.start, hours=FIN_PROD_SOIR):
            return timestamp_at_time(plan_prod.start, hours=FIN_PROD_SOIR)
        return False

    def set(self, day_ago=None, plan_prod=None, read_plan_prod=None):
        if day_ago is not None:
            self.day_ago = day_ago
        if plan_prod:
            self.plan_prod = plan_prod
            from gestion.stores.filter_store import filter_store
            filter_store.set_plan_prod(plan_prod)
        if read_plan_prod:
            self.read_plan_prod = read_plan_prod
        self.SETTINGS_CHANGED_SIGNAL.emit()

    def create_new_plan(self):
        from commun.model.plan_prod import PlanProd
        start_prod = self.get_start()
        if start_prod:
            plan_prod = PlanProd(start=start_prod)
            self.set(plan_prod=plan_prod)
            self.CREATE_PLAN_PROD_WINDOW.emit()

    def read_plan_prod(self, plan_prod):
        from commun.model.plan_prod import PlanProd
        from gestion.stores.plan_prod_store import plan_prod_store
        new_plan_prod = PlanProd(start=plan_prod[1], p_id=plan_prod[0])
        new_plan_prod.bobine_papier_selected = self.get_bobine_papier(code=plan_prod[4])
        new_plan_prod.refente_selected = self.get_refente(code=plan_prod[5])
        new_plan_prod.tours = plan_prod[2]
        new_plan_prod.longueur = plan_prod[3]
        new_plan_prod.get_end()
        plan_prod_store.add_bobine_to_plan_prod(plan_prod=new_plan_prod, code_bobines_filles=plan_prod[6])
        new_plan_prod.update_all_current_store()
        new_plan_prod.get_new_item_selected_from_store()
        self.set(read_plan_prod=new_plan_prod)
        self.CREATE_PLAN_PROD_WINDOW.emit()

    def get_start(self, start=None, plans_prods=None):
        if start is None:
            today = timestamp_at_day_ago(0)
            start = timestamp_at_time(ts=today, hours=DEBUT_PROD_MATIN) if self.cursor is None else self.cursor
        new_start = self.get_new_start(start=start, plans_prods=plans_prods)
        if new_start:
            return self.get_start(start=new_start, plans_prods=plans_prods)
        else:
            max_end = self.get_max_end(start)
            if max_end - start < 900:
                if max_end == timestamp_at_time(ts=max_end, hours=FIN_PROD_SOIR):
                    new_start = timestamp_after_day_ago(start=start, day_ago=1, hour=DEBUT_PROD_MATIN)
                    return self.get_start(start=new_start, plans_prods=plans_prods)
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

    def create_new_plan_prod(self, plan_prod):
        code_bobines_selected = self.get_code_bobine_selected(plan_prod.bobines_filles_selected)
        Database.create_plan_prod(bobine_papier=plan_prod.bobine_papier_selected.code,
                                  code_bobines_selected=code_bobines_selected,
                                  refente=plan_prod.refente_selected.code,
                                  start=plan_prod.start,
                                  longueur=plan_prod.longueur,
                                  tours=plan_prod.tours)

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
        self.SETTINGS_CHANGED_SIGNAL.emit()

    def delete_item(self):
        from commun.model.event import Event
        from commun.model.plan_prod import PlanProd
        print(self.focus)
        if isinstance(self.focus, Event):
            self.delete_event(event=self.focus)
        if isinstance(self.focus, PlanProd):
            self.delete_plan_prod(plan_prod=self.focus)

    def delete_event(self, event):
        Database.delete_event_prod(p_id=event.p_id)
        from gestion.stores.event_store import event_store
        event_store.update()
        self.update_plans_prods()
        self.SETTINGS_CHANGED_SIGNAL.emit()

    def delete_plan_prod(self, plan_prod, update=True):
        Database.delete_plan_prod(p_id=plan_prod.p_id)
        from gestion.stores.plan_prod_store import plan_prod_store
        plan_prod_store.get_plan_prod_from_database()
        if update:
            self.update_plans_prods()
        self.SETTINGS_CHANGED_SIGNAL.emit()

    def set_item_focus(self, item):
        if self.day_ago <= 0:
            self.focus = item
            self.FOCUS_CHANGED_SIGNAL.emit()

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
        self.ON_DAY_CHANGED.emit()

    def cancel_plan_prod(self):
        self.plan_prod = None
        self.SETTINGS_CHANGED_SIGNAL.emit()

settings_store_gestion = SettingsStore()
