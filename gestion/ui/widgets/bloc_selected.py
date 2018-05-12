# !/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QVBoxLayout, QLabel

from commun.constants.colors import color_vert_moyen, color_blanc
from commun.ui.public.mondon_widget import MondonWidget
from commun.utils.layout import clear_layout
from gestion.ui.widgets.line_bobine import LineBobine
from gestion.ui.widgets.line_perfo import LinePerfo
from gestion.ui.widgets.line_refente import LineRefente
from gestion.ui.widgets.line_bobine_papier import LineBobinePapier
from gestion.ui.widgets.line_bobine_poly import LineBobinePoly
from gestion.stores.settings_store import settings_store_gestion
from gestion.stores.filter_store import filter_store


class BlocSelected(MondonWidget):

    def __init__(self, data_type, callback,  parent=None):
        super(BlocSelected, self).__init__(parent=parent)
        self.background_color = color_blanc
        self.data_type = data_type
        self.parent = parent
        self.callback = callback
        self.master_hbox = QVBoxLayout()
        self.update_widget()

    def init_ui(self):
        clear_layout(self.master_hbox)
        if self.data_type == "bobine":
            self.init_ui_bobine_fille(self.master_hbox)
        if self.data_type == "poly":
            self.init_ui_bobine_poly(self.master_hbox)
        if self.data_type == "papier":
            self.init_ui_bobine_papier(self.master_hbox)
        if self.data_type == "perfo":
            self.init_ui_perfo(self.master_hbox)
        if self.data_type == "refente":
            self.init_ui_refente(self.master_hbox)
        self.setLayout(self.master_hbox)

    def init_ui_bobine_fille(self, layout):
        if self.parent.plan_prod.bobines_filles_selected:
            for bobine in self.parent.plan_prod.bobines_filles_selected:
                line_bobine = LineBobine(parent=self, bobine=bobine)
                layout.addWidget(line_bobine)
        else:
            label = QLabel("Bobines filles")
            label.setFixedHeight(30)
            layout.addWidget(label)

    def init_ui_bobine_papier(self, layout):
        if self.parent.plan_prod.bobine_papier_selected:
            line_bobine_papier = LineBobinePapier(parent=self, bobine=self.parent.plan_prod.bobine_papier_selected)
            layout.addWidget(line_bobine_papier)
        else:
            label = QLabel("Bobine mère papier")
            label.setFixedHeight(30)
            layout.addWidget(label)
        self.setLayout(layout)

    def init_ui_bobine_poly(self, layout):
        if self.parent.plan_prod.bobine_poly_selected:
            line_bobine_poly = LineBobinePoly(parent=self, bobine=self.parent.plan_prod.bobine_poly_selected)
            layout.addWidget(line_bobine_poly)
        else:
            label = QLabel("Bobine mère poly")
            label.setFixedHeight(30)
            layout.addWidget(label)
        self.setLayout(layout)

    def init_ui_refente(self, layout):
        if self.parent.plan_prod.refente_selected:
            line_refente = LineRefente(parent=self,
                                       refente=self.parent.plan_prod.refente_selected,
                                       bobines=self.parent.plan_prod.bobines_filles_selected,
                                       ech=settings_store_gestion.ech)
            layout.addWidget(line_refente)
        else:
            label = QLabel("Refente")
            label.setFixedHeight(30)
            layout.addWidget(label)
        self.setLayout(layout)

    def init_ui_perfo(self, layout):
        if self.parent.plan_prod.perfo_selected:
            line_perfo = LinePerfo(parent=self,
                                   perfo=self.parent.plan_prod.perfo_selected,
                                   ech=settings_store_gestion.ech)
            layout.addWidget(line_perfo)
        else:
            label = QLabel("Campagne de perforation")
            label.setFixedHeight(30)
            layout.addWidget(label)
        self.setLayout(layout)

    def on_filter_changed(self):
        self.update_widget()

    def update_widget(self):
        if filter_store.data_type == self.data_type:
            self.set_border(color=color_vert_moyen, size=2)
        else:
            self.set_border(color=color_blanc)

        self.init_ui()
        self.update()

    def mouseDoubleClickEvent(self, e):
        filter_store.set_data_type(self.data_type)
        self.callback()
