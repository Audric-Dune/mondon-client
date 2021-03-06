# !/usr/bin/env python
# -*- coding: utf-8 -*-

import threading
import time

from PyQt5.QtCore import pyqtSignal, QObject

from commun.constants.param import DEBUT_PROD_MATIN, FIN_PROD_SOIR
from commun.utils.timestamp import timestamp_at_day_ago,\
    timestamp_at_time,\
    timestamp_now,\
    get_day_ago

from production.stores.data_store import DataStore
from production.stores.settings_store import settings_store
from production.stores.user_store import user_store


class DataStoreManager(QObject):
    DATA_CHANGED_SIGNAL = pyqtSignal()
    NEW_ARRET_SIGNAL = pyqtSignal(int, int)
    SLEEP_TIME = 0.5

    def __init__(self):
        super(DataStoreManager, self).__init__()
        self.dic_data_store = {}
        self.current_store = None
        self.refresh_timer = None
        self.is_running = False
        settings_store.SETTINGS_CHANGED_SIGNAL.connect(self.handle_settings_change)
        self.update_current_store()

    def handle_settings_change(self):
        self.update_current_store()
        self.refresh_data()

    def refresh_once(self, force_refresh):
        # Récupération du DataStore du jour qui est actuellement affiché
        current_store = self.get_current_store()

        # Mets à jour le store courant
        should_refresh = force_refresh
        new_data, list_new_arret = current_store.add_data()
        should_refresh = new_data or should_refresh
        self.check_create_window_new_arret(current_store)
        from production.stores.stat_store import stat_store
        stat_store.update_data()
        # Envois un signal que les data ont changées si nécessaire
        if should_refresh:
            self.DATA_CHANGED_SIGNAL.emit()

    def check_create_window_new_arret(self, store):
        if settings_store.day_ago == 0 and user_store.user_level == 0:
            list_arrets = store.arrets
            if list_arrets:
                last_start_arret = list_arrets[-1][0]
                ts_now = timestamp_now()
                if ts_now - last_start_arret < 10:
                    self.NEW_ARRET_SIGNAL.emit(last_start_arret, 0)

    def update_current_store(self, *args):
        jour = round(timestamp_at_day_ago(settings_store.day_ago))
        jour_str = str(jour)
        if self.dic_data_store.get(jour_str):
            self.current_store = self.dic_data_store[jour_str]
        else:
            start = timestamp_at_time(jour, hours=DEBUT_PROD_MATIN)
            end = timestamp_at_time(jour, hours=FIN_PROD_SOIR)
            self.current_store = DataStore(start, end, settings_store.day_ago)
            self.dic_data_store[jour_str] = self.current_store

    def add_new_store(self, ts):
        jour = round(ts)
        jour_str = str(jour)
        day_ago = get_day_ago(ts)
        start = timestamp_at_time(jour, hours=DEBUT_PROD_MATIN)
        end = timestamp_at_time(jour, hours=FIN_PROD_SOIR)
        new_store = DataStore(start, end, day_ago)
        self.dic_data_store[jour_str] = new_store
        return new_store

    def stop(self):
        while self.is_running:
            time.sleep(0.1)
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
        jour = round(timestamp_at_day_ago(day_ago))
        jour_str = str(jour)
        return self.dic_data_store.get(jour_str, False)

    def get_store_at_time(self, ts):
        jour_str = str(round(ts))
        return self.dic_data_store.get(jour_str, False)

    def refresh_data(self, force_refresh=False):
        self.is_running = True
        if self.refresh_timer:
            self.refresh_timer.cancel()
        self.refresh_once(force_refresh)
        # Ré-exécute la fonction dans SLEEP_TIME seconde
        self.refresh_timer = threading.Timer(self.SLEEP_TIME, self.refresh_data)
        self.refresh_timer.daemon = True
        self.refresh_timer.start()
        self.is_running = False

data_store_manager = DataStoreManager()
