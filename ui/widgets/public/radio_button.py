# !/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtCore import QObject
from ui.widgets.public.pixmap_button import PixmapButton


class RadioButtonManager(QObject):
    def __init__(self):
        super(RadioButtonManager, self).__init__()
        self.radio_buttons = []

    def add(self, radio_button):
        self.radio_buttons.append(radio_button)
        radio_button.clicked.connect(lambda: self.on_click(radio_button))

    def remove(self, radio_button):
        self.radio_buttons.remove(radio_button)

    def on_click(self, radio_button):
        for current_button in self.radio_buttons:
            current_button.is_selected = current_button is radio_button


class RadioButton(PixmapButton):
    def __init__(self, parent=None):
        super(RadioButton, self).__init__(parent=parent)
        self._is_selected = False
        self.update_widget()

    @property
    def is_selected(self):
        return self._is_selected

    @is_selected.setter
    def is_selected(self, new_value):
        if new_value == self._is_selected:
            return
        self._is_selected = new_value
        self.update_widget()

    def update_widget(self):
        if self._is_selected:
            self.addImage("assets/images/white_check.png")
        else:
            self.addImage("assets/images/impression.png")