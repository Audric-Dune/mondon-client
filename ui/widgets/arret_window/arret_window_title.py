# !/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import timedelta

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QLabel, QHBoxLayout

from constants.colors import color_bleu_gris
from constants.stylesheets import white_20_label_stylesheet, white_24_label_stylesheet
from ui.utils.drawing import draw_rectangle
from ui.utils.timestamp import timestamp_to_hour_little, timestamp_to_date_little
from ui.widgets.public.mondon_widget import MondonWidget


class ArretWindowTitle(MondonWidget):
    def __init__(self, arret, parent):
        super(ArretWindowTitle, self).__init__(parent=parent)
        self.arret = arret
        self.label_date = QLabel()
        self.label_hour = QLabel()
        self.label_duration = QLabel()
        self.update_widget()
        self.init_widget()

    def draw_fond(self, p):
        draw_rectangle(p, 0, 0, self.width(), self.height(), color_bleu_gris)

    def on_data_changed(self):
        self.update_widget()

    def paintEvent(self, event):
        p = QPainter()
        p.begin(self)
        self.draw(p)
        p.end()

    def init_widget(self):
        hbox = QHBoxLayout()
        self.label_date.setStyleSheet(white_20_label_stylesheet)
        self.label_date.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        hbox.addWidget(self.label_date)
        self.label_duration.setStyleSheet(white_24_label_stylesheet)
        self.label_duration.setAlignment(Qt.AlignCenter)
        hbox.addWidget(self.label_duration)
        self.label_hour.setStyleSheet(white_20_label_stylesheet)
        self.label_hour.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        hbox.addWidget(self.label_hour)
        self.setLayout(hbox)

    def update_widget(self):
        self.label_date.setText(str(timestamp_to_date_little(self.arret.start)))
        self.label_hour.setText(str(timestamp_to_hour_little(self.arret.start)))
        self.label_duration.setText(str(timedelta(seconds=round(self.arret.end - self.arret.start))))

    def draw(self, p):
        self.draw_fond(p)
