# !/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QHBoxLayout, QLabel
from PyQt5.QtCore import QSize, Qt

from ui.utils.timestamp import timestamp_at_week_ago, timestamp_at_month_ago
from constants.colors import color_bleu_gris
from constants.stylesheets import button_stylesheet, white_22_label_stylesheet, green_maj_label_stylesheet
from stores.settings_stat_store import settings_stat_store
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
        self.label_date = QLabel()
        self.label_type_stat = QLabel()
        self.init_button()
        self.init_widget()
        self.update_button()
        self.update_label()

    def init_widget(self):
        self.hbox.setSpacing(20)
        left_hbox = QHBoxLayout()
        left_hbox.addStretch(1)
        self.hbox.addLayout(left_hbox)

        center_hbox = QHBoxLayout()
        center_hbox.addStretch(4)
        center_hbox.addWidget(self.bt_moins)
        center_hbox.addStretch(1)
        self.label_date.setStyleSheet(white_22_label_stylesheet)
        self.label_date.setMinimumWidth(self.MINIMUN_WIDTH_LABEL)
        self.label_date.setAlignment(Qt.AlignCenter)
        center_hbox.addWidget(self.label_date)
        center_hbox.addStretch(1)
        center_hbox.addWidget(self.bt_plus)
        center_hbox.addStretch(4)
        self.hbox.addLayout(center_hbox)

        right_hbox = QHBoxLayout()
        right_hbox.addStretch(1)
        self.label_type_stat.setStyleSheet(green_maj_label_stylesheet)
        right_hbox.addWidget(self.label_type_stat)
        self.hbox.addLayout(right_hbox)
        self.setLayout(self.hbox)

    def on_settings_stat_changed(self):
        self.update_button()
        self.update_label()

    def update_label(self):
        self.label_date.setText(settings_stat_store.time_stat)
        self.label_type_stat.setText(settings_stat_store.data_type.upper())

    def update_button(self):
        self.bt_plus.setEnabled(settings_stat_store.week_ago > 0 or settings_stat_store.month_ago > 0)
        disabled_bt_moins = False
        limit_week_stat = 1508709600 if settings_stat_store.data_type == "métrage" else 1514761200
        if timestamp_at_week_ago(settings_stat_store.week_ago) == limit_week_stat and settings_stat_store.week_ago >= 0:
            disabled_bt_moins = True
        limit_month_stat = 1509490800 if settings_stat_store.data_type == "métrage" else 1514761200
        if timestamp_at_month_ago(settings_stat_store.month_ago) == limit_month_stat \
                and settings_stat_store.month_ago >= 0:
            disabled_bt_moins = True
        self.bt_moins.setDisabled(disabled_bt_moins)

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
        settings_stat_store.update_time_ago(-1)

    @staticmethod
    def time_less():
        settings_stat_store.update_time_ago(1)
