# !/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QHBoxLayout, QPushButton
from constants.colors import color_bleu_gris
from constants.stylesheets import button_menu_stylesheet, button_menu_stylesheet_unselected
from ui.widgets.public.mondon_widget import MondonWidget
from ui.widgets.public.pixmap_button import PixmapButton


class AppMenu(MondonWidget):
    MENU_CHANGED_SIGNAL = pyqtSignal(str)

    def __init__(self, parent=None):
        super(AppMenu, self).__init__(parent=parent)
        self.set_background_color(color_bleu_gris)
        self.menu_selected = None
        self.hbox = QHBoxLayout()
        self.list_bt = {}
        self.init_widget()
        self.set_bt_stylesheet()

    def init_widget(self):
        self.hbox.setContentsMargins(0, 0, 0, 0)
        self.hbox.setSpacing(0)

        bt_acceuil = PixmapButton("Production")
        self.list_bt["prod"] = bt_acceuil
        bt_acceuil.clicked.connect(lambda: self.on_click("prod"))
        self.hbox.addWidget(bt_acceuil)

        bt_stat = QPushButton("Statistique")
        self.list_bt["chart_stat"] = bt_stat
        bt_stat.clicked.connect(lambda: self.on_click("chart_stat"))
        self.hbox.addWidget(bt_stat)

        self.hbox.addStretch(1)
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
