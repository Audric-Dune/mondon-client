# !/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import timedelta

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLabel, QVBoxLayout

from constants.colors import color_bleu_gris
from constants.param import (DEBUT_PROD_MATIN,
                             FIN_PROD_MATIN,
                             FIN_PROD_MATIN_VENDREDI,
                             FIN_PROD_SOIR,
                             FIN_PROD_SOIR_VENDREDI)
from constants.stylesheets import white_title_label_stylesheet, red_title_label_stylesheet, green_title_label_stylesheet, black_16_label_stylesheet, black_20_label_stylesheet, green_16_label_stylesheet, red_16_no_background_label_stylesheet
from stores.data_store_manager import data_store_manager
from ui.utils.timestamp import timestamp_to_day
from ui.utils.data import affiche_entier, get_ratio_prod
from ui.widgets.prod.chart_stat.bar import Bar
from ui.widgets.public.mondon_widget import MondonWidget


class StatBar(MondonWidget):
    HEIGHT_BAR = 35

    def __init__(self, parent=None, titre="", moment="", mode="ui"):
        super(StatBar, self).__init__(parent=parent)
        if mode == "ui":
            self.set_background_color(color_bleu_gris)
        self.mode = mode
        self.moment = moment
        self.metre_value = 0
        self.arret_time = 0
        self.imprevu_arret_time = 0
        self.percent = 0
        # _____INIT_WIDGET____
        self.vbox = QVBoxLayout(self)
        self.title = QLabel(titre, self)
        self.bar = Bar(parent=self, percent=round(self.percent, 1), mode=self.mode)
        self.metre = QLabel(self)
        self.arret = QLabel(self)
        self.arret_imprevu = QLabel(self)
        self.arret_prevu = QLabel(self)
        self.init_widget()
        self.update_widgets()

    def init_widget(self):
        self.vbox.setContentsMargins(5, 5, 5, 5)

        self.title.setStyleSheet(white_title_label_stylesheet if self.mode == "ui" else black_20_label_stylesheet)
        self.vbox.addWidget(self.title, alignment=Qt.AlignLeft)

        self.bar.setFixedHeight(self.HEIGHT_BAR)
        self.vbox.addWidget(self.bar)

        self.metre.setStyleSheet(white_title_label_stylesheet if self.mode == "ui" else black_16_label_stylesheet)
        self.vbox.addWidget(self.metre, alignment=Qt.AlignLeft)

        self.arret.setStyleSheet(white_title_label_stylesheet if self.mode == "ui" else black_16_label_stylesheet)
        self.vbox.addWidget(self.arret, alignment=Qt.AlignLeft)

        self.arret_prevu.setStyleSheet(white_title_label_stylesheet if self.mode == "ui" else black_16_label_stylesheet)
        self.vbox.addWidget(self.arret_prevu, alignment=Qt.AlignLeft)

        self.arret_imprevu.setStyleSheet(red_title_label_stylesheet if self.mode == "ui" else black_16_label_stylesheet)
        self.vbox.addWidget(self.arret_imprevu, alignment=Qt.AlignLeft)

        self.setLayout(self.vbox)

    def on_settings_changed(self, prev_live, prev_day_ago, prev_zoom):
        self.update_widgets()

    def on_data_changed(self):
        self.update_widgets()

    def update_widgets(self):
        self.get_stat()
        self.metre.setText("{metre}m".format(metre=affiche_entier(s=str(round(self.metre_value)))))
        arret_time_str = str(timedelta(seconds=round(self.arret_time)))
        self.arret.setText("{time} d'arrêt cumulé".format(time=arret_time_str))

        arret_prevu_time_str = str(timedelta(seconds=round(self.arret_time - self.imprevu_arret_time)))
        self.arret_prevu.setText("{time} d'arrêt prévu".format(time=arret_prevu_time_str))
        self.bar.set_percent(self.percent)

        if self.imprevu_arret_time == 0:
            self.arret_imprevu.setStyleSheet(green_title_label_stylesheet if self.mode == "ui"
                                             else green_16_label_stylesheet)
        else:
            self.arret_imprevu.setStyleSheet(red_title_label_stylesheet if self.mode == "ui"
                                             else red_16_no_background_label_stylesheet)
        arret_imprevu_time_str = str(timedelta(seconds=round(self.imprevu_arret_time)))
        self.arret_imprevu.setText("{time} d'arrêt imprévu".format(time=arret_imprevu_time_str))

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

    def get_stat(self):
        current_store = data_store_manager.get_current_store()
        metrage_matin = current_store.metrage_matin
        metrage_soir = current_store.metrage_soir
        arret_time_matin = current_store.arret_time_matin
        imprevu_arret_time_matin = current_store.imprevu_arret_time_matin
        arret_time_soir = current_store.arret_time_soir
        imprevu_arret_time_soir = current_store.imprevu_arret_time_soir

        if self.moment == "matin":
            result = metrage_matin
            arret_time = arret_time_matin
            imprevu_arret_time = imprevu_arret_time_matin
        elif self.moment == "soir":
            result = metrage_soir
            arret_time = arret_time_soir
            imprevu_arret_time = imprevu_arret_time_soir
        else:
            result = metrage_matin + metrage_soir
            arret_time = arret_time_matin + arret_time_soir
            imprevu_arret_time = imprevu_arret_time_matin + imprevu_arret_time_soir

        self.metre_value = result
        self.arret_time = arret_time
        self.imprevu_arret_time = imprevu_arret_time
        self.percent = get_ratio_prod(self.moment)
