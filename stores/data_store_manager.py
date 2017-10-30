# !/usr/bin/env python
# -*- coding: utf-8 -*-

import threading
from PyQt5.QtCore import pyqtSignal, QObject

from ui.utils.timestamp import timestamp_at_day_ago, timestamp_at_time
from stores.data_store import DataStore
from stores.settings_store import settings_store


class DataStoreManager(QObject):
    DATA_CHANGED_SIGNAL = pyqtSignal()

    def __init__(self):
        super(DataStoreManager, self).__init__()
        self.dic_data_store = {}
        self.current_store = None
        self.refresh_timer = None
        settings_store.SETTINGS_CHANGED_SIGNAL.connect(self.update_current_store)
        self.update_current_store()

    def update_current_store(self, *args):
        jour = timestamp_at_day_ago(settings_store.day_ago)
        jour_str = str(jour)
        if self.dic_data_store.get(jour_str):
            self.current_store = self.dic_data_store[jour_str]
        else:
            start = timestamp_at_time(jour, hours=6)
            end = timestamp_at_time(jour, hours=22)
            self.current_store = DataStore(start, end, settings_store.day_ago)
            self.dic_data_store[jour_str] = self.current_store
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

    def get_current_store(self):
        return self.current_store

    def refresh_data(self, force_refresh=False):
        if self.refresh_timer:
            self.refresh_timer.cancel()

        # Récupération du DataStore du jour qui est actuellement affiché
        current_store = self.get_current_store()
        # Récupération du DataStore le plus récent (celui d'aujourd'hui)
        most_recent_store = self.get_most_recent_store()

        # Création d'un "set" des DataStore à mettre à jour.
        # Le set s'occupe automatiquement d'enlevé les valeurs dupliquées, donc
        # on n'essayera pas de mettre à jour le même DataStore deux fois si le
        # DataStore actuellement affiché est aussi le plus récent
        stores_to_update = set([current_store, most_recent_store])

        # Mets à jour les stores
        should_refresh = force_refresh
        for store in stores_to_update:
            new_data = store.add_data()
            should_refresh = new_data or should_refresh

        # Envois un signal que les data ont changées si nécessaire
        if should_refresh:
            self.DATA_CHANGED_SIGNAL.emit()

        # Ré-exécute la fonction dans 1 seconde
        self.refresh_timer = threading.Timer(0.5, self.refresh_data)
        self.refresh_timer.start()

data_store_manager = DataStoreManager()
