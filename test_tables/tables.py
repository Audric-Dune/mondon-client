from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QIcon, QFont

from commun.constants.colors import color_gris_clair, color_rouge, color_noir
from commun.stores.bobine_fille_store import bobine_fille_store

from gestion.stores.filter_store import filter_store
from gestion.ui.selector_ui.selector_collum_filter import SelectorCollumFilter

from test_tables.core import TableModel


class BobineFilleTableModel(TableModel):
    logo_dune_production = QIcon('commun/assets/icons/logo_dune_production.ico')
    etat_font = QFont('Arial Narrow', 14, QFont.Bold)
    sommeil_background_color = QColor(*color_gris_clair.rgb_components)
    default_color = QColor(*color_noir.rgb_components)
    etat_rupture_color = QColor(*color_rouge.rgb_components)

    def get_elements(self):
        return bobine_fille_store.bobines

    def get_columns(self):
        return [
            'code',
            'laize',
            'color',
            'gr',
            'length',
            'poses',
            'vente_mensuelle',
            'stock',
            'stock_therme',
            'etat',
            'sommeil',
        ]

    def get_column_widget(self, column):
        try:
            index = filter_store.list_filter_bobine_fille.index(column)
            return SelectorCollumFilter(parent=None,
                                        title=filter_store.title_filter_bobine_fille[index],
                                        name_filter=filter_store.list_filter_bobine_fille[index],
                                        sort_mode=filter_store.sort_mode_bobine_fille[index],
                                        filter_mode=filter_store.filter_mode_bobine_fille[index])
        except ValueError:
            return None

    def get_column_width(self, column):
        if column == 'code':
            return 200
        else:
            return 100

    def get_column_height(self):
        return 21

    def get_text(self, bobine_fille, column):
        return getattr(bobine_fille, column)

    def get_icon(self, bobine_fille, column):
        if column == 'code':
            return self.logo_dune_production
        return None

    def get_font(self, bobine_fille, column):
        if column == 'etat':
            return self.etat_font
        return None

    def get_alignment(self, bobine_fille, column):
        if column == 'etat':
            return Qt.AlignCenter
        return None

    def get_background_color(self, bobine_fille, column):
        if bobine_fille.sommeil == 'Sommeil':
            return self.sommeil_background_color
        return None

    def get_color(self, bobine_fille, column):
        if column == 'etat' and bobine_fille.etat == 'RUPTURE':
            return self.etat_rupture_color
        return self.default_color