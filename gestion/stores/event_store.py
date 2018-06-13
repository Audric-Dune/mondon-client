# !/usr/bin/env python
# -*- coding: utf-8 -*-


from PyQt5.QtCore import QObject

from commun.lib.base_de_donnee import Database
from commun.constants.param import FIN_PROD_SOIR, FIN_PROD_SOIR_VENDREDI
from commun.utils.timestamp import timestamp_at_day_ago, timestamp_at_time

from gestion.stores.settings_store import settings_store_gestion


class EventStore(QObject):

    def __init__(self):
        super(EventStore, self).__init__()
        self.event_on_data_base = None
        settings_store_gestion.SETTINGS_CHANGED_SIGNAL.connect(self.update)
        self.events = []
        self.update()

    def update(self):
        self.get_event_from_database()

    def sort_events(self):
        self.events = sorted(self.events, key=lambda b: b.get_start(), reverse=False)

    def get_event_from_database(self):
        self.events = []
        event_on_data_base = Database.get_event_prod()
        start_ts = timestamp_at_day_ago(0)
        for event in event_on_data_base:
            if start_ts < event[2]:
                from commun.model.event import Event
                event = Event(p_type=event[1], start=event[2], end=event[3], info=event[4])
                self.events.append(event)
        self.sort_events()

    def add_defaut_stop_prod(self):
        day_ago = settings_store_gestion.day_ago
        start_defaut_stop_prod = timestamp_at_time(timestamp_at_day_ago(day_ago), hours=FIN_PROD_SOIR_VENDREDI)
        end_defaut_stop_prod = timestamp_at_time(timestamp_at_day_ago(day_ago), hours=FIN_PROD_SOIR)
        Database.create_event_prod(start=start_defaut_stop_prod, end=end_defaut_stop_prod, p_type="stop")
        self.update()


event_store = EventStore()
