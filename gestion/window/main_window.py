# !/usr/bin/env python
# -*- coding: utf-8 -*-


from PyQt5.QtWidgets import QMainWindow, QWidget, QHBoxLayout
from PyQt5.QtCore import Qt, QRect
from PyQt5.QtGui import QCursor

from commun.model.plan_prod import PlanProd

from gestion.ui.bobine_fille_selected import BobineFilleSelected
from gestion.ui.tab_bobine import TabBobine


class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__(parent=None, flags=Qt.Window)
        self.plan_prod = PlanProd()
        self.drag_bobine = None
        self.central_widget = QWidget(parent=self, flags=Qt.Widget)
        self.setMouseTracking(True)
        self.bobine_fille_selected = BobineFilleSelected()
        self.installEventFilter(self.bobine_fille_selected)
        self.tab_bobine = TabBobine(plan_prod=self.plan_prod)
        self.tab_bobine.setFixedWidth(400)
        self.tab_bobine.DRAG_SIGNAL.connect(self.handle_drag_bobine)
        self.tab_bobine.STOP_DRAG_SIGNAL.connect(self.handle_stop_drag_bobine)
        self.init_widget()

    def init_widget(self):
        hbox = QHBoxLayout()
        hbox.addWidget(self.tab_bobine)
        hbox.addWidget(self.bobine_fille_selected)
        self.central_widget.setLayout(hbox)
        self.setCentralWidget(self.central_widget)

    def handle_drag_bobine(self, bobine_code):
        self.drag_bobine = bobine_code

    def handle_stop_drag_bobine(self):
        if self.cursor_in_widget(self.bobine_fille_selected) and self.drag_bobine:
            self.plan_prod.add_bobine_fille(self.drag_bobine)
            self.bobine_fille_selected.set_text(self.drag_bobine)
            self.tab_bobine.update_widget()
        else:
            self.drag_bobine = None

    def cursor_in_widget(self, widget):
        cursor = QCursor()
        mouse_pos = cursor.pos()
        rec_widget = widget.geometry()
        rec_absolute = QRect()
        rec_absolute.setX(rec_widget.x()+self.pos().x())
        rec_absolute.setY(rec_widget.y()+self.pos().y())
        rec_absolute.setHeight(rec_widget.height())
        rec_absolute.setWidth(rec_widget.width())
        return rec_absolute.contains(mouse_pos)
