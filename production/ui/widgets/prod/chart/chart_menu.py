# !/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import QPushButton, QHBoxLayout, QLabel

from commun.constants.colors import color_bleu_gris
from commun.constants.stylesheets import button_stylesheet, white_22_label_stylesheet, button_little_stylesheet
from commun.ui.public.mondon_widget import MondonWidget
from commun.ui.public.pixmap_button import PixmapButton
from commun.utils.timestamp import timestamp_at_day_ago, timestamp_to_date

from production.ui.application import app
from production.ui.widgets.prod.chart.live_speed import LiveSpeed
from production.stores.settings_store import settings_store


class ChartMenu(MondonWidget):
    PIXMAPBUTTON_SIZE = QSize(40, 40)
    BUTTON_HEIGHT = 40
    BUTTON_WIDTH = 100
    MINIMUN_WIDTH_LABEL = 350

    def __init__(self, parent):
        super(ChartMenu, self).__init__(parent=parent)
        self.set_background_color(color_bleu_gris)
        self.bt_jour_plus = PixmapButton(parent=self)
        self.bt_jour_moins = PixmapButton(parent=self)
        self.bt_zoom_plus = PixmapButton(parent=self)
        self.bt_zoom_moins = PixmapButton(parent=self)
        self.bt_live = QPushButton("En direct")
        self.label_date = QLabel()
        self.live_speed = LiveSpeed(self)
        self.init_widget()
        self.update_label()
        self.update_button()

    def init_widget(self):
        self.init_button()
        self.update_label()
        master_hbox = QHBoxLayout()

        left_hbox = QHBoxLayout()
        left_hbox.addWidget(self.bt_live)
        self.live_speed.mouseDoubleClickEvent = self.create_window_live_speed
        left_hbox.addWidget(self.live_speed)
        left_hbox.addStretch(1)
        master_hbox.addLayout(left_hbox)

        center_hbox = QHBoxLayout()
        center_hbox.addWidget(self.bt_jour_moins)
        center_hbox.addStretch(1)
        center_hbox.addWidget(self.label_date)
        self.label_date.setStyleSheet(white_22_label_stylesheet)
        center_hbox.addStretch(1)
        center_hbox.addWidget(self.bt_jour_plus)
        master_hbox.addLayout(center_hbox)

        right_hbox = QHBoxLayout()
        right_hbox.addStretch(1)
        right_hbox.addWidget(self.bt_zoom_moins)
        right_hbox.addWidget(self.bt_zoom_plus)
        master_hbox.addLayout(right_hbox)

        self.setLayout(master_hbox)

    def init_button(self):
        # Bouton jour plus
        self.bt_jour_plus.clicked.connect(self.jour_plus)
        self.bt_jour_plus.setStyleSheet(button_stylesheet)
        self.bt_jour_plus.setFixedSize(self.PIXMAPBUTTON_SIZE)
        self.bt_jour_plus.addImage("commun/assets/images/fleche_suivant.png")

        # Bouton jour moins
        self.bt_jour_moins.clicked.connect(self.jour_moins)
        self.bt_jour_moins.setStyleSheet(button_stylesheet)
        self.bt_jour_moins.setFixedSize(self.PIXMAPBUTTON_SIZE)
        self.bt_jour_moins.addImage("commun/assets/images/fleche_precedent.png")

        # Bouton zoom plus
        self.bt_zoom_plus.clicked.connect(self.zoom_plus)
        self.bt_zoom_plus.setStyleSheet(button_stylesheet)
        self.bt_zoom_plus.setFixedSize(self.PIXMAPBUTTON_SIZE)
        self.bt_zoom_plus.addImage("commun/assets/images/zoom_plus.png")

        # Bouton zoom moins
        self.bt_zoom_moins.clicked.connect(self.zoom_moins)
        self.bt_zoom_moins.setStyleSheet(button_stylesheet)
        self.bt_zoom_moins.setFixedSize(self.PIXMAPBUTTON_SIZE)
        self.bt_zoom_moins.addImage("commun/assets/images/zoom_moins.png")

        # Bouton live
        self.bt_live.clicked.connect(self.live)
        self.bt_live.setFixedSize(self.BUTTON_WIDTH, self.BUTTON_HEIGHT)
        self.bt_live.setStyleSheet(button_little_stylesheet)

    def on_settings_changed(self, prev_live, prev_day_ago, prev_zoom):
        self.update_button()
        self.update_label()

    def update_button(self):
        self.bt_live.hide() if settings_store.day_ago == 0 else self.bt_live.show()
        self.live_speed.show() if settings_store.day_ago == 0 else self.live_speed.hide()
        self.bt_jour_plus.setEnabled(settings_store.day_ago > 0)
        self.bt_zoom_moins.setEnabled(settings_store.zoom > 1)
        self.bt_zoom_plus.setEnabled(32 > settings_store.zoom)

    def update_label(self):
        ts = timestamp_at_day_ago(settings_store.day_ago)
        date = timestamp_to_date(ts).capitalize()
        self.label_date.setMinimumWidth(self.MINIMUN_WIDTH_LABEL)
        self.label_date.setAlignment(Qt.AlignCenter)
        self.label_date.setText(date)

    @staticmethod
    def zoom_moins():
        new_zoom = max(1, int(settings_store.zoom/2))
        settings_store.set_zoom(new_zoom)

    @staticmethod
    def zoom_plus():
        settings_store.set_zoom(settings_store.zoom * 2)

    @staticmethod
    def jour_moins():
        settings_store.set_day_ago(settings_store.day_ago + 1)

    @staticmethod
    def jour_plus():
        settings_store.set_day_ago(settings_store.day_ago - 1)

    @staticmethod
    def live():
        settings_store.set_day_ago(0)

    @staticmethod
    def create_window_live_speed(event):
        app.create_tracker_window()
