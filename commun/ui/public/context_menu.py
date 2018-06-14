# !/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCursor, QPainter, QPen, QColor

from commun.constants.colors import color_gris_moyen, color_blanc, color_vert_moyen, color_rouge,\
    color_vert_fonce, color_rouge_clair
from commun.constants.stylesheets import white_12_no_background_label_stylesheet, black_12_label_stylesheet


class ContextMenu(QWidget):
    def __init__(self):
        super(ContextMenu, self).__init__()
        self.setWindowFlags(Qt.Popup)
        self.vbox = QVBoxLayout()
        self.vbox.setContentsMargins(0, 2, 0, 2)
        self.vbox.setSpacing(0)
        self.setMinimumWidth(100)
        self.setLayout(self.vbox)

    def add_action(self, literal_name, callback, shortcut=None, risk_style=None):
        self.vbox.addWidget(LineContextMenu(parent=self, literal_name=literal_name,
                                            callback=callback, shortcut=shortcut, risk_style=risk_style))

    def paintEvent(self, e):
        p = QPainter(self)
        color = color_gris_moyen.rgb_components
        qcolor_gris = QColor(color[0], color[1], color[2])
        color = color_blanc.rgb_components
        qcolor_blanc = QColor(color[0], color[1], color[2])
        pen = QPen()
        pen.setColor(qcolor_gris)
        p.setPen(pen)
        p.fillRect(1, 0, self.width() - 2, self.height(), qcolor_blanc)
        p.drawRect(0, 0, self.width()-1, self.height()-1)

    def showEvent(self, e):
        self.move(QCursor().pos())


class LineContextMenu(QWidget):

    def __init__(self, parent, callback, literal_name, shortcut=None, risk_style=None):
        super(LineContextMenu, self).__init__(parent=parent)
        self.parent = parent
        self.risk_style = risk_style
        self.setFixedHeight(20)
        self.callback = callback
        self.color = color_blanc
        self.label = QLabel(literal_name)
        self.label.setStyleSheet(black_12_label_stylesheet)
        if shortcut is not None and isinstance(shortcut, str):
            self.shortcut_label = QLabel(shortcut)
        self.init_widget()

    def init_widget(self):
        hbox = QHBoxLayout()
        hbox.setContentsMargins(0, 0, 0, 0)
        hbox.addWidget(self.label)
        self.setLayout(hbox)

    def paintEvent(self, e):
        p = QPainter(self)
        color = self.color.rgb_components
        qcolor = QColor(color[0], color[1], color[2])
        pen = QPen()
        pen.setColor(qcolor)
        p.setPen(pen)
        p.fillRect(1, 0, self.width()-2, self.height(), qcolor)

    def mouseReleaseEvent(self, e):
        if e.button() == Qt.LeftButton:
            self.callback()
            self.parent.close()
        super(LineContextMenu, self).mouseReleaseEvent(e)

    def mousePressEvent(self, e):
        self.color = color_rouge_clair if self.risk_style else color_vert_moyen
        self.update()
        super(LineContextMenu, self).enterEvent(e)

    def enterEvent(self, e):
        self.color = color_rouge if self.risk_style else color_vert_fonce
        self.label.setStyleSheet(white_12_no_background_label_stylesheet)
        super(LineContextMenu, self).enterEvent(e)

    def leaveEvent(self, e):
        self.color = color_blanc
        self.label.setStyleSheet(black_12_label_stylesheet)
        super(LineContextMenu, self).leaveEvent(e)
