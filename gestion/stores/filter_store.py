# !/usr/bin/env python
# -*- coding: utf-8 -*-


from PyQt5.QtCore import QObject, pyqtSignal


class FilterStore(QObject):
    ON_CHANGED_SIGNAL = pyqtSignal()

    def __init__(self):
        super(FilterStore, self).__init__()
        self.plan_prod = None
        self.dict_filter = None
        self.search_code = None

    def init_dict_filter(self):
        self.dict_filter = {"laize": {"Tout": True}, "color": {"Tout": True}}

    def update_dict_filter(self):
        self.init_dict_filter()
        dict_laizes = self.dict_filter["laize"]
        for bobine in self.plan_prod.current_bobine_fille_store.bobines:
            laize = bobine.laize
            if dict_laizes.get(laize) is None:
                dict_laizes[laize] = True

    def set_plan_prod(self, plan_prod):
        self.plan_prod = plan_prod
        self.update_dict_filter()
        self.plan_prod.ON_CHANGED_SIGNAL.connect(self.update_dict_filter)

    def get_is_selected(self, title, value):
        values = self.dict_filter[title]
        for key in values.keys():
            if key == value:
                return values.get(key)

    def set_is_selected(self, title, value):
        values = self.dict_filter[title]
        if value == "Tout":
            set_selected = False if values["Tout"] else True
            for key in values.keys():
                values[key] = set_selected
        else:
            values["Tout"] = True
            for key in values.keys():
                if key == value:
                    values[key] = False if values[key] else True
                if not values[key]:
                    values["Tout"] = False
        self.ON_CHANGED_SIGNAL.emit()

    def is_filtered(self, title):
        values = self.dict_filter[title]
        for key in values.keys():
            if not values.get(key):
                return True
        return False


filter_store = FilterStore()
