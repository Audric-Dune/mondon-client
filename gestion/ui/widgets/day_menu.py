# !/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import QHBoxLayout, QLabel

from commun.constants.colors import color_bleu_gris
from commun.constants.stylesheets import button_stylesheet, white_22_label_stylesheet
from commun.ui.public.mondon_widget import MondonWidget
from commun.ui.public.pixmap_button import PixmapButton
from commun.utils.timestamp import timestamp_at_day_ago, timestamp_to_date
from commun.utils.layout import clear_layout

from gestion.stores.settings_store import settings_store_gestion


class DayMenu(MondonWidget):
    PIXMAPBUTTON_SIZE = QSize(40, 40)
    BUTTON_HEIGHT = 40
    BUTTON_WIDTH = 100
    MINIMUN_WIDTH_LABEL = 350

    def __init__(self, parent):
        super(DayMenu, self).__init__(parent=parent)
        self.set_background_color(color_bleu_gris)
        self.master_hbox = QHBoxLayout()
        self.left_hbox = QHBoxLayout()
        self.center_hbox = QHBoxLayout()
        self.right_hbox = QHBoxLayout()
        self.bt_jour_plus = PixmapButton(parent=self)
        self.bt_jour_moins = PixmapButton(parent=self)
        self.bt_new_plan = PixmapButton(parent=self)
        self.label_date = QLabel()
        self.init_widget()

    def init_widget(self):
        self.init_button()
        self.setLayout(self.master_hbox)
        self.update_widget()

    def update_widget(self):
        self.left_hbox.addStretch(1)
        self.master_hbox.addLayout(self.left_hbox)

        self.center_hbox.addWidget(self.bt_jour_moins)
        self.center_hbox.addStretch(1)
        self.center_hbox.addWidget(self.label_date)
        self.label_date.setStyleSheet(white_22_label_stylesheet)
        self.center_hbox.addStretch(1)
        self.center_hbox.addWidget(self.bt_jour_plus)
        self.master_hbox.addLayout(self.center_hbox)

        self.right_hbox.addStretch(1)
        if settings_store_gestion.plan_prod_id:
            self.bt_new_plan.hide()
        else:
            self.right_hbox.addWidget(self.bt_new_plan)
            self.bt_new_plan.show()
        self.master_hbox.addLayout(self.right_hbox)
        self.update_label()


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

        # Bouton nouveau plan
        self.bt_new_plan.clicked.connect(self.create_new_plan)
        self.bt_new_plan.setStyleSheet(button_stylesheet)
        self.bt_new_plan.setFixedSize(self.PIXMAPBUTTON_SIZE)
        self.bt_new_plan.addImage("commun/assets/images/new_plan.png")

    def on_settings_gestion_changed(self):
        self.update_widget()

    def update_label(self):
        ts = timestamp_at_day_ago(settings_store_gestion.day_ago)
        date = timestamp_to_date(ts).capitalize()
        self.label_date.setMinimumWidth(self.MINIMUN_WIDTH_LABEL)
        self.label_date.setAlignment(Qt.AlignCenter)
        self.label_date.setText(date)

    @staticmethod
    def jour_moins():
        settings_store_gestion.set_day_ago(settings_store_gestion.day_ago + 1)

    @staticmethod
    def jour_plus():
        settings_store_gestion.set_day_ago(settings_store_gestion.day_ago - 1)

    @staticmethod
    def create_new_plan():
        settings_store_gestion.create_new_plan()
