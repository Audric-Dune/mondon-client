# !/usr/bin/env python
# -*- coding: utf-8 -*-


from PyQt5.QtCore import QObject, pyqtSignal


class FilterStore(QObject):
    ON_CHANGED_SIGNAL = pyqtSignal()

    def __init__(self):
        super(FilterStore, self).__init__()
        self.plan_prod = None
        self.dict_filter = {"Laize": {}}
        self.search_code = None

    def init_dict_filter(self):
        self.dict_filter = {"Laize": {}}
        self.update_dict_filter()

    def update_dict_filter(self):
        dict_laizes = self.dict_filter["Laize"]
        for bobine in self.plan_prod.current_bobine_fille_store.bobines:
            laize = bobine.laize
            if dict_laizes.get(laize) is None:
                dict_laizes[laize] = True

    def set_plan_plan(self, plan_prod):
        self.plan_prod = plan_prod
        self.init_dict_filter()
        self.plan_prod.ON_CHANGED_SIGNAL.connect(self.update_dict_filter)

    def get_is_selected(self, title, value):
        values = self.dict_filter[title]
        for key in values.keys():
            if key == value:
                return values.get(key)

    def set_is_selected(self, title, value):
        values = self.dict_filter[title]
        for key in values.keys():
            if key == value:
                values[key] = False if values[key] else True
        self.ON_CHANGED_SIGNAL.emit()


filter_store = FilterStore()
