# !/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QHBoxLayout, QLabel
from PyQt5.QtCore import QEvent, pyqtSignal, QPoint
from commun.ui.public.mondon_widget import MondonWidget
from commun.constants.colors import color_blanc, color_rouge


class LigneBobine(MondonWidget):
    DRAG_SIGNAL = pyqtSignal(str)
    STOP_DRAG_SIGNAL = pyqtSignal()

    def __init__(self, parent=None, bobine=None):
        super(LigneBobine, self).__init__(parent=parent)
        self.state = None
        self.installEventFilter(self)
        self.bobine = bobine
        self.background_color = color_rouge if self.bobine.alert else color_blanc
        self.init_widget()

    def init_widget(self):
        hbox = QHBoxLayout()
        hbox.setContentsMargins(5, 0, 0, 0)
        self.setLayout(hbox)
        code = QLabel(str(self.bobine.code))
        code.setFixedWidth(150)
        hbox.addWidget(code)
        laize = QLabel(str(int(self.bobine.laize)))
        hbox.addWidget(laize)
        color = QLabel(str(self.bobine.color.capitalize()))
        hbox.addWidget(color)
        pose = QLabel(str(self.bobine.pose))
        hbox.addWidget(pose)

    def eventFilter(self, QObject, e):
        if e.type() == QEvent.MouseButtonPress:
            self.set_border(color_rouge)
            self.state = "is_selected"
            return True
        if e.type() == QEvent.MouseButtonRelease:
            self.set_border(color=None)
            self.state = None
            self.STOP_DRAG_SIGNAL.emit()
            return True
        if e.type() == QEvent.MouseMove and self.state == "is_selected":
            self.DRAG_SIGNAL.emit(self.bobine.code)
            return True
        return False
