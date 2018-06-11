# !/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QBrush, QColor
from PyQt5.QtCore import Qt

from commun.constants.colors import color_rouge, color_vert


class EventUi(QWidget):
    def __init__(self, event, ech, parent=None):
        super(EventUi, self).__init__(parent=parent)
        self.setFocusPolicy(Qt.ClickFocus)
        self.ech = ech
        self.event = event
        self.selected = True
        self.color = color_rouge
        self.init_ui()
        self.show()

    def init_ui(self):
        self.setFixedWidth(self.ech*(self.event.end-self.event.start))
        self.setFixedHeight(50)

    def paintEvent(self, e):
        p = QPainter(self)
        color = self.color.rgb_components
        qcolor = QColor(color[0], color[1], color[2])
        brush = QBrush()
        brush.setStyle(Qt.BDiagPattern)
        brush.setColor(qcolor)
        p.setBrush(brush)
        p.drawRect(0, 0, self.width()-1, self.height()-1)

    def focusInEvent(self, e):
        self.color = color_vert
        super(EventUi, self).focusInEvent(e)

    def focusOutEvent(self, e):
        self.color = color_rouge
        super(EventUi, self).focusOutEvent(e)
