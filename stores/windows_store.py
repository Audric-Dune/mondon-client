# !/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtCore import pyqtSignal, QObject


class WindowsStore(QObject):
    NEW_WINDOWS_CHANGED_SIGNAL = pyqtSignal()

    def __init__(self):
        super(WindowsStore, self).__init__()

    def set(self):
        self.NEW_WINDOWS_CHANGED_SIGNAL.emit()


windows_store = WindowsStore()
