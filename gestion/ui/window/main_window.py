# !/usr/bin/env python
# -*- coding: utf-8 -*-


from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout

from commun.constants.dimensions import chart_menu_height

from gestion.stores.plan_prod_store import plan_prod_store
from gestion.stores.settings_store import settings_store_gestion
from gestion.ui.main_ui.day_menu import DayMenu
from gestion.ui.main_ui.plan_prod_creator import PlanProdCreator
from gestion.ui.main_ui.gant_manager import GantManager
from gestion.ui.main_ui.tab_prod_bobines import TabProdBobine
from gestion.ui.main_ui.toolbar_gantt import ToolbarGantt


class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__(parent=None, flags=Qt.Window)
        self.central_widget = QWidget(parent=self)
        settings_store_gestion.CREATE_PLAN_PROD_WINDOW.connect(self.create_plan_prod_creator_window)
        settings_store_gestion.CREATE_EVENT_CONFIG_WINDOW.connect(self.create_event_config_window)
        settings_store_gestion.CREATE_EVENT_CONFIG_EDIT_WINDOW.connect(self.create_event_config_edit_window)
        plan_prod_store.get_plan_prod_from_database()
        self.setMinimumWidth(800)
        self.gant_manager = GantManager()
        self.tab_prod_bobines = TabProdBobine(parent=self)
        self.toolbar_gantt = ToolbarGantt(parent=self)
        self.event_windows = []
        self.plan_prod_window = None
        self.init_widget()

    def init_widget(self):
        vbox = QVBoxLayout()
        day_menu = DayMenu(parent=self)
        day_menu.setFixedHeight(chart_menu_height)
        vbox.addWidget(day_menu)
        vbox.addWidget(self.gant_manager.gant_prod)
        self.central_widget.setLayout(vbox)
        self.setCentralWidget(self.central_widget)
        vbox.addWidget(self.toolbar_gantt)
        vbox.addWidget(self.gant_manager.gant_prod)
        vbox.addWidget(self.tab_prod_bobines)
        vbox.addStretch()

    def create_plan_prod_creator_window(self):
        self.plan_prod_window = PlanProdCreator(plan_prod=settings_store_gestion.plan_prod)

    def create_event_config_window(self, type_event):
        from gestion.ui.window.event_config import EventConfig
        self.event_windows.append(EventConfig(type_event=type_event))

    def create_event_config_edit_window(self, event):
        from gestion.ui.window.event_config import EventConfig
        self.event_windows.append(EventConfig(type_event=event.p_type, event=event))
