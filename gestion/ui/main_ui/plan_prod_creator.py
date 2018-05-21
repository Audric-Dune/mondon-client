# !/usr/bin/env python
# -*- coding: utf-8 -*-

# !/usr/bin/env python
# -*- coding: utf-8 -*-


from PyQt5.QtWidgets import QVBoxLayout, QLabel
from gestion.ui.plan_prod_creator_widget.bloc_information import BlocInformation
from gestion.ui.plan_prod_creator_widget.bloc_selected import BlocSelected
from gestion.ui.selector_ui.selector_manager import SelectorManager

from commun.constants.colors import color_blanc
from commun.constants.stylesheets import white_12_bold_label_stylesheet
from commun.ui.public.mondon_widget import MondonWidget
from gestion.stores.filter_store import filter_store
from gestion.ui.plan_prod_creator_widget.bloc_param_prod import BlocParamProd


class PlanProdCreator(MondonWidget):

    def __init__(self, plan_prod, parent=None):
        super(PlanProdCreator, self).__init__(parent=parent)
        self.set_background_color(color=color_blanc)
        self.plan_prod = plan_prod
        self.plan_prod.ON_CHANGED_SIGNAL.connect(self.handle_plan_prod_changed)
        self.plan_prod.ON_TOURS_CHANGED.connect(self.handle_tours_plan_prod_changed)
        self.selector_manager = SelectorManager(parent=self, plan_prod=self.plan_prod)
        self.selector_manager.hide()
        self.bloc_param_prod = BlocParamProd(plan_prod=self.plan_prod, parent=self)
        self.titre_prod = QLabel("NOUVELLE PRODUCTION")
        self.bloc_poly_selected = BlocSelected(data_type="poly", parent=self, callback=self.show_selector)
        self.bloc_papier_selected = BlocSelected(data_type="papier", parent=self, callback=self.show_selector)
        self.bloc_perfo_selected = BlocSelected(data_type="perfo", parent=self, callback=self.show_selector)
        self.bloc_refente_selected = BlocSelected(data_type="refente", parent=self, callback=self.show_selector)
        self.bloc_bobines_selected = BlocSelected(data_type="bobine", parent=self, callback=self.show_selector)
        self.bloc_info = BlocInformation(parent=self, plan_prod=plan_prod)
        self.init_ui()

    def init_ui(self):
        master_vbox = QVBoxLayout()
        master_vbox.setContentsMargins(0, 0, 0, 0)
        vbox = QVBoxLayout()
        # self.titre_prod.setFixedHeight(30)
        # self.titre_prod.setStyleSheet(white_12_bold_label_stylesheet)
        # self.titre_prod.setContentsMargins(5, 0, 0, 0)
        # self.titre_prod.setMinimumWidth(800)
        # vbox.addWidget(self.titre_prod)
        vbox.addWidget(self.bloc_refente_selected)
        vbox.addWidget(self.bloc_papier_selected)
        vbox.addWidget(self.bloc_perfo_selected)
        vbox.addWidget(self.bloc_poly_selected)
        master_vbox.addWidget(self.bloc_info)
        master_vbox.addWidget(self.bloc_param_prod)
        master_vbox.addWidget(self.bloc_bobines_selected)
        master_vbox.addLayout(vbox)
        self.setLayout(master_vbox)

    def update_bloc_selected(self):
        self.bloc_poly_selected.update_widget()
        self.bloc_bobines_selected.update_widget()
        self.bloc_refente_selected.update_widget()
        self.bloc_perfo_selected.update_widget()
        self.bloc_papier_selected.update_widget()

    def handle_plan_prod_changed(self):
        self.update_bloc_selected()
        self.selector_manager.selector.update_widget()
        if filter_store.data_type != "bobine" or len(self.plan_prod.current_bobine_fille_store.bobines) == 0:
            self.selector_manager.hide()
        self.bloc_param_prod.update_label()
        self.bloc_info.update_widget()

    def handle_tours_plan_prod_changed(self):
        self.bloc_param_prod.update_label()
        self.bloc_info.update_widget()

    def show_selector(self):
        self.selector_manager.show()
