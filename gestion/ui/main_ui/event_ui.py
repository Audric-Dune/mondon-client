# !/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QBrush, QColor
from PyQt5.QtCore import Qt

from commun.constants.colors import color_rouge
from commun.ui.public.context_menu import ContextMenu

from gestion.stores.settings_store import settings_store_gestion


class EventUi(QWidget):
    def __init__(self, event, ech, parent=None):
        super(EventUi, self).__init__(parent=parent)
        self.ech = ech
        self.event = event
        self.context_menu = ContextMenu()
        self.init_context_menu()
        self.init_ui()
        self.show()

    def init_ui(self):
        self.setFixedWidth(self.ech*(self.event.end-self.event.start))
        self.setFixedHeight(50)

    def init_context_menu(self):
        self.context_menu.add_action(literal_name="Modifier", callback=self.edit_event)
        self.context_menu.add_action(literal_name="Supprimer", callback=self.delete_event)

    def delete_event(self):
        settings_store_gestion.delete_event(self.event)

    def edit_event(self):
        print("edit_event")

    def paintEvent(self, e):
        p = QPainter(self)
        color = color_rouge.rgb_components
        qcolor_background = QColor(color[0], color[1], color[2])
        brush = QBrush()
        brush.setStyle(Qt.BDiagPattern)
        brush.setColor(qcolor_background)
        p.setBrush(brush)
        p.drawRect(0, 0, self.width()-1, self.height()-1)

    def mousePressEvent(self, e):
        if e.button() == Qt.RightButton:
            self.context_menu.show()
