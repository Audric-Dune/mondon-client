# !/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QVBoxLayout, QWidget, QScrollArea
from PyQt5.QtCore import Qt

from commun.constants.colors import color_bleu_gris
from commun.constants.stylesheets import scroll_bar_stylesheet
from commun.ui.public.mondon_widget import MondonWidget
from gestion.stores.filter_store import filter_store
from gestion.stores.settings_store import settings_store_gestion
from gestion.ui.line_in_selector.line_bobine import LineBobine
from gestion.ui.line_in_selector.line_bobine_papier import LineBobinePapier
from gestion.ui.line_in_selector.line_bobine_poly import LineBobinePoly
from gestion.ui.line_in_selector.line_perfo import LinePerfo
from gestion.ui.line_in_selector.line_refente import LineRefente
from gestion.ui.selector_ui.selector_pose import SelectorPose


class SelectorTable(MondonWidget):

    def __init__(self, plan_prod, parent):
        super(SelectorTable, self).__init__(parent=parent)
        self.plan_prod = plan_prod
        self.parent = parent
        self.table_bobine_fille = None
        filter_store.ON_CHANGED_SIGNAL.connect(self.update_widget)
        self.background_color = color_bleu_gris
        self.master_vbox = QVBoxLayout()
        self.master_vbox.setContentsMargins(0, 0, 0, 0)
        self.master_vbox.setSpacing(0)
        self.selector_pose = None
        self.vbox = QVBoxLayout()
        self.init_widget()

    def init_widget(self):
        self.vbox.setContentsMargins(0, 0, 0, 0)
        self.vbox.setSpacing(5)
        from gestion.ui.selector_ui.bobine_fille_table_selector import BobineFilleTableSelector
        from commun.utils.core_table import Table
        self.table_bobine_fille = Table(model=BobineFilleTableSelector(self.plan_prod), parent=self)
        self.table_bobine_fille.mouse_double_click_signal.connect(self.get_bobine_with_index)
        self.master_vbox.addWidget(self.table_bobine_fille)
        self.setLayout(self.master_vbox)

    def update_widget(self):
        if self.table_bobine_fille is not None:
            self.table_bobine_fille.refresh()

    def get_bobine_with_index(self, index):
        try:
            self.handle_selected_bobine(bobine=self.plan_prod.current_bobine_fille_store.bobines[index])
        except IndexError:
            pass

    def handle_selected_bobine(self, bobine, pose=None):
        if pose:
            self.plan_prod.add_bobine_selected(bobine, pose)
        elif len(bobine.poses) == 1:
            self.plan_prod.add_bobine_selected(bobine, bobine.poses[0])
        else:
            self.selector_pose = SelectorPose(self.handle_selected_bobine, bobine)
            self.selector_pose.show()
        self.update_widget()
        settings_store_gestion.plan_prod.get_new_item_selected_from_store()
