# !/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtCore import QEvent
from PyQt5.QtWidgets import QLabel


class Label(QLabel):
    """
    Label amélioré
    """
    def __init__(self, text, style, hover_style):
        super(Label, self).__init__()
        self.style = style
        self.hover_style = hover_style
        self.installEventFilter(self)
        self.setText(text)
        self.setStyleSheet(style)

    def eventFilter(self, o, e):
        if e.type() == QEvent.Enter:
            print("enter")
            self.setStyleSheet(self.hover_style)
            return True
        if e.type() == QEvent.Leave:
            print("leave")
            self.setStyleSheet(self.style)
            return True
        return False
