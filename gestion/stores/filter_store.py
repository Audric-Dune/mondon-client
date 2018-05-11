# !/usr/bin/env python
# -*- coding: utf-8 -*-


from PyQt5.QtCore import QObject, pyqtSignal


class FilterStore(QObject):
    ON_CHANGED_SIGNAL = pyqtSignal()

    def __init__(self):
        super(FilterStore, self).__init__()
        self.plan_prod = None
        self.dicts_filter = {}
        self.list_filter = ["laize", "color", "gr", "lenght", "poses"]
        self.title_filter = ["Laize", "Couleur", "Grammage", "Longueur", "Pose(s)"]
        self.filter_mode = [True, True, True, True, True]
        self.sort_mode = [True, True, True, True, False]
        self.search_code = None

    def init_dicts_filter(self):
        for name in self.list_filter:
            self.dicts_filter[name] = {"Tout": True}

    def update_dicts_filter(self):
        self.init_dicts_filter()
        for name_filter in self.list_filter:
            self.update_dict_filter(name_filter)

    def update_dict_filter(self, name_filter):
        dict = self.dicts_filter[name_filter]
        for bobine in self.plan_prod.current_bobine_fille_store.bobines:
            value = getattr(bobine, name_filter)
            if name_filter == "poses":
                for pose in value:
                    if dict.get(pose) is None:
                        dict[pose] = True
            else:
                if dict.get(value) is None:
                    dict[value] = True

    def set_plan_prod(self, plan_prod):
        self.plan_prod = plan_prod
        self.update_dicts_filter()
        self.plan_prod.ON_CHANGED_SIGNAL.connect(self.update_dicts_filter)

    def get_is_selected(self, title, value):
        values = self.dicts_filter[title]
        for key in values.keys():
            if key == value:
                return values.get(key)

    def set_is_selected(self, title, value):
        values = self.dicts_filter[title]
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
        values = self.dicts_filter[title]
        for key in values.keys():
            if not values.get(key):
                return True
        return False


filter_store = FilterStore()
