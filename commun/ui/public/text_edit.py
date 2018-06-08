# !/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.Qt import QIntValidator, Qt
from PyQt5.QtWidgets import QLineEdit

from commun.constants.stylesheets import line_edit_stylesheet


class TextEdit(QLineEdit):

    def __init__(self, number_only=None, number_min=None, number_max=None, number_limit=None,
                 parent=None, upper_mode=False, init_value=None, width=None, alignement=None, mode_min=False):
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
        self.mode_min = mode_min
        self.installEventFilter(self)
        self.all_selected = False
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
            if init_value == 0:
                init_value = "00"
            self.setText(str(init_value))

    def on_text_changed(self):
        if self.upper_mode:
            self.setText(self.text().upper())
        if self.mode_min and self.text() == "0":
            self.setText("00")

    def mouseReleaseEvent(self, e):
        if not self.all_selected:
            self.selectAll()
            self.all_selected = True
        else:
            self.all_selected = False
        super(TextEdit, self).mouseReleaseEvent(e)

    def focusOutEvent(self, e):
        self.all_selected = False
        super(TextEdit, self).focusOutEvent(e)
