# !/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QBrush, QColor, QPen
from PyQt5.QtCore import Qt

from commun.constants.colors import color_gris_noir, color_rouge, color_noir

from gestion.stores.settings_store import settings_store_gestion


class EventUi(QWidget):
    def __init__(self, event, ech, parent=None):
        super(EventUi, self).__init__(parent=parent)
        self.setFocusPolicy(Qt.ClickFocus)
        self.ech = ech
        self.event = event
        self.border_color = color_noir
        self.init_ui()
        self.show()

    def init_ui(self):
        self.setFixedWidth(self.ech*(self.event.end-self.event.start)+1)
        self.setFixedHeight(50)

    def delete_event(self):
        settings_store_gestion.delete_event(self.event)

    def paintEvent(self, e):
        p = QPainter(self)
        color = color_gris_noir.rgb_components
        background_color = QColor(color[0], color[1], color[2])
        brush = QBrush()
        brush.setStyle(Qt.BDiagPattern)
        brush.setColor(background_color)
        p.setBrush(brush)
        p.drawRect(0, 0, self.width(), self.height())
        color = self.border_color.rgb_components
        qborder_color = QColor(color[0], color[1], color[2])
        pen = QPen()
        pen.setColor(qborder_color)
        p.setPen(pen)
        p.drawRect(0, 0, self.width()-1, self.height()-1)

    def focusInEvent(self, e):
        self.border_color = color_rouge
        self.update()
        settings_store_gestion.set_item_focus(item=self.event)

    def focusOutEvent(self, e):
        self.border_color = color_noir
        self.update()
        if not settings_store_gestion.standing_insert:
            settings_store_gestion.set_item_focus(item=None)
