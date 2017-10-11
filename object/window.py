# !/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QSizePolicy
from PyQt5.QtCore import QSize
from param.param import *
from object.chart import Chart
from object.chart_menu import ChartMenu
from object.stat_menu import StatMenu
from object.tab_arret_menu import TabArretMenu
from object.data_store_manager import data_store_manager


class Window(QMainWindow):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent=parent)

    def initialisation(self):
        central_widget = QWidget(self)

        vbox = QVBoxLayout(central_widget)

        chart_menu = ChartMenu(parent=central_widget)
        chart_menu.setFixedHeight(chart_menu_height)
        vbox.addWidget(chart_menu)

        chart = Chart(parent=central_widget)
        chart.setSizePolicy(QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding))
        vbox.addWidget(chart)

        stat_menu = StatMenu(parent=central_widget)
        stat_menu.setFixedHeight(150)
        vbox.addWidget(stat_menu)

        tab_arret_menu = TabArretMenu(parent=central_widget)
        chart.setSizePolicy(QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding))
        vbox.addWidget(tab_arret_menu)

        central_widget.setLayout(vbox)
        self.setCentralWidget(central_widget)

    def closeEvent(self, QCloseEvent):
        data_store_manager.cancel_refresh()
