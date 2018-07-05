# !/usr/bin/env python
# -*- coding: utf-8 -*-


from PyQt5.QtGui import QColor
from PyQt5.QtCore import Qt

from commun.constants.colors import color_noir, color_blanc, color_gris_clair
from commun.utils.core_table import TableModel


class BobineFilleTableSelector(TableModel):

    def __init__(self, plan_prod):
        super(BobineFilleTableSelector, self).__init__()
        self.plan_prod = plan_prod
        self.column_widths = {
            "code": 250,
            "laize": 100,
            "color": 120,
            "gr": 120,
            "length": 100,
            "poses": 100,
            "vente_mensuelle": 150,
            "stock_at_time": 100,
            "stock_therme_at_time": 150,
            "etat": 120,
            "sommeil": 100
        }

    def get_elements(self):
        """
        Définit la liste des objets à afficher dans la table
        """
        return self.plan_prod.current_bobine_fille_store.bobines

    def get_columns(self):
        return ['code', 'laize', 'color', 'gr', 'length', 'poses', 'vente_mensuelle', 'stock_at_time',
                'stock_therme_at_time', 'etat', 'sommeil']

    def get_column_width(self, column):
        """
        Définit la largeur en pixel de la colonne `column`
        """
        return self.column_widths[column]

    def get_alignment(self, element, column):
        if column == "code":
            return Qt.AlignLeft | Qt.AlignVCenter
        return Qt.AlignCenter | Qt.AlignVCenter

    def get_text(self, element, column):
        if column == "laize":
            return str(int(getattr(element, column)))
        return str(getattr(element, column))

    def get_color(self, element, column):
        return QColor(*color_noir.rgb_components)
