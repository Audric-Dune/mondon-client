# !/usr/bin/env python
# -*- coding: utf-8 -*-
import time
from datetime import timedelta

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLabel, QVBoxLayout

from constants.colors import color_bleu_gris
from constants.param import (DEBUT_PROD_MATIN,
                             FIN_PROD_MATIN,
                             FIN_PROD_MATIN_VENDREDI,
                             FIN_PROD_SOIR,
                             FIN_PROD_SOIR_VENDREDI)
from constants.stylesheets import white_title_label_stylesheet, red_title_label_stylesheet, green_title_label_stylesheet
from stores.data_store_manager import data_store_manager
from stores.settings_store import settings_store
from ui.utils.timestamp import (
    timestamp_at_day_ago,
    timestamp_at_time,
    timestamp_now,
    timestamp_to_day,
)
from ui.utils.data import affiche_entier
from ui.widgets.prod.chart_stat.bar import Bar
from ui.widgets.public.mondon_widget import MondonWidget


class StatBar(MondonWidget):
    HEIGHT_BAR = 50

    def __init__(self, parent, titre, moment):
        super(StatBar, self).__init__(parent=parent)
        self.set_background_color(color_bleu_gris)
        self.moment = moment
        self.imprevu_arret_time = 0
        self.metre_value = 0
        self.percent = 0
        self.arret_time_str = ""
        self.arret_imprevu_time_str = ""
        self.day_ago = 0
        # _____INIT_WIDGET____
        self.vbox = QVBoxLayout(self)
        self.title = QLabel(titre, self)
        self.bar = Bar(parent=self, percent=round(self.percent, 1))
        self.metre = QLabel(self)
        self.arret = QLabel(self)
        self.arret_imprevu = QLabel(self)
        self.init_widget()
        self.update_widgets()

    def init_widget(self):
        self.vbox.setContentsMargins(5, 5, 5, 5)

        self.title.setStyleSheet(white_title_label_stylesheet)
        self.vbox.addWidget(self.title, alignment=Qt.AlignLeft)

        self.bar.setFixedHeight(self.HEIGHT_BAR)
        self.vbox.addWidget(self.bar)

        self.metre.setStyleSheet(white_title_label_stylesheet)
        self.vbox.addWidget(self.metre, alignment=Qt.AlignLeft)

        self.arret.setStyleSheet(white_title_label_stylesheet)
        self.vbox.addWidget(self.arret, alignment=Qt.AlignLeft)

        self.arret_imprevu.setStyleSheet(red_title_label_stylesheet)
        self.vbox.addWidget(self.arret_imprevu, alignment=Qt.AlignLeft)

        self.setLayout(self.vbox)

    def on_settings_changed(self, prev_live, prev_day_ago, prev_zoom):
        self.day_ago = settings_store.day_ago
        self.update_widgets()

    def on_data_changed(self):
        self.update_widgets()

    def update_widgets(self):
        self.get_stat()
        self.metre.setText("{metre}m".format(metre=affiche_entier(s=str(round(self.metre_value)))))
        self.arret.setText("{time} d'arrêt machine".format(time=self.arret_time_str))
        if self.imprevu_arret_time == 0:
            self.arret_imprevu.setStyleSheet(green_title_label_stylesheet)
        else:
            self.arret_imprevu.setStyleSheet(red_title_label_stylesheet)
        self.arret_imprevu.setText("{time} d'arrêt imprévu".format(time=self.arret_imprevu_time_str))
        self.bar.get_percent(self.percent)

    def get_start_and_end(self, ts):
        vendredi = timestamp_to_day(ts) == "vendredi"
        start = DEBUT_PROD_MATIN
        mid = FIN_PROD_MATIN_VENDREDI if vendredi else FIN_PROD_MATIN
        end = FIN_PROD_SOIR_VENDREDI if vendredi else FIN_PROD_SOIR
        if self.moment == "matin":
            end = mid
        if self.moment == "soir":
            start = mid

        return start, end

    def get_arret_stat(self, ts):
        arret_time = 0
        self.imprevu_arret_time = 0
        time = self.get_start_and_end(ts)
        start_ts = timestamp_at_time(ts, hours=time[0])
        end_ts = timestamp_at_time(ts, hours=time[1])
        arrets = data_store_manager.get_current_store().arrets
        for arret in arrets:
            start_arret = arret[0]
            end_arret = arret[1]
            if start_ts <= start_arret <= end_ts:
                arret_delay = end_arret - start_arret
                arret_time = arret_time + arret_delay
                if arret[2]:
                    first_raison = arret[2][0]
                    if first_raison.type == "Imprévu":
                        self.imprevu_arret_time = self.imprevu_arret_time + arret_delay
        self.arret_time_str = str(timedelta(seconds=round(arret_time)))
        self.arret_imprevu_time_str = str(timedelta(seconds=round(self.imprevu_arret_time)))

    @staticmethod
    def get_live_stat(start, end):
        speeds = data_store_manager.get_current_store().data
        start_ts = start
        end_ts = end

        def value_is_in_period(value):
            return start_ts <= value[0] <= end_ts

        speeds = [v[1] for v in list(filter(value_is_in_period, speeds))]
        result = sum(speeds) / 60
        return result

    def get_stat(self):
        ts = timestamp_at_day_ago(self.day_ago)
        time = self.get_start_and_end(ts)
        start_ts = timestamp_at_time(ts, hours=time[0])
        end_ts = timestamp_at_time(ts, hours=time[1])

        metrage_matin = data_store_manager.get_current_store().metrage_matin
        metrage_soir = data_store_manager.get_current_store().metrage_soir
        if self.day_ago == 0 or not metrage_matin or not metrage_soir or True:
            result = self.get_live_stat(start=start_ts, end=end_ts)
        else:
            if self.moment == "matin":
                result = metrage_matin
            elif self.moment == "soir":
                result = metrage_soir
            else:
                result = metrage_matin + metrage_soir

        self.get_arret_stat(ts)

        ts_actuel = timestamp_now()
        if ts_actuel < end_ts:
            maxi = 180 * (ts_actuel - start_ts) / 6000
        else:
            maxi = 180 * (end_ts - start_ts) / 6000

        if maxi > 0:
            percent = result / maxi
            if percent > 100:
                percent = 100
        else:
            percent = 0

        if result <= 0:
            percent = 0

        self.metre_value = result
        self.percent = percent
