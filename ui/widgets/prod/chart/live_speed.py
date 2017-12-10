# !/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.Qt import Qt
from PyQt5.QtWidgets import QVBoxLayout, QLabel

from constants.stylesheets import white_22_label_stylesheet
from constants.colors import color_bleu_gris
from stores.data_store_manager import data_store_manager
from ui.widgets.public.mondon_widget import MondonWidget


class LiveSpeed(MondonWidget):
    HEIGHT = 30

    def __init__(self, parent=None):
        super(LiveSpeed, self).__init__(parent=parent)
        self.set_background_color(color_bleu_gris)
        self.last_speed = 0
        self.update()
        self.speed_label = QLabel("0 m/min")
        self.init_widget()

    def init_widget(self):
        vbox = QVBoxLayout()
        vbox.setContentsMargins(5, 0, 5, 0)
        self.speed_label.setStyleSheet(white_22_label_stylesheet)
        self.speed_label.setFixedHeight(self.HEIGHT)
        vbox.addWidget(self.speed_label, alignment=Qt.AlignVCenter)
        self.setLayout(vbox)

    def update_widget(self):
        if not self.last_speed:
            self.last_speed = 0
        speed_text = "{speed} m/min".format(speed=self.last_speed)
        self.speed_label.setText(speed_text)

    def on_data_changed(self):
        self.last_speed = data_store_manager.get_most_recent_store().get_last_speed()
        self.update_widget()
