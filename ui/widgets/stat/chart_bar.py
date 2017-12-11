# !/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel

# from stores.stat_store import stat_store
from constants import colors
from constants.stylesheets import black_12_label_stylesheet, white_label_stylesheet
from ui.widgets.public.mondon_widget import MondonWidget
from ui.utils.data import affiche_entier


class ChartBar(MondonWidget):
    def __init__(self, parent=None):
        super(ChartBar, self).__init__(parent=parent)
        self.set_background_color(colors.color_bleu_gris)
        self.vbox = QVBoxLayout()
        self.content_chart = ContentChart(parent=self)
        self.chart_legend = ChartLegend(parent=self)
        self.init_widget()

    def init_widget(self):
        self.vbox.setContentsMargins(10, 10, 10, 0)
        self.vbox.setSpacing(0)
        self.vbox.addWidget(self.content_chart)
        self.vbox.addWidget(self.chart_legend)
        self.setLayout(self.vbox)

    def update_widget(self):
        self.content_chart.update_widget()


class ContentChart(MondonWidget):
    LEGEND_LABEL_HEIGHT = 30
    BAR_CONTENT_SPACING = 0

    def __init__(self, parent=None):
        super(ContentChart, self).__init__(parent=parent)
        self.background_color = colors.color_blanc
        self.data_1 = [67040, 110000, 98020, 78240, 12456]
        self.color_data_1 = colors.color_vert_fonce
        self.data_2 = [30000, 55607, 45000, 35000, 7097]
        self.color_data_2 = colors.color_gris_moyen
        self.data_3 = [37040, 45000, 3200, 50000, 5000]
        self.color_data_3 = colors.color_gris_fonce
        self.format = "semaine"
        self.bars = []
        self.hbox = QHBoxLayout(self)
        self.init_widget()

    def on_data_changed(self):
        self.update_widget()

    def init_widget(self):
        self.hbox.setContentsMargins(20, 0, 20, 0)
        self.hbox.setSpacing(20)
        index = 0
        for data in self.data_1:
            hbox_multi_bar = QHBoxLayout()
            hbox_multi_bar.setContentsMargins(0, 0, 0, 0)
            hbox_multi_bar.setSpacing(0)
            if self.data_2:
                hbox_multi_bar.addLayout(self.create_bar(value=self.data_2[index], color=self.color_data_2))
            if self.data_3:
                hbox_multi_bar.addLayout(self.create_bar(value=self.data_3[index], color=self.color_data_3))
            hbox_multi_bar.addLayout(self.create_bar(value=data, color=self.color_data_1))
            self.hbox.addLayout(hbox_multi_bar)
            index += 1
        self.setLayout(self.hbox)

    def update_widget(self):
        for bar in self.bars:
            max_size = self.height()-self.LEGEND_LABEL_HEIGHT-self.BAR_CONTENT_SPACING
            height = (bar[1]*max_size)/max(self.data_1)
            bar[0].setFixedHeight(height)

    def create_bar(self, value, color):
        vbox = QVBoxLayout()
        vbox.setSpacing(self.BAR_CONTENT_SPACING)
        vbox.addStretch(1)

        label_value = QLabel(affiche_entier(s=str(value)))
        label_value.setFixedHeight(self.LEGEND_LABEL_HEIGHT)
        label_value.setAlignment(Qt.AlignCenter)
        label_value.setStyleSheet(black_12_label_stylesheet)
        vbox.addWidget(label_value)

        bar = MondonWidget(parent=self)
        self.bars.append((bar, value))
        bar.set_background_color(color)
        vbox.addWidget(bar)

        return vbox


class ChartLegend(MondonWidget):
    LEGEND_LABEL_HEIGHT = 20
    SEMAINE = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi"]

    def __init__(self, parent=None):
        super(ChartLegend, self).__init__(parent=parent)
        self.background_color = colors.color_bleu_gris
        self.format = "semaine"
        self.hbox = QHBoxLayout(self)
        self.init_widget()

    def init_widget(self):
        if self.format == "semaine":
            for text in self.SEMAINE:
                self.hbox.addWidget(self.create_label(text))

    def create_label(self, text):
        label = QLabel(text)
        label.setFixedHeight(self.LEGEND_LABEL_HEIGHT)
        label.setAlignment(Qt.AlignCenter | Qt.AlignBottom)
        label.setStyleSheet(white_label_stylesheet)
        return label
