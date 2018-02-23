# !/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtCore import QEvent


class TextEdit(QLineEdit):
    def __init__(self, parent=None):
        super(TextEdit, self).__init__(parent=parent)
        self.installEventFilter(self)

    def eventFilter(self, object, event):
        if event.type() == QEvent.MouseButtonPress:
            self.selectAll()
            return True
        return False
