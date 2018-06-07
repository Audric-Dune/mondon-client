# !/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.Qt import QIntValidator, Qt
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtCore import QEvent

from commun.constants.stylesheets import line_edit_stylesheet


class TextEdit(QLineEdit):

    def __init__(self, number_only=None, number_min=None, number_max=None, number_limit=None,
                 parent=None, upper_mode=False, init_value=None, width=None, alignement=None):
        super(TextEdit, self).__init__(parent=parent)
        self.setStyleSheet(line_edit_stylesheet)
        if width:
            self.setFixedWidth(width)
        self.upper_mode = upper_mode
        self.textChanged.connect(self.on_text_changed)
        self.number_only = number_only
        self.number_limit = number_limit
        self.number_min = number_min
        self.number_max = number_max
        self.only_int = None
        self.installEventFilter(self)
        if alignement == "center":
            self.setAlignment(Qt.AlignCenter)
        if number_limit:
            self.only_int = QIntValidator(0, number_limit)
        if number_min and number_max:
            self.only_int = QIntValidator(number_min, number_max)
        if number_only:
            if not self.only_int:
                self.only_int = QIntValidator()
            self.setValidator(self.only_int)
        if init_value is not None:
            self.setText(str(init_value))

    def on_text_changed(self):
        if self.upper_mode:
            self.setText(self.text().upper())

    def eventFilter(self, object, e):
        if e.type() == QEvent.MouseButtonPress:
            self.selectAll()
            return True
        return False
