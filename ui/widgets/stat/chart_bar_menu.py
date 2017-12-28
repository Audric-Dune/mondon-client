# !/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QHBoxLayout, QLabel
from PyQt5.QtCore import QSize, Qt

from ui.utils.timestamp import timestamp_at_week_ago, timestamp_at_month_ago
from constants.colors import color_bleu_gris
from constants.stylesheets import button_stylesheet, white_22_label_stylesheet
from stores.stat_store import stat_store
from ui.widgets.public.mondon_widget import MondonWidget
from ui.widgets.public.pixmap_button import PixmapButton


class ChartBarMenu(MondonWidget):
    MINIMUN_WIDTH_LABEL = 200
    PIXMAPBUTTON_SIZE = QSize(30, 30)

    def __init__(self, parent=None):
        super(ChartBarMenu, self).__init__(parent=parent)
        self.background_color = color_bleu_gris
        self.hbox = QHBoxLayout(self)
        self.bt_plus = PixmapButton(parent=self)
        self.bt_moins = PixmapButton(parent=self)
        self.label = QLabel()
        self.init_button()
        self.init_widget()

    def init_widget(self):
        self.hbox.setSpacing(20)
        self.hbox.addStretch(1)
        center_hbox = QHBoxLayout()
        center_hbox.addWidget(self.bt_moins)
        center_hbox.addStretch(1)
        self.label.setStyleSheet(white_22_label_stylesheet)
        self.label.setMinimumWidth(self.MINIMUN_WIDTH_LABEL)
        self.label.setAlignment(Qt.AlignCenter)
        center_hbox.addWidget(self.label)
        center_hbox.addStretch(1)
        center_hbox.addWidget(self.bt_plus)
        self.hbox.addLayout(center_hbox)
        self.hbox.addStretch(1)
        self.setLayout(self.hbox)
        self.update_button()
        self.update_label()

    def on_settings_stat_changed(self):
        self.update_button()
        self.update_label()

    def update_label(self):
        self.label.setText(stat_store.time_stat)

    def update_button(self):
        self.bt_plus.setEnabled(stat_store.week_ago > 0 or stat_store.month_ago > 0)
        self.bt_moins.setDisabled(timestamp_at_week_ago(stat_store.week_ago) == 1508709600)
        self.bt_moins.setDisabled(timestamp_at_month_ago(stat_store.month_ago) == 1509490800)

    def init_button(self):
        # Bouton time plus
        self.bt_plus.clicked.connect(self.time_more)
        self.bt_plus.setStyleSheet(button_stylesheet)
        self.bt_plus.setFixedSize(self.PIXMAPBUTTON_SIZE)
        self.bt_plus.addImage("assets/images/fleche_suivant.png")

        # Bouton time moins
        self.bt_moins.clicked.connect(self.time_less)
        self.bt_moins.setStyleSheet(button_stylesheet)
        self.bt_moins.setFixedSize(self.PIXMAPBUTTON_SIZE)
        self.bt_moins.addImage("assets/images/fleche_precedent.png")

    @staticmethod
    def time_more():
        stat_store.update_time_ago(-1)

    @staticmethod
    def time_less():
        stat_store.update_time_ago(1)
