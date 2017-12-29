# !/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtCore import Qt, QSize, pyqtSignal
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel

from stores.stat_store import stat_store
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

    def update_widget(self):
        self.content_chart.update_widget()


class ContentChart(MondonWidget):
    BAR_CONTENT_SPACING = 0
    VALUE_LABEL_HEIGHT = 20

    def __init__(self, parent=None):
        super(ContentChart, self).__init__(parent=parent)
        self.background_color = colors.color_blanc
        self.on_settings_stat_changed()
        self.color_data = [colors.color_gris_moyen, colors.color_gris_fonce, colors.color_vert_fonce]
        self.format = stat_store.format
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

    def on_size_main_window_changed(self):
        self.update_widget()

    def init_widget(self):
        self.hbox = clear_layout(self.hbox)
        self.bars = []
        self.hbox.setContentsMargins(10, 0, 10, 0)
        self.hbox.setSpacing(5)
        len_format = 0
        if self.format == "week":
            len_format = 5
        if self.format == "month":
            len_format = len(stat_store.data[0]["values"])
        index = 0
        while index < len_format:
            index_data = 0
            hbox_multi_bar = QHBoxLayout()
            hbox_multi_bar.setContentsMargins(0, 0, 0, 0)
            hbox_multi_bar.setSpacing(0)
            for data in stat_store.data:
                if stat_store.displays[index_data]:
                    value = data["values"][index] if len(data["values"]) > index else "NA"
                    hbox_multi_bar.addLayout(self.create_bar(value=value,
                                                             color=self.color_data[index_data]))
                index_data += 1
            self.hbox.addLayout(hbox_multi_bar)
            index += 1
        self.setLayout(self.hbox)
        self.update_widget()

    def update_widget(self):
        if self.bars:
            for bar in self.bars:
                max_size = self.height() - 2 * (self.VALUE_LABEL_HEIGHT + self.BAR_CONTENT_SPACING)
                if stat_store.data[-1]["values"]:
                    height = (bar[1]*max_size)/max(stat_store.data[-1]["values"]) if max(stat_store.data[-1]["values"]) > 0 else 0
                else:
                    height = 1
                bar[0].setFixedHeight(round(height))

    def create_bar(self, value, color):
        vbox = QVBoxLayout()
        vbox.setSpacing(self.BAR_CONTENT_SPACING)
        vbox.addStretch(1)

        # label_value = QLabel(affiche_entier(s=str(value)))
        # label_value.setFixedHeight(self.VALUE_LABEL_HEIGHT)
        # label_value.setAlignment(Qt.AlignCenter)
        # label_value.setStyleSheet(black_12_label_stylesheet)
        # vbox.addWidget(label_value)

        bar = MondonWidget(parent=self)
        bar.setMinimumSize(1, 1)
        self.bars.append((bar, value))
        bar.set_background_color(color)
        vbox.addWidget(bar)

        return vbox


class ChartLegend(MondonWidget):
    LEGEND_LABEL_HEIGHT = 20

    def __init__(self, parent=None):
        super(ChartLegend, self).__init__(parent=parent)
        self.setFixedHeight(40)
        self.background_color = colors.color_bleu_gris
        self.format = stat_store.format
        self.hbox = QHBoxLayout(self)
        self.hbox.setSpacing(0)
        self.init_widget()

    def on_settings_stat_changed(self):
        self.update_widget()

    def init_widget(self):
        str_date = "NA"
        for ts in stat_store.data[0]["ts"]:
            if self.format == "week":
                str_date = timestamp_to_name_number_day_month(ts)
            if self.format == "month":
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
                                  preset=stat_store.displays[0])
        self.add_check_box_layout(index_data=1,
                                  stylecheet_label=gris_fonce_label_stylesheet,
                                  text_label="Equipe soir",
                                  preset=stat_store.displays[1])
        self.add_check_box_layout(index_data=2,
                                  stylecheet_label=vert_fonce_label_stylesheet,
                                  text_label="Equipes cumulées",
                                  preset=stat_store.displays[2])

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
        check_box.ON_CLICK_SIGNAL.connect(lambda: stat_store.on_select_checkbox_display(index_data))
        check_box_hbox.addWidget(check_box)
        label = QLabel(text_label)
        label.setStyleSheet(stylecheet_label)
        label.setFixedHeight(self.HEIGHT_LABEL)
        check_box_hbox.addWidget(label)
        self.hbox.addLayout(check_box_hbox)
