# !/usr/bin/env python
# -*- coding: utf-8 -*-


from PyQt5.QtCore import QObject, pyqtSignal

from gestion.stores.settings_store import settings_store_gestion


class FilterStore(QObject):
    ON_CHANGED_SIGNAL = pyqtSignal()
    ON_DATA_TYPE_CHANGED = pyqtSignal()

    def __init__(self):
        super(FilterStore, self).__init__()
        self.data_type = None
        self.dicts_filter = {}
        # FILTER BOBINE FILLE
        self.list_filter_bobine_fille = ["laize", "color", "gr", "length", "poses",
                                         "vente_mensuelle", "stock_at_time", "stock_therme_at_time", "qte_a_prod",
                                         "etat", "sommeil"]
        self.title_filter_bobine_fille = ["Laize", "Couleur", "Grammage", "Longueur", "Pose(s)", "Vente mensuelle",
                                          "Stock", "Stock à therme", "Production opti.", "Etat", "Sommeil"]
        self.filter_mode_bobine_fille = [True, True, True, True, False, False, False, False, True, True, True]
        self.sort_mode_bobine_fille = [True, True, True, True, False, True, True, True, True, False, False]
        # FILTER POLY
        self.list_filter_poly = ["code", "laize", "length", "famille", "stock_at_time", "stock_therme_at_time"]
        self.title_filter_poly = ["Code", "Laize", "Longueur", "Famille", "Stock", "Stock à therme"]
        self.filter_mode_poly = [False, False, False, False, False, False]
        self.sort_mode_poly = [True, True, True, False, True, True]
        # FILTER BOBINE PAPIER
        self.list_filter_papier = ["code", "laize", "color", "gr", "length", "stock_at_time", "stock_therme_at_time"]
        self.title_filter_papier = ["Code", "Laize", "Couleur", "Grammage", "Longueur", "Stock", "Stock à therme"]
        self.filter_mode_papier = [False, True, True, True, True, False, False]
        self.sort_mode_papier = [True, True, True, True, True, True, True]
        # FILTER REFENTE
        self.list_filter_refente = ["code_perfo", "laize_fille", "laize"]
        self.title_filter_refente = ["Code perfo.", "Laize bobine fille", "Laize bobine mère"]
        self.filter_mode_refente = [True, True, True]
        self.sort_mode_refente = [False, False, True]
        self.sort_name = "code"
        self.sort_asc = True
        self.search_code = None
        self.init_dicts_filter()

    def reset_hard(self):
        self.sort_name = "code"
        self.sort_asc = True
        self.search_code = None
        self.init_dicts_filter()

    def init_dicts_filter(self):
        if self.data_type == "bobine":
            for name in self.list_filter_bobine_fille:
                self.dicts_filter[name] = {"Tous": True}
        if self.data_type == "poly":
            for name in self.list_filter_poly:
                self.dicts_filter[name] = {"Tous": True}
        if self.data_type == "refente":
            for name in self.list_filter_refente:
                self.dicts_filter[name] = {"Tous": True}
        if self.data_type == "papier":
            for name in self.list_filter_papier:
                self.dicts_filter[name] = {"Tous": True}

    def update_dicts_filter(self):
        if self.data_type == "bobine":
            for name_filter in self.list_filter_bobine_fille:
                new_dict_filter = self.get_new_dict_filter(name_filter)
                self.update_dict_filter(name_filter, new_dict_filter)
                self.sort_dict(name_filter)
        if self.data_type == "poly":
            for name_filter in self.list_filter_poly:
                new_dict_filter = self.get_new_dict_filter(name_filter)
                self.update_dict_filter(name_filter, new_dict_filter)
                self.sort_dict(name_filter)
        if self.data_type == "refente":
            for name_filter in self.list_filter_refente:
                new_dict_filter = self.get_new_dict_filter(name_filter)
                self.update_dict_filter(name_filter, new_dict_filter)
                self.sort_dict(name_filter)
        if self.data_type == "papier":
            for name_filter in self.list_filter_papier:
                new_dict_filter = self.get_new_dict_filter(name_filter)
                self.update_dict_filter(name_filter, new_dict_filter)
                self.sort_dict(name_filter)

    def sort_dict(self, name_filter):
        current_dict = self.dicts_filter[name_filter]
        new_dict_filter = {"Tous": True}
        list_key = []
        for key in current_dict.keys():
            if key != "Tous":
                list_key.append(key)
        if list_key and list_key[0] is str:
            list_key.sort(key=str.lower)
        else:
            list_key.sort()
        for key in list_key:
            value = current_dict.get(key)
            new_dict_filter[key] = value
        self.dicts_filter[name_filter] = new_dict_filter

    def get_new_dict_filter(self, name_filter):
        new_dict_filter = {"Tous": True}
        if self.data_type == "bobine":
            for bobine in settings_store_gestion.plan_prod.current_bobine_fille_store.bobines:
                value = getattr(bobine, name_filter)
                if name_filter == "poses":
                    for pose in value:
                        if new_dict_filter.get(pose) is None:
                            new_dict_filter[pose] = True
                else:
                    if new_dict_filter.get(value) is None:
                        new_dict_filter[value] = True
        if self.data_type == "poly":
            for bobine in settings_store_gestion.plan_prod.current_bobine_poly_store.bobines:
                if name_filter == "famille":
                    continue
                value = getattr(bobine, name_filter)
                if new_dict_filter.get(value) is None:
                    new_dict_filter[value] = True
        if self.data_type == "papier":
            for bobine in settings_store_gestion.plan_prod.current_bobine_papier_store.bobines:
                value = getattr(bobine, name_filter)
                if new_dict_filter.get(value) is None:
                    new_dict_filter[value] = True
        if self.data_type == "refente":
            for refente in settings_store_gestion.plan_prod.current_refente_store.refentes:
                if name_filter == "laize_fille":
                    for laize in refente.laizes:
                        if laize == 173.3:
                            laize = 173
                        if laize == 128.56:
                            laize = 130
                        if new_dict_filter.get(laize) is None and laize is not None:
                            new_dict_filter[laize] = True
                else:
                    value = getattr(refente, name_filter)
                    if new_dict_filter.get(value) is None:
                        new_dict_filter[value] = True
        return new_dict_filter

    def update_dict_filter(self, name_filter, new_dict_filter):
        current_dict = self.dicts_filter[name_filter]
        for new_key in new_dict_filter.keys():
            if current_dict.get(new_key) is None:
                current_dict[new_key] = current_dict["Tous"]
        delete_key = []
        for current_key in current_dict.keys():
            if new_dict_filter.get(current_key) is None:
                delete_key.append(current_key)
        for key in delete_key:
            del current_dict[key]

    def get_is_selected(self, title, value):
        values = self.dicts_filter[title]
        for key in values.keys():
            if key == value:
                return values.get(key)

    def set_is_selected(self, title, value):
        values = self.dicts_filter[title]
        if value == "Tous":
            set_selected = False if values["Tous"] else True
            for key in values.keys():
                values[key] = set_selected
        else:
            values["Tous"] = True
            for key in values.keys():
                if key == value:
                    values[key] = False if values[key] else True
                if not values[key]:
                    values["Tous"] = False
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
        self.reset_hard()
        self.update_dicts_filter()
        self.ON_DATA_TYPE_CHANGED.emit()
        self.ON_CHANGED_SIGNAL.emit()

    def is_filtered(self, title):
        values = self.dicts_filter[title]
        for key in values.keys():
            if not values.get(key):
                return True
        return False


filter_store = FilterStore()
