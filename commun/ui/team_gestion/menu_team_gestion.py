# !/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import QHBoxLayout, QLabel

from commun.constants.colors import color_bleu_gris
from commun.constants.param import LIMIT_JOURS_GESTION_EQUIPE
from commun.constants.stylesheets import button_stylesheet, white_22_label_stylesheet, green_maj_label_stylesheet
from commun.ui.public.mondon_widget import MondonWidget
from commun.ui.public.pixmap_button import PixmapButton
from commun.utils.timestamp import timestamp_at_week_ago

from production.stores.settings_team_gestion_store import settings_team_gestion_store


class TeamGestionMenu(MondonWidget):
    MINIMUN_WIDTH_LABEL = 200
    PIXMAPBUTTON_SIZE = QSize(30, 30)

    def __init__(self, parent=None):
        super(TeamGestionMenu, self).__init__(parent=parent)
        self.background_color = color_bleu_gris
        self.hbox = QHBoxLayout(self)
        self.bt_plus = PixmapButton(parent=self)
        self.bt_moins = PixmapButton(parent=self)
        self.label_date = QLabel()
        self.label_type_stat = QLabel("Gestion des équipes")
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

    def on_settings_team_gestion_changed(self):
        self.update_button()
        self.update_label()

    def update_label(self):
        self.label_date.setText(settings_team_gestion_store.time_stat)

    def update_button(self):
        disabled_bt_moins = False
        disabled_bt_plus = False
        if settings_team_gestion_store.week_ago >= LIMIT_JOURS_GESTION_EQUIPE:
            disabled_bt_plus = True
        limit_week_stat = 1508709600
        if timestamp_at_week_ago(settings_team_gestion_store.week_ago) == limit_week_stat:
            disabled_bt_moins = True
        self.bt_moins.setDisabled(disabled_bt_moins)
        self.bt_plus.setDisabled(disabled_bt_plus)

    def init_button(self):
        # Bouton time plus
        self.bt_plus.clicked.connect(self.time_more)
        self.bt_plus.setStyleSheet(button_stylesheet)
        self.bt_plus.setFixedSize(self.PIXMAPBUTTON_SIZE)
        self.bt_plus.addImage("commun/assets/images/fleche_suivant.png")

        # Bouton time moins
        self.bt_moins.clicked.connect(self.time_less)
        self.bt_moins.setStyleSheet(button_stylesheet)
        self.bt_moins.setFixedSize(self.PIXMAPBUTTON_SIZE)
        self.bt_moins.addImage("commun/assets/images/fleche_precedent.png")

    @staticmethod
    def time_more():
        settings_team_gestion_store.update_week_ago(-1)

    @staticmethod
    def time_less():
        settings_team_gestion_store.update_week_ago(1)
