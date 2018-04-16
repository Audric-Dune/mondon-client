# !/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.Qt import QIntValidator
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtCore import QEvent, pyqtSignal


class TextEdit(QLineEdit):

    def __init__(self, number_only=None, parent=None):
        super(TextEdit, self).__init__(parent=parent)
        self.number_only = number_only
        self.installEventFilter(self)
        if number_only:
            self.onlyInt = QIntValidator()
            self.setValidator(self.onlyInt)

    def eventFilter(self, object, e):
        if e.type() == QEvent.MouseButtonPress:
            self.selectAll()
            return True
        return False
