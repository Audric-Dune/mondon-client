# !/usr/bin/env python
# -*- coding: utf-8 -*-


from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout
from PyQt5.QtCore import Qt

from commun.utils.layout import clear_layout
from commun.constants.dimensions import chart_menu_height
from commun.utils.timestamp import timestamp_at_day_ago, is_vendredi

from gestion.ui.widgets.plan_prod_creator import PlanProdCreator
from gestion.ui.widgets.chart_production import ChartProd
from gestion.ui.widgets.day_menu import DayMenu
from gestion.stores.settings_store import settings_store_gestion
from gestion.stores.plan_prod_store import plan_prod_store
from gestion.stores.event_store import event_store


class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__(parent=None, flags=Qt.Window)
        self.setMinimumWidth(1400)
        self.central_widget = QWidget(parent=self)
        self.vbox = QVBoxLayout()
        settings_store_gestion.SETTINGS_CHANGED_SIGNAL.connect(self.update_widget)
        plan_prod_store.get_plan_prod_from_database()
        self.init_widget()
        self.update_widget()

    def init_widget(self):
        self.central_widget.setLayout(self.vbox)
        self.setCentralWidget(self.central_widget)

    def update_widget(self):
        plan_prod_store.get_plan_prod_from_database()
        clear_layout(self.vbox)
        if is_vendredi(timestamp_at_day_ago(settings_store_gestion.day_ago)):
            if not event_store.events:
                event_store.add_defaut_stop_prod()
        chart_prod = ChartProd(parent=self, prods=plan_prod_store.plans_prods, events=event_store.events)
        day_menu = DayMenu(parent=self)
        day_menu.setFixedHeight(chart_menu_height)
        self.vbox.addWidget(day_menu)
        if settings_store_gestion.plan_prod:
            settings_store_gestion.plan_prod.ON_CHANGED_SIGNAL.connect(day_menu.update_state_bt)
            settings_store_gestion.plan_prod.ON_TOURS_CHANGED.connect(day_menu.update_state_bt)
            plan_prod_creator = PlanProdCreator(parent=self, plan_prod=settings_store_gestion.plan_prod)
            self.vbox.addWidget(plan_prod_creator)
        else:
            self.vbox.addWidget(chart_prod)

