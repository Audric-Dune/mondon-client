# !/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtCore import pyqtSignal, QObject
from statistics import mean
from lib.base_de_donnee import Database
from constants.param import VITESSE_MOYENNE_MAXI, DEBUT_PROD_MATIN, FIN_PROD_SOIR, FIN_PROD_SOIR_VENDREDI
from stores.data_store_manager import data_store_manager

from ui.utils.timestamp import timestamp_at_week_ago,\
    timestamp_now,\
    timestamp_to_week,timestamp_to_month,\
    timestamp_at_month_ago,\
    timestamp_after_day_ago,\
    timestamp_to_day,\
    timestamp_at_time


class StatStore(QObject):
    SETTINGS_STAT_CHANGED_SIGNAL = pyqtSignal()
    DATA_STAT_CHANGED_SIGNAL = pyqtSignal()

    def __init__(self):
        super(StatStore, self).__init__()
        self.stat = None
        self.time_stat = None
        self.format = None
        self.displays = [False, False, True]
        self.raison = -1
        self.week_ago = -1
        self.month_ago = -1
        self.years_ago = -1
        self.data = []
        self.get_format()
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
            dic = {"values": [], "ts": [], "moyenne": 0, "percent": 0}
            self.data.append(dic)
            i += 1
        current_ts_day = start_ts
        for metrage in metrages:
            current_day = timestamp_to_day(current_ts_day)
            we = current_day == "samedi" or current_day == "dimanche"
            if not we:
                metrage_matin = metrage[1]
                metrage_soir = metrage[2]
                metrage_total = metrage_matin + metrage_soir
                self.data[0]["values"].append(metrage_matin)
                self.data[1]["values"].append(metrage_soir)
                self.data[2]["values"].append(metrage_total)
                self.data[0]["ts"].append(current_ts_day)
            current_ts_day = timestamp_after_day_ago(start=current_ts_day, day_ago=1)
        current_day = timestamp_to_day(current_ts_day)
        vendredi = current_day == "vendredi"
        if timestamp_now() < timestamp_at_time(current_ts_day, hours=FIN_PROD_SOIR_VENDREDI if vendredi else FIN_PROD_SOIR) :
            metrage_matin = data_store_manager.get_current_store().metrage_matin
            metrage_soir = data_store_manager.get_current_store().metrage_soir
            metrage_total = metrage_matin + metrage_soir
            self.data[0]["values"].append(metrage_matin)
            self.data[1]["values"].append(metrage_soir)
            self.data[2]["values"].append(metrage_total)
            self.data[0]["ts"].append(current_ts_day)
        self.stat_calculator(start_ts, end_ts)
        self.DATA_STAT_CHANGED_SIGNAL.emit()

    def stat_calculator(self, start, end):
        if self.stat == "métrage":
            maxi = self.get_max_prod(start, end)
            maxi = 1 if maxi == 0 else maxi
            index = 0
            for dic in self.data:
                current_maxi = maxi if index == 2 else maxi/2
                if self.data[index]["values"]:
                    dic["moyenne"] = round(mean(self.data[index]["values"]))
                dic["percent"] = round(sum(self.data[index]["values"])*100/current_maxi, 2)
                index += 1

    def get_max_prod(self, start, end):
        hour_worked = 0
        time_worked = 0
        current_ts_day = start
        while current_ts_day <= timestamp_at_time(end):
            current_day = timestamp_to_day(current_ts_day)
            vendredi = current_day == "vendredi"
            we = current_day == "samedi" or current_day == "dimanche"
            if timestamp_now() < timestamp_at_time(current_ts_day, hours=FIN_PROD_SOIR_VENDREDI if vendredi else FIN_PROD_SOIR) :
                time_worked += end - timestamp_at_time(end, hours=DEBUT_PROD_MATIN)
            elif not we:
                hour_worked += FIN_PROD_SOIR_VENDREDI-DEBUT_PROD_MATIN if vendredi else FIN_PROD_SOIR-DEBUT_PROD_MATIN
            current_ts_day = timestamp_after_day_ago(start=current_ts_day, day_ago=1)
        time_worked += hour_worked * 3600
        time_worked = 1 if time_worked == 0 else time_worked
        max_prod = round(VITESSE_MOYENNE_MAXI / 60 * time_worked)
        return max_prod

    def update_param(self):
        if not self.stat:
            self.stat = "métrage"
        if self.week_ago < 0 and self.month_ago < 0 and self.years_ago < 0:
            self.month_ago = 0
        if self.week_ago >= 0:
            self.time_stat = timestamp_to_week(timestamp_at_week_ago(self.week_ago)).capitalize()
        if self.month_ago >= 0:
            self.time_stat = timestamp_to_month(timestamp_at_month_ago(self.month_ago)).capitalize()
        self.get_format()

    def get_format(self):
        if self.week_ago >= 0:
            self.format = "week"
        if self.month_ago >= 0:
            self.format = "month"
        if self.years_ago >= 0:
            self.format = "years"

    def get_start_end(self):
        start_ts = 0
        end_ts = 0
        if self.week_ago >= 0:
            start_ts = timestamp_at_week_ago(self.week_ago)
            if self.week_ago == 0:
                end_ts = timestamp_now()
            else:
                end_ts = timestamp_at_week_ago(self.week_ago - 1)
        if self.month_ago >= 0:
            start_ts = timestamp_at_month_ago(self.month_ago)
            if self.month_ago == 0:
                end_ts = timestamp_now()
            else:
                end_ts = timestamp_at_month_ago(self.month_ago - 1)
        return start_ts, end_ts

    def update_time_ago(self, delta):
        if self.week_ago >= 0:
            self.week_ago += delta
        if self.month_ago >= 0:
            self.month_ago += delta
        if self.years_ago >= 0:
            self.years_ago += delta
        self.get_data()
        self.DATA_STAT_CHANGED_SIGNAL.emit()
        self.SETTINGS_STAT_CHANGED_SIGNAL.emit()

    def set_new_settings(self, week_ago=-1, month_ago=-1, years_ago=-1):
        self.week_ago = week_ago
        self.month_ago = month_ago
        self.years_ago = years_ago
        if self.week_ago >= 0:
            self.displays = [True, True, True]
        else:
            self.displays = [False, False, True]
        self.get_data()
        self.SETTINGS_STAT_CHANGED_SIGNAL.emit()

    def on_select_checkbox_display(self, index):
        self.displays[index] = False if self.displays[index] else True

stat_store = StatStore()
