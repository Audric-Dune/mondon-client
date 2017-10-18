# !/usr/bin/env python
# -*- coding: utf-8 -*-

import threading

from ui.utils.timestamp import timestamp_at_day_ago, timestamp_at_time
from stores.data_store import DataStore
from stores.settings_store import settings_store


class DataStoreManager:
    def __init__(self):
        self.listeners = []
        self.dic_data_store = {}
        self.store = None
        self.refresh_timer = None
        settings_store.add_listener(self.get_store)
        self.get_store()

    def add_listener(self, fonction):
        self.listeners.append(fonction)

    def call_listener(self):
        for fonction in self.listeners:
            fonction()

    def get_store(self, *args):
        jour = timestamp_at_day_ago(settings_store.day_ago)
        jour_str = str(jour)
        if self.dic_data_store.get(jour_str):
            self.store = self.dic_data_store[jour_str]
        else:
            start = timestamp_at_time(jour, hours=6)
            end = timestamp_at_time(jour, hours=22)
            self.store = DataStore(start, end)
            self.dic_data_store[jour_str] = self.store
        self.refresh_data(force_refresh=True)

    def cancel_refresh(self):
        if self.refresh_timer:
            self.refresh_timer.cancel()

    def get_most_recent_store(self):
        most_recent_store = None
        most_recent_timestamp = 0
        for key in self.dic_data_store.keys():
            timestamp = float(key)
            if timestamp > most_recent_timestamp:
                most_recent_timestamp = timestamp
                most_recent_store = self.dic_data_store[key]
        return most_recent_store

    def refresh_data(self, force_refresh=False):
        if self.refresh_timer:
            self.refresh_timer.cancel()
        # self.get_most_recent_store().add_data()
        if self.store.add_data() or force_refresh:
            self.call_listener()
        self.refresh_timer = threading.Timer(1, self.refresh_data)
        self.refresh_timer.start()

data_store_manager = DataStoreManager()
