# !/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QHBoxLayout, QLabel
from PyQt5.QtCore import QSize

from ui.utils.timestamp import timestamp_at_week_ago
from constants.colors import color_bleu_gris
from constants.stylesheets import button_stylesheet
from stores.stat_store import stat_store
from ui.widgets.public.mondon_widget import MondonWidget
from ui.widgets.public.pixmap_button import PixmapButton


class ChartBarMenu(MondonWidget):
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
        self.hbox.addWidget(self.bt_moins)
        self.hbox.addWidget(self.bt_plus)
        self.setLayout(self.hbox)
        self.update_button()

    def on_settings_stat_changed(self):
        self.update_button()
        self.update_label()

    def update_label(self):
        pass

    def update_button(self):
        self.bt_plus.setEnabled(stat_store.week_ago > 0)
        self.bt_moins.setDisabled(timestamp_at_week_ago(stat_store.week_ago) == 1508709600)

    def init_button(self):
        # Bouton semaine plus
        self.bt_plus.clicked.connect(self.semaine_plus)
        self.bt_plus.setStyleSheet(button_stylesheet)
        self.bt_plus.setFixedSize(self.PIXMAPBUTTON_SIZE)
        self.bt_plus.addImage("assets/images/fleche_suivant.png")

        # Bouton semaine moins
        self.bt_moins.clicked.connect(self.semaine_moins)
        self.bt_moins.setStyleSheet(button_stylesheet)
        self.bt_moins.setFixedSize(self.PIXMAPBUTTON_SIZE)
        self.bt_moins.addImage("assets/images/fleche_precedent.png")

    @staticmethod
    def semaine_moins():
        stat_store.set_week_ago(stat_store.week_ago + 1)

    @staticmethod
    def semaine_plus():
        stat_store.set_week_ago(stat_store.week_ago - 1)
