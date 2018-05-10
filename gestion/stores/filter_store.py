# !/usr/bin/env python
# -*- coding: utf-8 -*-


from PyQt5.QtCore import QObject


class FilterStore(QObject):

    def __init__(self):
        super(FilterStore, self).__init__()
        self.dict_filter = {"Laize": [(130, True), (140, True), (150, False)]}

    def get_is_selected(self, title, value):
        values = self.dict_filter[title]
        for tuple in values:
            if tuple[0] == value:
                return tuple[1]


filter_store = FilterStore()
