# !/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel

from stores.stat_store import stat_store
from stores.settings_stat_store import settings_stat_store
from constants import colors
from constants.stylesheets import black_12_label_stylesheet,\
    white_12_label_stylesheet,\
    gris_fonce_label_stylesheet,\
    gris_moyen_label_stylesheet,\
    vert_fonce_label_stylesheet
from ui.widgets.public.mondon_widget import MondonWidget
from ui.utils.data import affiche_entier
from lib.logger import logger
from ui.widgets.public.checkbox_button import CheckboxButton
from ui.utils.layout import clear_layout
from ui.utils.timestamp import timestamp_to_name_number_day_month, timestamp_to_day_month_little
from ui.widgets.stat.stat_chart_bar import StatChartBar


class ChartBar(MondonWidget):
    def __init__(self, parent=None):
        super(ChartBar, self).__init__(parent=parent)
        self.set_background_color(colors.color_bleu_gris)
        self.vbox = QVBoxLayout()
        self.chart_settings = ChartSettings(parent=self)
        self.content_chart = ContentChart(parent=self)
        self.chart_legend = ChartLegend(parent=self)
        self.init_widget()

    def init_widget(self):
        self.vbox.setContentsMargins(10, 0, 10, 0)
        self.vbox.setSpacing(0)
        self.vbox.addWidget(self.chart_settings)
        self.vbox.addWidget(self.content_chart)
        self.vbox.addWidget(self.chart_legend)
        self.setLayout(self.vbox)


class ContentChart(MondonWidget):
    BAR_CONTENT_SPACING = 0
    VALUE_LABEL_HEIGHT = 20

    def __init__(self, parent=None):
        super(ContentChart, self).__init__(parent=parent)
        self.background_color = colors.color_blanc
        self.color_data = [colors.color_gris_moyen, colors.color_gris_fonce, colors.color_vert_fonce]
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

    def on_settings_chart_changed(self):
        try:
            self.init_widget()
        except:
            logger.log("CHART_STAT", "Erreur de mise à jour lors du changement de settings du chart")

    def init_widget(self):
        self.hbox = clear_layout(self.hbox)
        self.bars = []
        self.hbox.setContentsMargins(10, 0, 10, 0)
        self.hbox.setSpacing(5)
        len_format = 0
        if settings_stat_store.format == "week":
            len_format = 5
        if settings_stat_store.format == "month":
            len_format = len(stat_store.data["total"])
        print(len_format)
        index = 0
        while index < len_format:
            hbox_multi_bar = QHBoxLayout()
            hbox_multi_bar.setContentsMargins(0, 0, 0, 0)
            hbox_multi_bar.setSpacing(0)
            index_data = 0
            while index_data < len(stat_store.data):
                if settings_stat_store.display_setting[index_data]:
                    moment = "matin" if index_data == 0 else ""
                    moment = "soir" if index_data == 1 else moment
                    moment = "total" if index_data == 2 else moment
                    value = stat_store.data[moment][index][1] if len(stat_store.data[moment]) > index else -1
                    hbox_multi_bar.addLayout(self.create_bar(value=value,
                                                             color=self.color_data[index_data]))
                index_data += 1
            self.hbox.addLayout(hbox_multi_bar)
            index += 1
        self.setLayout(self.hbox)
        self.update_widget()

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

    def on_data_stat_changed(self):
        self.update_widget()

    def init_widget(self):
        str_date = "NA"
        for values in stat_store.data["total"]:
            ts = values[0]
            if settings_stat_store.format == "week":
                str_date = timestamp_to_name_number_day_month(ts).capitalize()
            if settings_stat_store.format == "month":
                str_date = timestamp_to_day_month_little(ts)
            self.hbox.addWidget(self.create_label(str_date))

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

        self.add_check_box_layout(index_data=0,
                                  stylecheet_label=gris_moyen_label_stylesheet,
                                  text_label="Equipe matin",
                                  preset=settings_stat_store.display_setting[0])
        self.add_check_box_layout(index_data=1,
                                  stylecheet_label=gris_fonce_label_stylesheet,
                                  text_label="Equipe soir",
                                  preset=settings_stat_store.display_setting[1])
        self.add_check_box_layout(index_data=2,
                                  stylecheet_label=vert_fonce_label_stylesheet,
                                  text_label="Equipes cumulées",
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
