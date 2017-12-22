# !/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QSizePolicy, QHBoxLayout
from ui.widgets.prod.chart.chart import Chart

from constants.dimensions import chart_menu_height
from ui.utils.layout import clear_layout
from ui.widgets.app_menu import AppMenu
from ui.widgets.prod.chart.chart_menu import ChartMenu
from ui.widgets.prod.chart_stat.stat_titre import StatTitre
from ui.widgets.prod.tableau_arret.tab_arret_menu import TabArretMenu
from ui.widgets.stat.chart_bar import ChartBar
from ui.widgets.stat.data_tab import DataTab
from ui.widgets.stat.stat_menu import StatMenu
from ui.widgets.stat.chart_bar_menu import ChartBarMenu
from ui.widgets.rapport.menu_rapport import RapportMenu
from ui.widgets.rapport.preview_rapport import PreviewRapport


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

    def update_widget(self, menu_selected):
        clear_layout(self.content_vbox)
        if menu_selected == "chart_stat":
            self.content_vbox.addLayout(self.create_stat_layout())
            QTimer.singleShot(0, self.chart_bar.update_widget)
        elif menu_selected == "rapport":
            self.content_vbox.addLayout(self.create_rapport_layout())
        else:
            self.content_vbox.addLayout(self.create_prod_layout())

    def create_stat_layout(self):
        hbox = QHBoxLayout()

        stat_menu = StatMenu(parent=self)
        stat_menu.setFixedWidth(300)
        hbox.addWidget(stat_menu)

        vbox = QVBoxLayout()

        chart_bar_menu = ChartBarMenu(parent=self)
        chart_bar_menu.setFixedHeight(50)
        vbox.addWidget(chart_bar_menu)

        self.chart_bar = ChartBar(parent=self)
        self.chart_bar.setSizePolicy(QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding))
        vbox.addWidget(self.chart_bar)

        data_tab = DataTab(parent=self)
        data_tab.setFixedHeight(200)
        vbox.addWidget(data_tab)

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
        stat_menu.setFixedHeight(160)
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

    def resizeEvent(self, event):
        self.on_resize()
        return super(MainWindow, self).resizeEvent(event)

    def closeEvent(self, QCloseEvent):
        self.on_close()
