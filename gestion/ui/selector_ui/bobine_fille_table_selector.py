# !/usr/bin/env python
# -*- coding: utf-8 -*-


from PyQt5.QtGui import QColor, QFont
from PyQt5.QtCore import Qt

from gestion.stores.filter_store import filter_store

from commun.constants.colors import color_noir, color_gris_moyen
from commun.constants.dimensions import dict_width_selector_bobine, width_search_bar
from commun.utils.core_table import TableModel


class BobineFilleTableSelector(TableModel):

    def __init__(self, plan_prod):
        super(BobineFilleTableSelector, self).__init__()
        self.plan_prod = plan_prod
        self.elements = []
        self.column_code_width = width_search_bar
        self.column_widths = dict_width_selector_bobine
        self.refresh()

    def refresh(self):
        self.elements = self.get_elements()
        self.sort_bobine()

    def sort_bobine(self):
        self.elements = self.sort_item(self.elements, "code", True)
        self.elements = self.sort_item(self.elements, filter_store.sort_name, filter_store.sort_asc)

    @staticmethod
    def sort_item(items, sort_name, sort_asc):
        items = sorted(items, key=lambda b: b.get_value(sort_name), reverse=not sort_asc)
        return items

    def get_elements(self):
        """
        Définit la liste des objets à afficher dans la table
        """
        elements = []
        for bobine in self.plan_prod.current_bobine_fille_store.bobines:
            if self.is_valid_bobine_from_filters(bobine) and self.is_valid_from_search_code(bobine):
                bobine.get_stock_at_time(time=self.plan_prod.start)
                elements.append(bobine)
        return elements

    def get_columns(self):
        return ['code', 'laize', 'color', 'gr', 'length', 'poses', 'vente_mensuelle', 'stock_at_time',
                'stock_therme_at_time', 'etat', 'sommeil']

    def get_column_width(self, column):
        """
        Définit la largeur en pixel de la colonne `column`
        """
        if column == "code":
            width = self.column_code_width + 5
        elif column == "sommeil":
            width = self.column_widths[column] + 5
        else:
            width = self.column_widths[column] + 11
        return width

    def get_alignment(self, element, column):
        if column == "code":
            return Qt.AlignLeft | Qt.AlignVCenter
        return Qt.AlignCenter | Qt.AlignVCenter

    def get_text(self, element, column):
        if column == "poses":
            return str(getattr(element, "valid_poses"))
        if column == "laize" or column == "vente_mensuelle"\
                or column == "stock_at_time" or column == "stock_therme_at_time":
            return str(int(getattr(element, column)))
        return str(getattr(element, column))

    def get_color(self, element, column):
        return QColor(*color_noir.rgb_components)

    def get_font(self, element, column):
        return QFont('Arial', 10)

    def get_background_color(self, element, column):
        if element.sommeil:
            return QColor(*color_gris_moyen.rgb_components)

    @staticmethod
    def is_valid_from_search_code(bobine):
        if not filter_store.search_code:
            return True
        elif filter_store.search_code in bobine.code:
            return True
        else:
            return False

    def is_valid_bobine_from_filters(self, bobine):
        index = 0
        for name in filter_store.list_filter_bobine_fille:
            if not filter_store.filter_mode_bobine_fille[index]:
                continue
            if not self.is_valid_bobine_from_filter(bobine, name):
                return False
            index += 1
        return True

    @staticmethod
    def is_valid_bobine_from_filter(bobine, name):
        if filter_store.data_type == "bobine":
            dict_filter = filter_store.dicts_filter[name]
            if name == "poses":
                for key in dict_filter.keys():
                    for pose in bobine.poses:
                        if key == pose and dict_filter[key]:
                            return True
                return False
            else:
                for key in dict_filter.keys():
                    if key == getattr(bobine, name) and dict_filter[key]:
                        return True
                return False
