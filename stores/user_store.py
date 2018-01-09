# !/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtCore import pyqtSignal, QObject


class UserStore(QObject):
    ON_USER_CHANGED_FIRST_TIME_SIGNAL = pyqtSignal()
    ON_USER_CHANGED_SIGNAL = pyqtSignal()
    OPEN_POPUP_USER_SIGNAL = pyqtSignal()

    def __init__(self):
        super(UserStore, self).__init__()
        self.data_on_database = []
        self.user_level = None

    def create_popup_user(self):
        self.OPEN_POPUP_USER_SIGNAL.emit()

    def update_user_level(self, user_level):
        prev_user = self.user_level
        self.user_level = user_level
        if prev_user:
            self.ON_USER_CHANGED_SIGNAL.emit()
        else:
            self.ON_USER_CHANGED_FIRST_TIME_SIGNAL.emit()


user_store = UserStore()
