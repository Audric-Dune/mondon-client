# !/usr/bin/env python
# -*- coding: utf-8 -*-


from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout
from PyQt5.QtCore import Qt

from gestion.ui.widgets.plan_prod_creator import PlanProdCreator
from gestion.ui.widgets.day_menu import DayMenu


class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__(parent=None, flags=Qt.Window)
        self.central_widget = QWidget(parent=self)
        self.plan_prod_creator = PlanProdCreator(parent=self)
        self.day_menu = DayMenu(parent=self)
        self.init_widget()

    def init_widget(self):
        vbox = QVBoxLayout()
        vbox.addWidget(self.day_menu)
        vbox.addWidget(self.plan_prod_creator)
        self.central_widget.setLayout(vbox)
        self.setCentralWidget(self.central_widget)
