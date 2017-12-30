# !/usr/bin/env python
# -*- coding: utf-8 -*-

import threading
from PyQt5.QtCore import pyqtSignal, QObject

from constants.param import DEBUT_PROD_MATIN, FIN_PROD_SOIR

from ui.utils.timestamp import timestamp_at_day_ago, timestamp_at_time
from stores.data_store import DataStore
from stores.settings_store import settings_store


class DataStoreManager(QObject):
    DATA_CHANGED_SIGNAL = pyqtSignal()
    NEW_ARRET_SIGNAL = pyqtSignal(int, int)

    def __init__(self):
        super(DataStoreManager, self).__init__()
        self.dic_data_store = {}
        self.current_store = None
        self.refresh_timer = None
        settings_store.SETTINGS_CHANGED_SIGNAL.connect(self.handle_settings_change)
        self.update_current_store()

    def handle_settings_change(self):
        self.update_current_store()
        self.refresh_data(force_refresh=True)

    def refresh_once(self, force_refresh):
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
            new_data, list_new_arret = store.add_data()
            should_refresh = new_data or should_refresh
            if list_new_arret:
                for start_arret in list_new_arret:
                    if settings_store.day_ago == 0:
                        self.NEW_ARRET_SIGNAL.emit(start_arret, store.day_ago)
        from stores.stat_store import stat_store
        stat_store.update_data()
        # Envois un signal que les data ont changées si nécessaire
        if should_refresh:
            self.DATA_CHANGED_SIGNAL.emit()

    def update_current_store(self, *args):
        jour = timestamp_at_day_ago(settings_store.day_ago)
        jour_str = str(jour)
        if self.dic_data_store.get(jour_str):
            self.current_store = self.dic_data_store[jour_str]
        else:
            start = timestamp_at_time(jour, hours=DEBUT_PROD_MATIN)
            end = timestamp_at_time(jour, hours=FIN_PROD_SOIR)
            self.current_store = DataStore(start, end, settings_store.day_ago)
            self.dic_data_store[jour_str] = self.current_store

    def add_new_store(self, ts):
        jour = ts
        jour_str = str(jour)
        start = timestamp_at_time(jour, hours=DEBUT_PROD_MATIN)
        end = timestamp_at_time(jour, hours=FIN_PROD_SOIR)
        new_store = DataStore(start, end, settings_store.day_ago)
        self.dic_data_store[jour_str] = new_store
        return new_store

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

    def get_store_at_day_ago(self, day_ago):
        jour = timestamp_at_day_ago(day_ago)
        jour_str = str(jour)
        return self.dic_data_store.get(jour_str, False)

    def get_store_at_time(self, ts):
        jour_str = str(round(ts))
        return self.dic_data_store.get(jour_str, False)

    def refresh_data(self, force_refresh=False):
        if self.refresh_timer:
            self.refresh_timer.cancel()
        self.refresh_once(force_refresh)
        # Ré-exécute la fonction dans 1 seconde
        self.refresh_timer = threading.Timer(1, self.refresh_data)
        self.refresh_timer.start()

data_store_manager = DataStoreManager()
