# !/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QHBoxLayout, QPushButton, QLabel
from constants.colors import color_bleu_gris
from constants.stylesheets import button_menu_stylesheet, button_menu_stylesheet_unselected, button_green_stylesheet, white_16_label_stylesheet
from stores.user_store import user_store
from ui.widgets.public.mondon_widget import MondonWidget
from ui.widgets.public.pixmap_button import PixmapButton


class AppMenu(MondonWidget):
    WIDTH_BT = 150
    MENU_CHANGED_SIGNAL = pyqtSignal(str)

    def __init__(self, parent=None):
        super(AppMenu, self).__init__(parent=parent)
        self.set_background_color(color_bleu_gris)
        self.menu_selected = None
        self.hbox = QHBoxLayout()
        self.list_bt = {}
        self.label_user = QLabel("Opérateur")
        self.init_widget()
        self.set_bt_stylesheet()

    def init_widget(self):
        self.hbox.setContentsMargins(0, 0, 0, 0)
        self.hbox.setSpacing(0)

        bt_acceuil = PixmapButton("Production")
        bt_acceuil.setFixedWidth(self.WIDTH_BT)
        self.list_bt["prod"] = bt_acceuil
        bt_acceuil.clicked.connect(lambda: self.on_click("prod"))
        self.hbox.addWidget(bt_acceuil)

        if user_store.level_user > 0:
            bt_stat = QPushButton("Statistique")
            bt_stat.setFixedWidth(self.WIDTH_BT)
            self.list_bt["chart_stat"] = bt_stat
            bt_stat.clicked.connect(lambda: self.on_click("chart_stat"))
            self.hbox.addWidget(bt_stat)

            bt_rapport = QPushButton("Rapport")
            bt_rapport.setFixedWidth(self.WIDTH_BT)
            self.list_bt["rapport"] = bt_rapport
            bt_rapport.clicked.connect(lambda: self.on_click("rapport"))
            self.hbox.addWidget(bt_rapport)

            bt_team_gestion = QPushButton("Gestion équipes")
            bt_team_gestion.setFixedWidth(self.WIDTH_BT)
            self.list_bt["team_gestion"] = bt_team_gestion
            bt_team_gestion.clicked.connect(lambda: self.on_click("team_gestion"))
            self.hbox.addWidget(bt_team_gestion)

        self.hbox.addStretch(1)
        self.label_user.setStyleSheet(white_16_label_stylesheet)
        self.hbox.addWidget(self.label_user)
        bt_user = PixmapButton(parent=self)
        bt_user.addImage("assets/images/user_icon.png")
        bt_user.setStyleSheet(button_green_stylesheet)
        bt_user.setFixedSize(self.height(), self.height())
        self.hbox.addWidget(bt_user)
        self.setLayout(self.hbox)

    def on_click(self, menu_selected):
        self.menu_selected = menu_selected
        self.set_bt_stylesheet()
        self.MENU_CHANGED_SIGNAL.emit(str(menu_selected))

    def set_bt_stylesheet(self):
        if not self.menu_selected:
            self.menu_selected = "prod"
        for key in self.list_bt.keys():
            if key == self.menu_selected:
                stylesheet = button_menu_stylesheet
            else:
                stylesheet = button_menu_stylesheet_unselected
            self.list_bt[key].setStyleSheet(stylesheet)
            self.list_bt[key].setFixedHeight(self.height())
