# !/usr/bin/env python
# -*- coding: utf-8 -*-

# !/usr/bin/env python
# -*- coding: utf-8 -*-


from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt

from commun.ui.public.mondon_widget import MondonWidget
from commun.constants.colors import color_blanc
from commun.constants.stylesheets import white_12_bold_label_stylesheet

from gestion.ui.widgets.selector_manager import SelectorManager
from gestion.ui.widgets.bloc_param_prod import BlocParamProd
from gestion.ui.widgets.bloc_selected import BlocSelected
from gestion.ui.widgets.bloc_information import BlocInformation


class PlanProdCreator(MondonWidget):

    def __init__(self, plan_prod, parent=None):
        super(PlanProdCreator, self).__init__(parent=parent)
        self.set_background_color(color=color_blanc)
        self.plan_prod = plan_prod
        self.plan_prod.ON_CHANGED_SIGNAL.connect(self.handle_plan_prod_changed)
        self.plan_prod.ON_TOURS_CHANGED.connect(self.handle_tours_plan_prod_changed)
        self.selector_manager = SelectorManager(parent=self, plan_prod=self.plan_prod)
        self.bloc_param_prod = BlocParamProd(plan_prod=self.plan_prod, parent=self)
        self.titre_prod = QLabel("NOUVELLE PRODUCTION")
        self.bloc_poly_selected = BlocSelected(data_type="poly", parent=self)
        self.bloc_poly_selected.ON_CLICK_SIGNAL.connect(self.handle_click_on_bloc_selected)
        self.bloc_papier_selected = BlocSelected(data_type="papier", parent=self)
        self.bloc_papier_selected.ON_CLICK_SIGNAL.connect(self.handle_click_on_bloc_selected)
        self.bloc_perfo_selected = BlocSelected(data_type="perfo", parent=self)
        self.bloc_perfo_selected.ON_CLICK_SIGNAL.connect(self.handle_click_on_bloc_selected)
        self.bloc_refente_selected = BlocSelected(data_type="refente", parent=self)
        self.bloc_refente_selected.ON_CLICK_SIGNAL.connect(self.handle_click_on_bloc_selected)
        self.bloc_bobines_selected = BlocSelected(data_type="bobine", parent=self)
        self.bloc_bobines_selected.ON_CLICK_SIGNAL.connect(self.handle_click_on_bloc_selected)
        self.bloc_info = BlocInformation(parent=self, plan_prod=plan_prod)
        self.init_ui()

    def init_ui(self):
        master_vbox = QVBoxLayout()
        master_vbox.setContentsMargins(0, 0, 0, 0)

        hbox = QHBoxLayout()
        hbox.addWidget(self.selector_manager)
        vbox = QVBoxLayout()
        self.titre_prod.setFixedHeight(30)
        self.titre_prod.setStyleSheet(white_12_bold_label_stylesheet)
        self.titre_prod.setContentsMargins(5, 0, 0, 0)
        self.titre_prod.setMinimumWidth(800)
        vbox.addWidget(self.titre_prod)
        vbox.addWidget(self.bloc_poly_selected)
        vbox.addWidget(self.bloc_perfo_selected)
        vbox.addWidget(self.bloc_papier_selected)
        vbox.addWidget(self.bloc_refente_selected)
        hbox.addLayout(vbox)

        master_vbox.addWidget(self.bloc_param_prod)
        master_vbox.addLayout(hbox)
        master_vbox.addWidget(self.bloc_bobines_selected)
        master_vbox.addWidget(self.bloc_info)

        self.setLayout(master_vbox)

    def update_bloc_selected(self):
        self.bloc_poly_selected.update_widget()
        self.bloc_bobines_selected.update_widget()
        self.bloc_refente_selected.update_widget()
        self.bloc_perfo_selected.update_widget()
        self.bloc_papier_selected.update_widget()

    def update_selector(self):
        self.selector.update_widget()

    def handle_plan_prod_changed(self):
        self.update_bloc_selected()
        self.update_selector()
        self.bloc_param_prod.update_label()
        self.bloc_info.update_widget()

    def handle_tours_plan_prod_changed(self):
        self.bloc_param_prod.update_label()
        self.bloc_info.update_widget()

    def handle_click_on_bloc_selected(self, name_bloc):
        if self.selector_manager.bloc_focus == name_bloc:
            self.selector_manager.bloc_focus = "bobine"
        else:
            self.selector_manager.bloc_focus = name_bloc
        self.update_bloc_selected()
        self.update_selector()
        self.bloc_info.update_widget()

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Delete:
            self.plan_prod.del_item_selected(self.selector_manager.bloc_focus)
        if e.key() == Qt.Key_Enter:
            self.plan_prod.get_new_item_selected_from_store()
