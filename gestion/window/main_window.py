# !/usr/bin/env python
# -*- coding: utf-8 -*-


from PyQt5.QtWidgets import QMainWindow, QWidget, QHBoxLayout
from PyQt5.QtCore import Qt, QRect
from PyQt5.QtGui import QCursor

from commun.model.plan_prod import PlanProd

from gestion.ui.plan_prod_creator import PlanProdCreator


class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__(parent=None, flags=Qt.Window)
        self.central_widget = QWidget(parent=self)
        self.plan_prod_creator = PlanProdCreator(parent=self)
        self.init_widget()

    def init_widget(self):
        hbox = QHBoxLayout()
        hbox.addWidget(self.plan_prod_creator)
        self.central_widget.setLayout(hbox)
        self.setCentralWidget(self.central_widget)

    # def cursor_in_widget(self, widget):
    #     cursor = QCursor()
    #     mouse_pos = cursor.pos()
    #     rec_widget = widget.geometry()
    #     rec_absolute = QRect()
    #     rec_absolute.setX(rec_widget.x()+self.pos().x())
    #     rec_absolute.setY(rec_widget.y()+self.pos().y())
    #     rec_absolute.setHeight(rec_widget.height())
    #     rec_absolute.setWidth(rec_widget.width())
    #     return rec_absolute.contains(mouse_pos)
