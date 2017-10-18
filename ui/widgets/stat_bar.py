# !/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import timedelta
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QLabel, QSizePolicy, QVBoxLayout, QWidget
from param import color_bleu_gris
from stores.data_store_manager import data_store_manager
from stores.settings_store import settings_store
from ui.utils.drawing import draw_rectangle
from ui.utils.timestamp import (
    timestamp_at_day_ago,
    timestamp_at_time,
    timestamp_now,
    timestamp_to_day,
)
from ui.widgets.bar import Bar


class StatBar(QWidget):
    def __init__(self, parent, titre, moment):
        super(StatBar, self).__init__(parent=parent)
        self.moment = moment
        self.metre_value = 0
        self.percent = 0
        self.time_at_0_str = ""
        self.day_ago = 0

        self.vbox = QVBoxLayout(self)
        self.vbox.setContentsMargins(5, 5, 5, 5)

        self.title = QLabel(titre, self)
        self.title.setAlignment(Qt.AlignLeft)
        self.title.setStyleSheet("QLabel {color: rgb(255, 255, 255); font-size: 16px;}")

        self.bar = Bar(parent=self, percent=round(self.percent, 1))
        self.bar.setSizePolicy(QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding))

        self.metre = QLabel(self)
        self.metre.setAlignment(Qt.AlignLeft)
        self.metre.setStyleSheet("QLabel {color: rgb(255, 255, 255); font-size: 16px;}")

        self.arret = QLabel(self)
        self.arret.setAlignment(Qt.AlignLeft)
        self.arret.setStyleSheet("QLabel {color: rgb(255, 255, 255); font-size: 16px;}")

        self.vbox.addWidget(self.title)
        self.vbox.addWidget(self.bar)
        self.vbox.addWidget(self.metre)
        self.vbox.addWidget(self.arret)

        self.setLayout(self.vbox)

        data_store_manager.add_listener(self.update_bar)
        settings_store.add_listener(self.get_setting)
        self.update_widgets()

    def paintEvent(self, event):
        p = QPainter()
        p.begin(self)
        self.draw(p)
        p.end()

    def get_setting(self, prev_live, prev_day_ago, prev_zoom):
        self.day_ago = settings_store.day_ago
        self.update_widgets()

    def update_bar(self):
        self.update_widgets()

    def update_widgets(self):
        self.get_stat()
        self.metre.setText("{metre}m".format(metre=self.affiche_entier(round(self.metre_value))))
        self.arret.setText("{time} d'arrêt machine".format(time = self.time_at_0_str))
        self.bar.get_percent(self.percent)
        self.update()

    def affiche_entier(self, s, sep=' '):
        s = str(s)
        if len(s) <= 3:
            return s
        else:
            return self.affiche_entier(s[:-3]) + sep + s[-3:]

    def get_stat(self):
        ts_actuel = timestamp_now()
        speeds = data_store_manager.store.data
        ts = timestamp_at_day_ago(self.day_ago)

        vendredi = timestamp_to_day(ts) == "Vendredi"
        start = 6
        mid = 13 if vendredi else 14
        end = 20 if vendredi else 22

        if self.moment == "matin":
            end = mid
        if self.moment == "soir":
            start = mid

        start_ts = timestamp_at_time(ts, hours=start)
        end_ts = timestamp_at_time(ts, hours=end)

        def value_is_in_period(value):
            return start_ts <= value[0] <= end_ts

        def speed_is_low(value):
            return 0 <= value <= 30

        speeds = [v[1] for v in list(filter(value_is_in_period, speeds))]
        low_speeds = list(filter(speed_is_low, speeds))

        result = sum(speeds) / 60
        time_at_0 = len(low_speeds)

        if ts_actuel < end_ts:
            maxi = 172.5 * (ts_actuel - start_ts) / 6000
        else:
            maxi = 172.5 * (end_ts - start_ts) / 6000
        if maxi > 0:
            percent = result / maxi
        else:
            percent = 0
        if result <= 0:
            percent = 0
        time_at_0_str = str(timedelta(seconds=round(time_at_0)))
        self.metre_value = result
        self.percent = percent
        self.time_at_0_str = time_at_0_str

    def draw(self, p):
        draw_rectangle(p, 0, 0, self.width(), self.height(), color_bleu_gris)
