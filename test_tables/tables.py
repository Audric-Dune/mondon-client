# !/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QIcon, QFont

from commun.constants.colors import color_gris_clair, color_rouge, color_noir
from commun.stores.bobine_fille_store import bobine_fille_store
from commun.utils.core_table import TableModel
from gestion.stores.filter_store import filter_store
from gestion.ui.selector_ui.selector_collum_filter import SelectorCollumFilter


class BobineFilleTableModel(TableModel):

    # Quelques constantes
    logo_dune_production = QIcon('commun/assets/icons/logo_dune_production.ico')
    etat_font = QFont('Arial Narrow', 14, QFont.Bold)
    sommeil_background_color = QColor(*color_gris_clair.rgb_components)
    default_color = QColor(*color_noir.rgb_components)
    etat_rupture_color = QColor(*color_rouge.rgb_components)
    column_widths = {
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
        "sommeil": 100,
    }

    def __int__(self, plan_prod):
        self.plan_prod = plan_prod

    def refresh(self):
        self.elements = self.get_elements()
        len_elements = len(self.elements)
        len_collums = len(self.get_columns())
        self.dataChanged.emit(self.createIndex(0, 0), self.createIndex(len_elements, len_collums))

    def get_elements(self):
        """
        Définit la liste des objets à afficher dans la table
        """
        return bobine_fille_store.bobines

    def get_columns(self):
        """
        Définit la liste des colonnes de la table
        """
        return ['code', 'laize', 'color', 'gr', 'length', 'poses', 'vente_mensuelle', 'stock_at_time',
                'stock_therme_at_time', 'etat', 'sommeil']

    def get_column_widget(self, column):
        """
        Crée le widget a afficher pour la colonne `column`
        """
        try:
            index = filter_store.list_filter_bobine_fille.index(column)
            return SelectorCollumFilter(parent=None,
                                        title=filter_store.title_filter_bobine_fille[index],
                                        name_filter=filter_store.list_filter_bobine_fille[index],
                                        sort_mode=filter_store.sort_mode_bobine_fille[index],
                                        filter_mode=filter_store.filter_mode_bobine_fille[index])
        except ValueError:
            return None
        except KeyError:
            return None

    def get_column_width(self, column):
        """
        Définit la largeur en pixel de la colonne `column`
        """
        return self.column_widths[column]

    def get_column_height(self):
        """
        Définit la hauteur des colonnes
        """
        return 21

    def get_text(self, element, column):
        """
        Retourne le texte qui est affiché pour l'élément `element` dans la colonne `column`
        """
        return str(getattr(element, column))

    def get_icon(self, element, column):
        """
        Retourne l'icone affiché à gauche du texte pour l'élément `element` dans la colonne `column`
        """
        if column == 'code':
            return self.logo_dune_production
        return None

    def get_font(self, element, column):
        """
        Retourne la font du texte pour l'élément `element` dans la colonne `column`
        """
        if column == 'etat':
            return self.etat_font
        return None

    def get_alignment(self, element, column):
        """
        Retourne l'alignement du texte pour l'élément `element` dans la colonne `column`
        """
        if column == 'etat':
            return Qt.AlignCenter
        return None

    def get_background_color(self, element, column):
        """
        Retourne la background color de la case pour l'élément `element` dans la colonne `column`
        """
        if element.sommeil == 'Sommeil':
            return self.sommeil_background_color
        return None

    def get_color(self, element, column):
        """
        Retourne la couleur du texte pour l'élément `element` dans la colonne `column`
        """
        if column == 'etat' and element.etat == 'RUPTURE':
            return self.etat_rupture_color
        return self.default_color
