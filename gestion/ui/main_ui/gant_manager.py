# !/usr/bin/env python
# -*- coding: utf-8 -*-

from commun.lib.base_de_donnee import Database
from commun.utils.timestamp import timestamp_at_day_ago

from gestion.stores.settings_store import settings_store_gestion
from gestion.ui.main_ui.gant_prod import GantProd


class GantManager:
    def __init__(self):
        self.prods = []
        self.events = []
        self.gant_prod = GantProd(prods=self.prods, events=self.events)
        self.update_data()
        settings_store_gestion.SETTINGS_CHANGED_SIGNAL.connect(self.update_data)

    def update_data(self):
        day_ago = settings_store_gestion.day_ago
        self.prods = self.get_prods(start=timestamp_at_day_ago(day_ago))
        self.events = self.get_events(start=timestamp_at_day_ago(day_ago))
        self.gant_prod.update_data(prods=self.prods, events=self.events, day_ago=day_ago)

    @staticmethod
    def get_prods(start):
        from gestion.stores.plan_prod_store import plan_prod_store
        prods = []
        for prod in plan_prod_store.plans_prods:
            if prod.start >= start:
                prods.append(prod)
        return prods

    @staticmethod
    def get_events(start):
        from gestion.stores.event_store import event_store
        events = []
        for event in event_store.events:
            if event.start >= start:
                events.append(event)
        return events
