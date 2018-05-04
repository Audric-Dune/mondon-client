# !/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.Qt import QIntValidator
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtCore import QEvent, pyqtSignal


class TextEdit(QLineEdit):

    def __init__(self, number_only=None, number_limit=None, parent=None, upper_mode=False):
        super(TextEdit, self).__init__(parent=parent)
        self.upper_mode = upper_mode
        self.textChanged.connect(self.on_text_changed)
        self.number_only = number_only
        self.number_limit = number_limit
        self.installEventFilter(self)
        if number_limit:
            self.only_int = QIntValidator(0, number_limit)
        if number_only:
            if not self.only_int:
                self.only_int = QIntValidator()
            self.setValidator(self.only_int)

    def on_text_changed(self):
        if self.upper_mode:
            self.setText(self.text().upper())

    def eventFilter(self, object, e):
        if e.type() == QEvent.MouseButtonPress:
            self.selectAll()
            return True
        return False
