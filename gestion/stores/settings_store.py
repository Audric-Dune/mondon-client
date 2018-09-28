# !/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime

from PyQt5.QtCore import pyqtSignal, QObject

from commun.utils.timestamp import timestamp_at_day_ago, timestamp_at_time, get_day_ago, is_vendredi
from commun.constants.param import DEBUT_PROD_MATIN, FIN_PROD_SOIR, FIN_PROD_SOIR_VENDREDI
from commun.model.task import Task
from commun.lib.base_de_donnee import Database
from gestion.utils import get_code_bobine_selected


class SettingsStore(QObject):
    SETTINGS_CHANGED_SIGNAL = pyqtSignal()
    FOCUS_CHANGED_SIGNAL = pyqtSignal()
    CREATE_EVENT_CONFIG_WINDOW = pyqtSignal(str)
    from commun.model.event import Event
    CREATE_EVENT_CONFIG_EDIT_WINDOW = pyqtSignal(Event)
    CREATE_PLAN_PROD_WINDOW = pyqtSignal()
    ON_DAY_CHANGED = pyqtSignal()

    def __init__(self):
        super(SettingsStore, self).__init__()
        self.day_ago = 0
        self.plan_prod = None
        self.ech = 1
        self.focus = None
        self.standing_insert = None

    def create_new_plan(self):
        from commun.model.plan_prod import PlanProd
        new_start = self.get_start_for_new_plan_prod()
        from gestion.stores.plan_prod_store import plan_prod_store
        plan_prod = PlanProd(start=new_start,
                             last_plan_prod=plan_prod_store.get_last_plan_prod(start_plan_prod=new_start))
        self.set(plan_prod=plan_prod)
        self.SETTINGS_CHANGED_SIGNAL.emit()
        self.CREATE_PLAN_PROD_WINDOW.emit()

    def create_new_event(self, type_event):
        self.CREATE_EVENT_CONFIG_WINDOW.emit(type_event)

    def focus_insert(self):
        self.standing_insert = self.focus
        self.focus = None
        self.FOCUS_CHANGED_SIGNAL.emit()

    def focus_edit(self):
        from commun.model.event import Event
        from commun.model.plan_prod import PlanProd
        if isinstance(self.focus, Event):
            self.edit_event(event=self.focus)
        if isinstance(self.focus, PlanProd):
            self.edit_plan_prod(plan_prod=self.focus)

    def edit_plan_prod(self, plan_prod):
        self.set(plan_prod=plan_prod)
        self.CREATE_PLAN_PROD_WINDOW.emit()

    def edit_event(self, event):
        self.CREATE_EVENT_CONFIG_EDIT_WINDOW.emit(event)

    def get_start_for_new_plan_prod(self):
        tasks = self.get_tasks_at_day_ago(day_ago=self.day_ago)
        start = timestamp_at_time(timestamp_at_day_ago(self.day_ago), hours=DEBUT_PROD_MATIN)
        for task in tasks:
            if task.start == start:
                start = task.end
        return start

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

    def set_item_focus(self, item):
        from commun.model.plan_prod import PlanProd
        if self.standing_insert and isinstance(item, PlanProd) and self.day_ago <= 0:
            self.insert_plan_prod_1_before_plan_prod_2(plan_1=self.standing_insert, plan_2=item)
            self.standing_insert = None
            self.focus = None
            self.SETTINGS_CHANGED_SIGNAL.emit()
        if self.day_ago <= 0:
            self.focus = item
            self.FOCUS_CHANGED_SIGNAL.emit()

    def insert_plan_prod_1_before_plan_prod_2(self, plan_1, plan_2):
        def set_index_to_plan_prod(p_index, plan_prod, day_ago=None):
            for p_task in tasks:
                if p_task.plan_prod == plan_prod:
                    p_task.index = p_index
                    if day_ago is not None:
                        p_task.day_ago = day_ago
        tasks = self.get_tasks_at_day_ago(day_ago=self.day_ago)
        plan_1_in_tasks = False
        for task in tasks:
            if task.plan_prod == plan_1:
                plan_1_in_tasks = True
        if not plan_1_in_tasks:
            tasks.append(Task(plan_prod=plan_1, start=plan_1.start, end=plan_1.end, day_ago=self.day_ago))
        index = 0
        current_day_ago = self.day_ago
        for task in tasks:
            if current_day_ago != task.day_ago:
                current_day_ago = task.day_ago
                index = 0
            if task.plan_prod == plan_2:
                set_index_to_plan_prod(plan_prod=plan_1, p_index=index, day_ago=current_day_ago)
                index += 1
                set_index_to_plan_prod(plan_prod=plan_2, p_index=index)
                index += 1
            elif task.plan_prod != plan_1:
                task.index = index
                index += 1
        tasks = sorted(tasks, key=lambda t: t.get_index())
        self.update_plans_prods(tasks=tasks)

    def set(self, day_ago=None, plan_prod=None):
        if day_ago is not None:
            self.day_ago = day_ago
            self.update_stock_bobines()
            self.SETTINGS_CHANGED_SIGNAL.emit()
        if plan_prod:
            self.plan_prod = plan_prod
            self.update_stock_bobines_at_time()

    def update_stock_bobines(self):
        from commun.stores.bobine_fille_store import bobine_fille_store
        from commun.stores.bobine_papier_store import bobine_papier_store
        from commun.stores.bobine_poly_store import bobine_poly_store
        for bobine in bobine_fille_store.bobines:
            bobine.get_stock_at_time(day_ago=self.day_ago)
        for bobine_papier in bobine_papier_store.bobines:
            bobine_papier.get_stock_at_time(day_ago=self.day_ago)
        for bobine_poly in bobine_poly_store.bobines:
            bobine_poly.get_stock_at_time(day_ago=self.day_ago)

    def update_stock_bobines_at_time(self):
        from commun.stores.bobine_fille_store import bobine_fille_store
        from commun.stores.bobine_papier_store import bobine_papier_store
        from commun.stores.bobine_poly_store import bobine_poly_store
        for bobine in bobine_fille_store.bobines:
            bobine.get_stock_at_time(time=self.plan_prod.start)
        for bobine_papier in bobine_papier_store.bobines:
            bobine_papier.get_stock_at_time(time=self.plan_prod.start)
        for bobine_poly in bobine_poly_store.bobines:
            bobine_poly.get_stock_at_time(time=self.plan_prod.start)

    @staticmethod
    def get_tasks_at_day_ago(day_ago):
        tasks = []
        from gestion.stores.plan_prod_store import plan_prod_store
        for plan_prod in plan_prod_store.plans_prods:
            if plan_prod.start > timestamp_at_day_ago(day_ago):
                if plan_prod.start > timestamp_at_day_ago(day_ago-1):
                    day_ago -= 1
                tasks.append(Task(start=plan_prod.start, plan_prod=plan_prod, end=plan_prod.end, day_ago=day_ago))
        tasks = sorted(tasks, key=lambda t: t.get_start())
        index = 0
        day_ago = None
        for task in tasks:
            if day_ago is None:
                day_ago = task.day_ago
            if task.day_ago < day_ago:
                day_ago = task.day_ago
                index = 0
            task.index = index
            index += 1
        return tasks

    def update_plans_prods(self, tasks=None, day_ago=None):
        def get_end_from_index_task(index, p_day_ago):
            for p_task in tasks:
                if p_task.index == index and p_task.day_ago == p_day_ago:
                    return p_task.plan_prod.end

        def get_task_from_index(index, p_day_ago):
            for p_task in tasks:
                if p_task.index == index and p_task.day_ago == p_day_ago:
                    return p_task
        day_ago_for_next_update = []
        current_day_ago = self.day_ago if day_ago is None else day_ago
        if tasks is None:
            tasks = self.get_tasks_at_day_ago(day_ago=current_day_ago)
        for task in tasks:
            if task.index == 0:
                if current_day_ago != task.day_ago:
                    current_day_ago = task.day_ago
                from gestion.stores.plan_prod_store import plan_prod_store
                start_day = timestamp_at_time(timestamp_at_day_ago(day_ago=current_day_ago), hours=DEBUT_PROD_MATIN)
                last_plan_prod = plan_prod_store.get_last_plan_prod(start_plan_prod=start_day)
                task.plan_prod.update_from_start(start=start_day, last_plan_prod=last_plan_prod)
            else:
                last_plan_prod = get_task_from_index(task.index-1, p_day_ago=current_day_ago).plan_prod
                start = get_end_from_index_task(index=task.index-1, p_day_ago=current_day_ago)
                fin_prod = FIN_PROD_SOIR_VENDREDI if is_vendredi(last_plan_prod.start) else FIN_PROD_SOIR
                if start > timestamp_at_time(timestamp_at_day_ago(day_ago=current_day_ago), hours=fin_prod):
                    start = timestamp_at_time(timestamp_at_day_ago(day_ago=current_day_ago-1), hours=DEBUT_PROD_MATIN-1)
                    task.plan_prod.update_from_start(start=start, last_plan_prod=last_plan_prod)
                    if current_day_ago-1 not in day_ago_for_next_update:
                        day_ago_for_next_update.append(current_day_ago-1)
                else:
                    task.plan_prod.update_from_start(start=start, last_plan_prod=last_plan_prod)
            self.update_plan_prod_on_database(plan_prod=task.plan_prod)
        from gestion.stores.plan_prod_store import plan_prod_store
        plan_prod_store.sort_plans_prods()
        if day_ago_for_next_update:
            for day_ago in day_ago_for_next_update:
                self.update_plans_prods(day_ago=day_ago)
        self.SETTINGS_CHANGED_SIGNAL.emit()

    def on_data_reglage_changed(self):
        self.plan_prod.ON_CHANGED_SIGNAL.emit()

    def save_plan_prod(self):
        if not self.plan_prod.new_plan:
            self.update_plan_prod_on_database(plan_prod=self.plan_prod)
        else:
            code_bobines_selected = get_code_bobine_selected(self.plan_prod.bobines_filles_selected)
            code_data_reglages = self.plan_prod.data_reglages.get_data_reglage_code()
            Database.create_plan_prod(p_id=self.plan_prod.p_id,
                                      bobine_papier=self.plan_prod.bobine_papier_selected.code,
                                      code_bobines_selected=code_bobines_selected,
                                      refente=self.plan_prod.refente_selected.code,
                                      start=self.plan_prod.start,
                                      longueur=self.plan_prod.longueur,
                                      tours=self.plan_prod.tours,
                                      bobine_poly=self.plan_prod.bobine_poly_selected.code,
                                      code_data_reglages=code_data_reglages,
                                      encrier_1=self.plan_prod.encrier_1.color,
                                      encrier_2=self.plan_prod.encrier_2.color,
                                      encrier_3=self.plan_prod.encrier_3.color)
            self.plan_prod.new_plan = False
            from gestion.stores.plan_prod_store import plan_prod_store
            plan_prod_store.plans_prods.append(self.plan_prod)
        self.update_plans_prods()
        self.SETTINGS_CHANGED_SIGNAL.emit()

    @staticmethod
    def update_plan_prod_on_database(plan_prod):
        code_bobines_selected = get_code_bobine_selected(plan_prod.bobines_filles_selected)
        code_data_reglages = plan_prod.data_reglages.get_data_reglage_code()
        Database.update_plan_prod(p_id=plan_prod.p_id,
                                  bobine_papier=plan_prod.bobine_papier_selected.code,
                                  code_bobines_selected=code_bobines_selected,
                                  refente=plan_prod.refente_selected.code,
                                  start=plan_prod.start,
                                  longueur=plan_prod.longueur,
                                  tours=plan_prod.tours,
                                  bobine_poly=plan_prod.bobine_poly_selected.code,
                                  code_data_reglages=code_data_reglages,
                                  encrier_1=plan_prod.encrier_1.color,
                                  encrier_2=plan_prod.encrier_2.color,
                                  encrier_3=plan_prod.encrier_3.color)

    def save_event(self, event):
        Database.create_event_prod(start=event.start, end=event.end, p_type=event.type_event, info=event.info,
                                   ensemble=event.ensemble)
        from gestion.stores.event_store import event_store
        event_store.update()
        self.SETTINGS_CHANGED_SIGNAL.emit()

    def delete_item(self):
        from commun.model.event import Event
        from commun.model.plan_prod import PlanProd
        if isinstance(self.focus, Event):
            self.delete_event(event=self.focus)
        if isinstance(self.focus, PlanProd):
            self.delete_plan_prod(plan_prod=self.focus)

    def delete_event(self, event):
        Database.delete_event_prod(p_id=event.p_id)
        from gestion.stores.event_store import event_store
        event_store.update()
        self.SETTINGS_CHANGED_SIGNAL.emit()

    def delete_plan_prod(self, plan_prod):
        Database.delete_plan_prod(p_id=plan_prod.p_id)
        from gestion.stores.plan_prod_store import plan_prod_store
        plan_prod_store.plans_prods.remove(plan_prod)
        self.update_plans_prods()
        self.SETTINGS_CHANGED_SIGNAL.emit()


settings_store_gestion = SettingsStore()
