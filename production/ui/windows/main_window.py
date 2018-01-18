# !/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.Qt import Qt
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QSizePolicy, QHBoxLayout

from commun.constants.dimensions import chart_menu_height
from commun.ui.team_gestion.tab_team_gestion import TabTeamGestion
from commun.utils.layout import clear_layout

from production.stores.settings_store import settings_store
from production.ui.widgets.prod.chart.chart import Chart
from production.ui.widgets.prod.chart.chart_menu import ChartMenu
from production.ui.widgets.prod.chart_stat.stat_titre import StatTitre
from production.ui.widgets.rapport.menu_rapport import RapportMenu
from production.ui.widgets.stat.chart_bar import ChartBar
from production.ui.widgets.stat.chart_bar_menu import ChartBarMenu
from production.ui.widgets.stat.stat_menu import StatMenu
from production.ui.widgets.app_menu import AppMenu
from production.ui.widgets.prod.tableau_arret.tab_arret_menu import TabArretMenu
from production.ui.widgets.rapport.preview_rapport import PreviewRapport
from production.ui.widgets.stat.data_tab import DataTab


class MainWindow(QMainWindow):

    def __init__(self, on_close, on_resize):
        super(MainWindow, self).__init__(None)
        self.central_widget = QWidget(parent=self)
        self.app_menu = AppMenu(parent=self)
        self.app_menu.MENU_CHANGED_SIGNAL.connect(self.update_widget)
        self.master_vbox = QVBoxLayout(self.central_widget)
        self.content_vbox = QVBoxLayout()
        self.on_close = on_close
        self.on_resize = on_resize

    def initialisation(self):
        self.app_menu.setFixedHeight(30)
        self.master_vbox.addWidget(self.app_menu)
        self.content_vbox.addLayout(self.create_prod_layout())
        self.master_vbox.addLayout(self.content_vbox)
        self.central_widget.setLayout(self.master_vbox)
        self.setCentralWidget(self.central_widget)

    def update_widget(self, menu_selected="chart_stat"):
        clear_layout(self.content_vbox)
        if menu_selected == "chart_stat":
            settings_store.set(day_ago=0)
            self.content_vbox.addLayout(self.create_stat_layout())
        elif menu_selected == "rapport":
            self.content_vbox.addLayout(self.create_rapport_layout())
        elif menu_selected == "team_gestion":
            self.content_vbox.addLayout(self.create_team_gestion_layout())
        else:
            self.content_vbox.addLayout(self.create_prod_layout())

    def create_stat_layout(self):
        hbox = QHBoxLayout()

        stat_menu = StatMenu(parent=self)
        hbox.addWidget(stat_menu)

        vbox = QVBoxLayout()

        chart_bar_menu = ChartBarMenu(parent=self)
        chart_bar_menu.setFixedHeight(50)
        vbox.addWidget(chart_bar_menu)

        self.chart_bar = ChartBar(parent=self)
        self.chart_bar.setSizePolicy(QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding))
        vbox.addWidget(self.chart_bar)

        data_tab = DataTab(parent=self)
        vbox.addWidget(data_tab, alignment=Qt.AlignTop)

        hbox.addLayout(vbox)
        return hbox

    def create_prod_layout(self):
        vbox = QVBoxLayout()

        chart_menu = ChartMenu(parent=self.central_widget)
        chart_menu.setFixedHeight(chart_menu_height)
        vbox.addWidget(chart_menu)

        chart = Chart(parent=self.central_widget)
        chart.setMinimumHeight(300)
        vbox.addWidget(chart)

        stat_menu = StatTitre(parent=self.central_widget)
        stat_menu.setFixedHeight(170)
        vbox.addWidget(stat_menu)

        tab_arret_menu = TabArretMenu(parent=self.central_widget)
        tab_arret_menu.setMaximumHeight(300)
        vbox.addWidget(tab_arret_menu)

        return vbox

    def create_rapport_layout(self):
        vbox = QVBoxLayout()

        rapport_menu = RapportMenu(parent=self.central_widget)
        rapport_menu.setFixedHeight(chart_menu_height)
        vbox.addWidget(rapport_menu)

        preview_rapport = PreviewRapport(parent=self)
        vbox.addWidget(preview_rapport)

        return vbox

    def create_team_gestion_layout(self):
        vbox = QVBoxLayout()
        tab_team_gestion = TabTeamGestion(parent=self)
        vbox.addWidget(tab_team_gestion)
        return vbox

    def resizeEvent(self, event):
        self.on_resize()
        return super(MainWindow, self).resizeEvent(event)

    def closeEvent(self, QCloseEvent):
        self.on_close()
