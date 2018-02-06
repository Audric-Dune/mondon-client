# !/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QHBoxLayout, QPushButton, QLabel

from commun.ui.public.pixmap_button import PixmapButton
from commun.constants.colors import color_bleu_gris
from commun.constants.stylesheets import button_menu_stylesheet,\
    button_menu_stylesheet_unselected,\
    button_green_stylesheet,\
    white_16_label_stylesheet
from commun.ui.public.mondon_widget import MondonWidget

from production.stores.user_store import user_store


class AppMenu(MondonWidget):
    WIDTH_BT = 150
    MENU_CHANGED_SIGNAL = pyqtSignal(str)

    def __init__(self, parent=None):
        super(AppMenu, self).__init__(parent=parent)
        self.set_background_color(color_bleu_gris)
        user_store.ON_USER_CHANGED_SIGNAL.connect(self.update_widget)
        self.menu_selected = None
        self.hbox = QHBoxLayout()
        self.list_bt = {}
        self.bt_stat = QPushButton("Statistique")
        self.bt_rapport = QPushButton("Rapport")
        self.bt_team_gestion = QPushButton("Gestion équipes")
        self.label_user = QLabel()
        self.init_widget()
        self.set_bt_stylesheet()
        self.update_widget()

    def on_user_changed(self):
        self.update_widget()

    def init_widget(self):
        self.hbox.setContentsMargins(0, 0, 0, 0)
        self.hbox.setSpacing(0)

        bt_acceuil = PixmapButton("Production")
        bt_acceuil.setFixedWidth(self.WIDTH_BT)
        self.list_bt["prod"] = bt_acceuil
        bt_acceuil.clicked.connect(lambda: self.on_click("prod"))
        self.hbox.addWidget(bt_acceuil)

        self.bt_stat.setFixedWidth(self.WIDTH_BT)
        self.bt_stat.hide()
        self.list_bt["chart_stat"] = self.bt_stat
        self.bt_stat.clicked.connect(lambda: self.on_click("chart_stat"))
        self.hbox.addWidget(self.bt_stat)

        self.bt_rapport.setFixedWidth(self.WIDTH_BT)
        self.bt_rapport.hide()
        self.list_bt["rapport"] = self.bt_rapport
        self.bt_rapport.clicked.connect(lambda: self.on_click("rapport"))
        self.hbox.addWidget(self.bt_rapport)

        self.bt_team_gestion.setFixedWidth(self.WIDTH_BT)
        self.bt_team_gestion.hide()
        self.list_bt["team_gestion"] = self.bt_team_gestion
        self.bt_team_gestion.clicked.connect(lambda: self.on_click("team_gestion"))
        self.hbox.addWidget(self.bt_team_gestion)

        self.hbox.addStretch(1)
        self.label_user.setStyleSheet(white_16_label_stylesheet)
        self.hbox.addWidget(self.label_user)
        bt_user = PixmapButton(parent=self)
        bt_user.addImage("commun/assets/images/user_icon.png")
        bt_user.setStyleSheet(button_green_stylesheet)
        bt_user.setFixedSize(self.height(), self.height())
        bt_user.clicked.connect(self.on_click_user)
        self.hbox.addWidget(bt_user)
        self.setLayout(self.hbox)

    def update_widget(self):
        if user_store.user_level == 0:
            user = "Opérateur"
            self.bt_rapport.hide()
            self.bt_stat.hide()
            self.bt_team_gestion.hide()
        else:
            user = "Superviseur"
            self.bt_rapport.show()
            self.bt_stat.show()
            self.bt_team_gestion.show()
        self.label_user.setText(user)

    def on_click(self, menu_selected):
        self.menu_selected = menu_selected
        self.set_bt_stylesheet()
        self.MENU_CHANGED_SIGNAL.emit(str(menu_selected))

    @staticmethod
    def on_click_user():
        user_store.create_popup_user()

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
