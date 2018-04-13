# !/usr/bin/env python
# -*- coding: utf-8 -*-


from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout
from PyQt5.QtCore import Qt

from commun.utils.layout import clear_layout

from gestion.ui.widgets.plan_prod_creator import PlanProdCreator
from gestion.ui.widgets.day_menu import DayMenu
from gestion.stores.settings_store import settings_store_gestion
from gestion.stores.plan_prod_store import plan_prod_store


class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__(parent=None, flags=Qt.Window)
        self.central_widget = QWidget(parent=self)
        self.day_menu = DayMenu(parent=self)
        self.vbox = QVBoxLayout()
        settings_store_gestion.SETTINGS_CHANGED_SIGNAL.connect(self.update_widget)
        self.init_widget()

    def init_widget(self):
        self.vbox.addWidget(self.day_menu)
        self.central_widget.setLayout(self.vbox)
        self.setCentralWidget(self.central_widget)

    def update_widget(self):
        if settings_store_gestion.plan_prod:
            plan_prod_creator = PlanProdCreator(parent=self, plan_prod=settings_store_gestion.plan_prod)
            self.vbox.addWidget(plan_prod_creator)
