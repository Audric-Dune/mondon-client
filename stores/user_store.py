# !/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtCore import pyqtSignal, QObject


class UserStore(QObject):
    ON_USER_CHANGED_SIGNAL = pyqtSignal()

    def __init__(self):
        super(UserStore, self).__init__()
        self.data_on_database = []
        self.level_user = 0


user_store = UserStore()
