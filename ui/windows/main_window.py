# !/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QSizePolicy, QLabel

from constants.dimensions import chart_menu_height
from ui.utils.layout import clear_layout
from ui.widgets.chart.chart import Chart
from ui.widgets.chart.chart_menu import ChartMenu
from ui.widgets.stat.stat_menu import StatMenu
from ui.widgets.tableau_arret.tab_arret_menu import TabArretMenu
from ui.widgets.app_menu import AppMenu


class MainWindow(QMainWindow):
    def __init__(self, on_close):
        super(MainWindow, self).__init__(None)
        self.central_widget = QWidget(parent=self)
        self.app_menu = AppMenu(parent=self)
        self.app_menu.MENU_CHANGED_SIGNAL.connect(self.update_widget)
        self.master_vbox = QVBoxLayout(self.central_widget)
        self.content_vbox = QVBoxLayout()
        self.on_close = on_close

    def initialisation(self):
        self.app_menu.setFixedHeight(30)
        self.master_vbox.addWidget(self.app_menu)
        self.content_vbox.addLayout(self.create_prod_layout())
        self.master_vbox.addLayout(self.content_vbox)
        self.central_widget.setLayout(self.master_vbox)
        self.setCentralWidget(self.central_widget)

    def update_widget(self, menu_selected):
        clear_layout(self.content_vbox)
        if menu_selected == "stat":
            self.content_vbox.addLayout(self.create_stat_layout())
        else:
            self.content_vbox.addLayout(self.create_prod_layout())

    @staticmethod
    def create_stat_layout():
        vbox = QVBoxLayout()
        vbox.addWidget(QLabel("STATSTIQUE"))
        return vbox

    def create_prod_layout(self):
        vbox = QVBoxLayout()

        chart_menu = ChartMenu(parent=self.central_widget)
        chart_menu.setFixedHeight(chart_menu_height)
        vbox.addWidget(chart_menu)

        chart = Chart(parent=self.central_widget)
        chart.setSizePolicy(QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding))
        vbox.addWidget(chart)

        stat_menu = StatMenu(parent=self.central_widget)
        stat_menu.setFixedHeight(150)
        vbox.addWidget(stat_menu)

        tab_arret_menu = TabArretMenu(parent=self.central_widget)
        vbox.addWidget(tab_arret_menu)

        return vbox

    def closeEvent(self, QCloseEvent):
        self.on_close()
