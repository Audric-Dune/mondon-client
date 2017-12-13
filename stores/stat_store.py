# !/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtCore import pyqtSignal, QObject
from lib.base_de_donnee import Database
from constants.param import VITESSE_MOYENNE_MAXI, DEBUT_PROD_MATIN, FIN_PROD_SOIR, FIN_PROD_SOIR_VENDREDI

from ui.utils.timestamp import timestamp_at_week_ago, timestamp_now, timestamp_to_week


class StatStore(QObject):
    SETTINGS_STAT_CHANGED_SIGNAL = pyqtSignal()
    DATA_STAT_CHANGED_SIGNAL = pyqtSignal()

    def __init__(self):
        super(StatStore, self).__init__()
        self.stat = None
        self.time_stat = None
        self.raison = -1
        self.week_ago = -1
        self.month_ago = -1
        self.years_ago = -1
        self.data = []
        self.get_data()

    def get_data(self):
        self.data = []
        self.update_param()
        time = self.get_start_end()
        start_ts = time[0]
        end_ts = time[1]
        metrages = Database.get_metrages(start_time=start_ts, end_time=end_ts)
        metrages.sort()
        i = 0
        while i < 3:
            dic = {"values": [], "moyenne": 0, "percent": 0}
            self.data.append(dic)
            i += 1
        for metrage in metrages:
            metrage_matin = metrage[1]
            metrage_soir = metrage[2]
            metrage_total = metrage_matin + metrage_soir
            self.data[2]["values"].append(metrage_total)
            self.data[0]["values"].append(metrage_matin)
            self.data[1]["values"].append(metrage_soir)
        self.stat_calculator()

    def stat_calculator(self):
        if self.stat == "métrage":
            if self.week_ago >= 0:
                number_of_hours = (FIN_PROD_SOIR-DEBUT_PROD_MATIN)*4+(FIN_PROD_SOIR_VENDREDI-DEBUT_PROD_MATIN)
                maxi = VITESSE_MOYENNE_MAXI*number_of_hours*60
                index = 0
                for dic in self.data:
                    current_maxi = maxi if index == 2 else maxi/2
                    print(maxi)
                    dic["moyenne"] = round(sum(self.data[index]["values"])/5)
                    dic["percent"] = round(sum(self.data[index]["values"])*100/current_maxi)
                    index += 1

    def update_param(self):
        if not self.stat:
            self.stat = "métrage"
        if self.week_ago < 0 and self.month_ago < 0 and self.years_ago < 0:
            self.week_ago = 0
        if self.week_ago >= 0:
            self.time_stat = timestamp_to_week(timestamp_at_week_ago(self.week_ago))

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
