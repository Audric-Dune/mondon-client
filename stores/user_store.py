# !/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtCore import pyqtSignal, QObject


class UserStore(QObject):
    ON_USER_CHANGED_SIGNAL = pyqtSignal()
    OPEN_POPUP_USER_SIGNAL = pyqtSignal()

    def __init__(self):
        super(UserStore, self).__init__()
        self.data_on_database = []
        self.user_level = 0

    def create_popup_user(self):
        self.OPEN_POPUP_USER_SIGNAL.emit()

    def update_user_level(self, user_level):
        self.user_level = user_level
        self.ON_USER_CHANGED_SIGNAL.emit()


user_store = UserStore()
