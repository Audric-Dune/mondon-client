# !/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtCore import pyqtSignal, QObject
from lib.base_de_donnee import Database

from ui.utils.timestamp import timestamp_at_week_ago, timestamp_now


class StatStore(QObject):
    SETTINGS_STAT_CHANGED_SIGNAL = pyqtSignal()
    DATA_STAT_CHANGED_SIGNAL = pyqtSignal()

    def __init__(self):
        super(StatStore, self).__init__()
        self.stat = "metrage"
        self.raison = None
        self.week_ago = 0
        self.month_ago = None
        self.years_ago = None
        self.data_1 = []
        self.data_2 = []
        self.data_3 = []
        self.get_data()

    def get_data(self):
        self.init_data()
        time = self.get_start_end()
        start_ts = time[0]
        end_ts = time[1]
        metrages = Database.get_metrages(start_time=start_ts, end_time=end_ts)
        metrages.sort()
        for metrage in metrages:
            metrage_matin = metrage[1]
            metrage_soir = metrage[2]
            metrage_total = metrage_matin + metrage_soir
            self.data_1.append(metrage_total)
            self.data_2.append(metrage_matin)
            self.data_3.append(metrage_soir)

    def init_data(self):
        self.data_1 = []
        self.data_2 = []
        self.data_3 = []

    def get_start_end(self):
        start_ts = 0
        end_ts = 0
        if self.week_ago >= 0:
            start_ts = timestamp_at_week_ago(self.week_ago)
            if self.week_ago == 0:
                end_ts = timestamp_now()
            else:
                end_ts = timestamp_at_week_ago(self.week_ago - 1)
        return start_ts, end_ts

    def set_week_ago(self, week_ago):
        self.week_ago = week_ago
        self.get_data()
        self.DATA_STAT_CHANGED_SIGNAL.emit()
        self.SETTINGS_STAT_CHANGED_SIGNAL.emit()

stat_store = StatStore()
