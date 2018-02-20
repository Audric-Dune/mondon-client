# !/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel, QSizePolicy

from commun.constants import colors
from commun.constants.stylesheets import white_12_label_stylesheet,\
    gris_fonce_label_stylesheet,\
    gris_moyen_label_stylesheet,\
    vert_fonce_label_stylesheet,\
    blue_16_label_stylesheet,\
    red_16_label_stylesheet
from commun.lib.logger import logger
from commun.ui.public.checkbox_button import CheckboxButton
from commun.ui.public.mondon_widget import MondonWidget
from commun.utils.layout import clear_layout
from commun.utils.timestamp import timestamp_to_name_number_day_month,\
    timestamp_to_day_month_little,\
    timestamp_after_day_ago,\
    timestamp_to_day

from production.stores.settings_stat_store import settings_stat_store
from production.stores.stat_store import stat_store
from production.ui.widgets.stat.stat_chart_bar import StatChartBar


class ChartBar(MondonWidget):
    def __init__(self, parent=None):
        super(ChartBar, self).__init__(parent=parent)
        self.set_background_color(colors.color_bleu_gris)
        self.vbox = QVBoxLayout()
        self.chart_settings = ChartSettings(parent=self)
        self.content_chart = ContentChart(parent=self)
        self.chart_legend = ChartLegend(parent=self)
        self.on_settings_stat_changed()
        self.init_widget()

    def on_settings_stat_changed(self):
        if settings_stat_store.data_type == "raisons prévue" or settings_stat_store.data_type == "raisons imprévue":
            self.hide()
        else:
            self.show()

    def init_widget(self):
        self.vbox.setContentsMargins(10, 0, 10, 0)
        self.vbox.setSpacing(0)
        self.vbox.addWidget(self.chart_settings)
        self.vbox.addWidget(self.content_chart)
        self.content_chart.setSizePolicy(QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding))
        self.vbox.addWidget(self.chart_legend)
        self.setLayout(self.vbox)


class ContentChart(MondonWidget):
    BAR_CONTENT_SPACING = 0
    VALUE_LABEL_HEIGHT = 20

    def __init__(self, parent=None):
        super(ContentChart, self).__init__(parent=parent)
        self.background_color = colors.color_blanc
        self.color_data_métrage = [colors.color_gris_moyen, colors.color_gris_fonce, colors.color_vert_fonce]
        self.color_data_temps = [colors.color_bleu, colors.color_rouge, colors.color_gris_fonce]
        self.bars = []
        self.hbox = QHBoxLayout()
        try:
            self.init_widget()
        except:
            logger.log("CHART_STAT", "Erreur de mise à jour lors de l'initialisation du chart")

    def on_data_stat_changed(self):
        try:
            self.init_widget()
        except:
            logger.log("CHART_STAT", "Erreur de mise à jour lors du changement de data chart")

    def on_settings_stat_changed(self):
        try:
            self.on_loading(layout=self.hbox, gif_name="loader_white_green", set_text=True, size=40)
        except:
            logger.log("CHART_STAT", "Erreur d'affichage chargement")

    def on_settings_chart_changed(self):
        try:
            self.init_widget()
        except:
            logger.log("CHART_STAT", "Erreur de mise à jour lors du changement de settings du chart")

    def init_widget(self):
        clear_layout(self.hbox)
        self.bars = []
        self.hbox.setContentsMargins(10, 0, 10, 0)
        self.hbox.setSpacing(5)
        len_format = 0
        if settings_stat_store.format == "week":
            len_format = 5
        if settings_stat_store.format == "month":
            len_format = len(stat_store.data["total"])
        index = 0
        while index < len_format:
            hbox_multi_bar = QHBoxLayout()
            hbox_multi_bar.setContentsMargins(0, 0, 0, 0)
            hbox_multi_bar.setSpacing(0)
            index_data = 0
            while index_data < len(stat_store.data):
                if settings_stat_store.display_setting[index_data]:
                    if settings_stat_store.data_type == "métrage":
                        moment = "matin" if index_data == 0 else ""
                        moment = "soir" if index_data == 1 else moment
                        moment = "total" if index_data == 2 else moment
                    else:
                        moment = "Prévu" if index_data == 0 else ""
                        moment = "Imprévu" if index_data == 1 else moment
                        moment = "total" if index_data == 2 else moment
                    value = stat_store.data[moment][index][1] if len(stat_store.data[moment]) > index else -1
                    color = self.color_data_métrage[index_data] if settings_stat_store.data_type == "métrage"\
                        else self.color_data_temps[index_data]
                    hbox_multi_bar.addLayout(self.create_bar(value=value,
                                                             color=color))
                index_data += 1
            self.hbox.addLayout(hbox_multi_bar)
            index += 1
        self.setLayout(self.hbox)

    def create_bar(self, value, color):
        vbox = QVBoxLayout()
        bar = StatChartBar(color=color, value=value, max_value=stat_store.stat["total"]["max"], parent=self)
        self.bars.append((bar, value))
        vbox.addWidget(bar)
        return vbox


class ChartLegend(MondonWidget):
    LEGEND_LABEL_HEIGHT = 20

    def __init__(self, parent=None):
        super(ChartLegend, self).__init__(parent=parent)
        self.setFixedHeight(40)
        self.background_color = colors.color_bleu_gris
        self.hbox = QHBoxLayout(self)
        self.hbox.setSpacing(0)
        self.init_widget()

    def on_settings_stat_changed(self):
        self.on_loading(layout=self.hbox, gif_name="loader_blue_white", set_text=False, size=self.LEGEND_LABEL_HEIGHT)

    def on_data_stat_changed(self):
        self.update_widget()

    @staticmethod
    def is_weekend(ts_day):
        """
        Test si un ts correspond à un jour du weekend (samedi ou dimanche)
        :return: True si le ts correspond a un samedi ou dimanche sinon False
        """
        day = timestamp_to_day(ts_day)
        return day == "samedi" or day == "dimanche"

    def init_widget(self):
        len_format = 0
        start = 0
        if stat_store.data.get("total"):
            if settings_stat_store.format == "week":
                len_format = 5
            if settings_stat_store.format == "month":
                len_format = len(stat_store.data["total"])
            start = stat_store.data["total"][0][0]
        index = 0
        str_date = "NA"
        dec_weekend = 0
        while index < len_format:
            while self.is_weekend(timestamp_after_day_ago(start, day_ago=index + dec_weekend)):
                dec_weekend += 1
            ts = timestamp_after_day_ago(start, day_ago=index + dec_weekend)
            if settings_stat_store.format == "week":
                str_date = timestamp_to_name_number_day_month(ts).capitalize()
            if settings_stat_store.format == "month":
                str_date = timestamp_to_day_month_little(ts)
            self.hbox.addWidget(self.create_label(str_date))
            index += 1

    def update_widget(self):
        clear_layout(self.hbox)
        self.init_widget()

    def create_label(self, text):
        label = QLabel(str(text))
        label.setFixedHeight(self.LEGEND_LABEL_HEIGHT)
        label.setAlignment(Qt.AlignCenter | Qt.AlignBottom)
        label.setStyleSheet(white_12_label_stylesheet)
        return label


class ChartSettings(MondonWidget):
    CHART_SETTINGS_SIZE = QSize(20, 20)
    HEIGHT_LABEL = 20

    def __init__(self, parent=None):
        super(ChartSettings, self).__init__(parent=parent)
        self.setFixedHeight(40)
        self.background_color = colors.color_bleu_gris
        self.hbox = QHBoxLayout(self)
        self.init_widget()

    def on_settings_stat_changed(self):
        clear_layout(self.hbox)
        try:
            self.init_widget()
        except:
            logger.log("CHART_STAT", "Erreur de mise à jour lors du chargement des settings du chart")

    def init_widget(self):
        self.hbox.setSpacing(20)
        self.hbox.addStretch(1)
        texte = "Equipe matin" if settings_stat_store.data_type == "métrage" else "Arrêt Prévu"
        stylesheet = gris_moyen_label_stylesheet if settings_stat_store.data_type == "métrage"\
            else blue_16_label_stylesheet
        self.add_check_box_layout(index_data=0,
                                  stylecheet_label=stylesheet,
                                  text_label=texte,
                                  preset=settings_stat_store.display_setting[0])
        texte = "Equipe soir" if settings_stat_store.data_type == "métrage" else "Arrêt Imprévu"
        stylesheet = gris_fonce_label_stylesheet if settings_stat_store.data_type == "métrage"\
            else red_16_label_stylesheet
        self.add_check_box_layout(index_data=1,
                                  stylecheet_label=stylesheet,
                                  text_label=texte,
                                  preset=settings_stat_store.display_setting[1])
        texte = "Equipes cumulées" if settings_stat_store.data_type == "métrage" else "Arrêt cumulées"
        stylesheet = vert_fonce_label_stylesheet if settings_stat_store.data_type == "métrage"\
            else gris_fonce_label_stylesheet
        self.add_check_box_layout(index_data=2,
                                  stylecheet_label=stylesheet,
                                  text_label=texte,
                                  preset=settings_stat_store.display_setting[2])
        self.hbox.addStretch(1)
        self.setLayout(self.hbox)

    def add_check_box_layout(self, index_data, stylecheet_label, text_label, preset=False):
        check_box_hbox = QHBoxLayout()
        check_box_hbox.setSpacing(5)
        if preset:
            check_box = CheckboxButton(parent=self, is_check=False)
        else:
            check_box = CheckboxButton(parent=self)
        check_box.setFixedSize(self.CHART_SETTINGS_SIZE)
        check_box.ON_CLICK_SIGNAL.connect(lambda: settings_stat_store.on_select_checkbox_display(index_data))
        check_box_hbox.addWidget(check_box)
        label = QLabel(text_label)
        label.setStyleSheet(stylecheet_label)
        label.setFixedHeight(self.HEIGHT_LABEL)
        check_box_hbox.addWidget(label)
        self.hbox.addLayout(check_box_hbox)
