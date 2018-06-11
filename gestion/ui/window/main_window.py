# !/usr/bin/env python
# -*- coding: utf-8 -*-


from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout
from gestion.ui.main_ui.day_menu import DayMenu
from gestion.ui.main_ui.plan_prod_creator import PlanProdCreator

from commun.constants.dimensions import chart_menu_height
from commun.utils.layout import clear_layout
from commun.utils.timestamp import timestamp_at_day_ago, is_vendredi
from gestion.stores.event_store import event_store
from gestion.stores.plan_prod_store import plan_prod_store
from gestion.stores.settings_store import settings_store_gestion
from gestion.ui.main_ui.chart_production import ChartProd
from gestion.ui.main_ui.gant_manager import GantManager


class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__(parent=None, flags=Qt.Window)
        self.central_widget = QWidget(parent=self)
        # self.vbox = QVBoxLayout()
        # settings_store_gestion.SETTINGS_CHANGED_SIGNAL.connect(self.update_widget)
        settings_store_gestion.CREATE_PLAN_PROD_WINDOW.connect(self.create_plan_prod_creator_window)
        settings_store_gestion.CREATE_EVENT_CONFIG_WINDOW.connect(self.create_event_config_window)
        plan_prod_store.get_plan_prod_from_database()
        self.gant_manager = GantManager()
        self.event_windows = []
        self.plan_prod_window = None
        self.init_widget()
        # self.update_widget()

    def init_widget(self):
        vbox = QVBoxLayout()
        day_menu = DayMenu(parent=self)
        day_menu.setFixedHeight(chart_menu_height)
        vbox.addWidget(day_menu)
        vbox.addWidget(self.gant_manager.gant_prod)
        self.central_widget.setLayout(vbox)
        # self.central_widget.setLayout(self.vbox)
        self.setCentralWidget(self.central_widget)

    def update_widget(self):
        plan_prod_store.get_plan_prod_from_database()
        clear_layout(self.vbox)
        self.vbox.addWidget(self.gant_manager.gant_prod)
        # if is_vendredi(timestamp_at_day_ago(settings_store_gestion.day_ago)):
        #     if not event_store.events:
        #         event_store.add_defaut_stop_prod()
        # chart_prod = ChartProd(parent=self, prods=plan_prod_store.plans_prods, events=event_store.events)
        # day_menu = DayMenu(parent=self)
        # day_menu.setFixedHeight(chart_menu_height)
        # self.vbox.addWidget(day_menu)
        # if settings_store_gestion.plan_prod:
        #     settings_store_gestion.plan_prod.ON_CHANGED_SIGNAL.connect(day_menu.update_state_bt)
        #     settings_store_gestion.plan_prod.ON_TOURS_CHANGED.connect(day_menu.update_state_bt)
        #     plan_prod_creator = PlanProdCreator(parent=self, plan_prod=settings_store_gestion.plan_prod)
        #     self.vbox.addWidget(plan_prod_creator)
        # else:
        #     self.vbox.addWidget(chart_prod)

    def create_plan_prod_creator_window(self):
        self.plan_prod_window = PlanProdCreator(plan_prod=settings_store_gestion.plan_prod)

    def create_event_config_window(self, type_event):
        from gestion.ui.window.event_config import EventConfig
        self.event_windows.append(EventConfig(type_event=type_event))
