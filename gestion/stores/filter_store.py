# !/usr/bin/env python
# -*- coding: utf-8 -*-


from PyQt5.QtCore import QObject, pyqtSignal


class FilterStore(QObject):
    ON_CHANGED_SIGNAL = pyqtSignal()

    def __init__(self):
        super(FilterStore, self).__init__()
        self.plan_prod = None
        self.dicts_filter = {}
        self.list_filter = ["laize", "color", "gr", "lenght", "poses",
                            "vente_mensuelle", "stock", "stock_therme", "etat", "sommeil"]
        self.title_filter = ["Laize", "Couleur", "Grammage", "Longueur", "Pose(s)",
                             "Vente mensuelle", "Stock", "Stock à therme", "Etat", "Sommeil"]
        self.filter_mode = [True, True, True, True, True, False, False, False, True, True]
        self.sort_mode = [True, True, True, True, False, True, True, True, False, False]
        self.sort_name = "code"
        self.sort_asc = True
        self.search_code = None
        self.data_type = None
        self.init_dicts_filter()

    def reset_hard(self):
        self.sort_name = "code"
        self.sort_asc = True
        self.search_code = None
        self.data_type = None
        self.init_dicts_filter()

    def init_dicts_filter(self):
        for name in self.list_filter:
            self.dicts_filter[name] = {"Tout": True}

    def update_dicts_filter(self):
        for name_filter in self.list_filter:
            new_dict_filter = self.get_new_dict_filter(name_filter)
            self.update_dict_filter(name_filter, new_dict_filter)
            self.sort_dict(name_filter)

    def sort_dict(self, name_filter):
        current_dict = self.dicts_filter[name_filter]
        new_dict_filter = {"Tout": True}
        list_key = []
        for key in current_dict.keys():
            if key != "Tout":
                list_key.append(key)
        list_key.sort()
        for key in list_key:
            value = current_dict.get(key)
            new_dict_filter[key] = value
        self.dicts_filter[name_filter] = new_dict_filter

    def get_new_dict_filter(self, name_filter):
        new_dict_filter = {"Tout": True}
        for bobine in self.plan_prod.current_bobine_fille_store.bobines:
            value = getattr(bobine, name_filter)
            if name_filter == "poses":
                for pose in value:
                    if new_dict_filter.get(pose) is None:
                        new_dict_filter[pose] = True
            else:
                if new_dict_filter.get(value) is None:
                    new_dict_filter[value] = True
        return new_dict_filter

    def update_dict_filter(self, name_filter, new_dict_filter):
        current_dict = self.dicts_filter[name_filter]
        for new_key in new_dict_filter.keys():
            if current_dict.get(new_key) is None:
                current_dict[new_key] = current_dict["Tout"]
        delete_key = []
        for current_key in current_dict.keys():
            if new_dict_filter.get(current_key) is None:
                delete_key.append(current_key)
        for key in delete_key:
            del current_dict[key]

    def set_plan_prod(self, plan_prod):
        self.reset_hard()
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

    def set_sort_param(self, sort_name, sort_asc):
        if self.sort_name == sort_name and self.sort_asc == sort_asc:
            self.sort_name = "code"
            self.sort_asc = True
        else:
            self.sort_name = sort_name
            self.sort_asc = sort_asc
        self.ON_CHANGED_SIGNAL.emit()

    def set_search_code(self, search_code):
        self.search_code = search_code
        self.ON_CHANGED_SIGNAL.emit()

    def set_data_type(self, data_type):
        self.data_type = data_type
        self.ON_CHANGED_SIGNAL.emit()

    def is_filtered(self, title):
        values = self.dicts_filter[title]
        for key in values.keys():
            if not values.get(key):
                return True
        return False


filter_store = FilterStore()
