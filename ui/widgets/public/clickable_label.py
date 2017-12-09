# !/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtCore import QEvent
from PyQt5.QtWidgets import QLabel


class ClickableLabel(QLabel):
    """
    Label amélioré : permet de connecter le label a une fonction sur un click
    """
    def __init__(self, text=None):
        super(ClickableLabel, self).__init__()
        self.function_connect = None
        self.installEventFilter(self)
        self.setText(text)

    def eventFilter(self, source, event):
        if event.type() == QEvent.MouseButtonRelease and source == self:
            self._onclick()
            return True
        else:
            return False

    def connect(self, fct=None):
        self.function_connect = fct

    def _onclick(self):
        if self.function_connect:
            self.function_connect()
        pass
