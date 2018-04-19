# !/usr/bin/env python
# -*- coding: utf-8 -*-

# !/usr/bin/env python
# -*- coding: utf-8 -*-


from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt

from commun.ui.public.mondon_widget import MondonWidget
from commun.constants.stylesheets import white_12_bold_label_stylesheet

from gestion.ui.widgets.selector import Selector
from gestion.ui.widgets.bloc_param_prod import BlocParamProd
from gestion.ui.widgets.bloc_selected import BlocSelected


class PlanProdCreator(MondonWidget):

    def __init__(self, plan_prod, parent=None):
        super(PlanProdCreator, self).__init__(parent=parent)
        self.plan_prod = plan_prod
        self.plan_prod.ON_CHANGED_SIGNAL.connect(self.handle_plan_prod_changed)
        self.plan_prod.ON_TOURS_CHANGED.connect(self.handle_tours_plan_prod_changed)
        self.bloc_focus = "bobine"
        self.selector = Selector(parent=self, plan_prod=self.plan_prod)
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
        self.init_ui()

    def init_ui(self):
        master_vbox = QVBoxLayout()
        master_vbox.setContentsMargins(0, 0, 0, 0)
        hbox = QHBoxLayout()
        hbox.addWidget(self.selector)
        hbox.addStretch(0)
        vbox = QVBoxLayout()
        self.titre_prod.setFixedHeight(30)
        self.titre_prod.setStyleSheet(white_12_bold_label_stylesheet)
        self.titre_prod.setContentsMargins(5, 0, 0, 0)
        vbox.addWidget(self.titre_prod)
        vbox.addWidget(self.bloc_poly_selected)
        vbox.addWidget(self.bloc_perfo_selected)
        vbox.addWidget(self.bloc_papier_selected)
        vbox.addWidget(self.bloc_refente_selected)
        vbox.addStretch(0)
        hbox.addLayout(vbox)
        master_vbox.addLayout(hbox)
        vbox = QVBoxLayout()
        vbox.addWidget(self.bloc_param_prod)
        vbox.addWidget(self.bloc_bobines_selected)
        master_vbox.addLayout(vbox)
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

    def handle_tours_plan_prod_changed(self):
        self.bloc_param_prod.update_label()

    def handle_click_on_bloc_selected(self, name_bloc):
        if self.bloc_focus == name_bloc:
            self.bloc_focus = "bobine"
        else:
            self.bloc_focus = name_bloc
        self.update_bloc_selected()
        self.update_selector()

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Delete:
            self.plan_prod.del_item_selected(self.bloc_focus)
        if e.key() == Qt.Key_Enter:
            self.plan_prod.get_new_item_selected_from_store()
