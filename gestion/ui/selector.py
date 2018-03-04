# !/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QScrollArea, QVBoxLayout, QWidget
from commun.constants.colors import color_bleu_gris
from commun.constants.stylesheets import scroll_bar_stylesheet
from commun.ui.public.mondon_widget import MondonWidget
from commun.utils.layout import clear_layout
from gestion.ui.line_bobine import LineBobine
from gestion.ui.line_refente import LineRefente
from gestion.ui.line_perfo import LinePerfo
from gestion.ui.line_bobine_papier import LineBobinePapier
from gestion.ui.line_bobine_poly import LineBobinePoly


class Selector(MondonWidget):

    def __init__(self, plan_prod, parent=None):
        super(Selector, self).__init__(parent=parent)
        self.plan_prod = plan_prod
        self.parent = parent
        self.current_focus = "perfo"
        self.background_color = color_bleu_gris
        self.master_vbox = QVBoxLayout()
        self.vbox = QVBoxLayout()
        self.scroll_bar = QScrollArea(parent=self)
        self.content_scrollbar = QWidget(parent=self.scroll_bar)
        self.init_widget()
        self.update_widget()

    def init_widget(self):
        self.content_scrollbar.setLayout(self.vbox)
        self.scroll_bar.setWidget(self.content_scrollbar)
        self.scroll_bar.setStyleSheet(scroll_bar_stylesheet)
        self.scroll_bar.setWidgetResizable(True)
        self.master_vbox.addWidget(self.scroll_bar)
        self.setLayout(self.master_vbox)

    def update_widget(self):
        self.current_focus = self.parent.bloc_focus
        clear_layout(self.vbox)
        if self.current_focus == "bobine" or not self.current_focus:
            for bobine in self.plan_prod.current_bobine_fille_store.bobines:
                line_bobine = LineBobine(parent=self, bobine=bobine)
                line_bobine.ON_DBCLICK_SIGNAL.connect(self.handle_selected_bobine)
                line_bobine.setFixedHeight(20)
                self.vbox.addWidget(line_bobine)
        if self.current_focus == "refente":
            for refente in self.plan_prod.current_refente_store.refentes:
                line_refente = LineRefente(parent=self, refente=refente)
                line_refente.ON_DBCLICK_SIGNAL.connect(self.handle_selected_refente)
                self.vbox.addWidget(line_refente)
        if self.current_focus == "perfo":
            for perfo in self.plan_prod.current_perfo_store.perfos:
                line_perfo = LinePerfo(parent=self, perfo=perfo)
                line_perfo.ON_DBCLICK_SIGNAL.connect(self.handle_selected_perfo)
                self.vbox.addWidget(line_perfo)
        if self.current_focus == "papier":
            for bobine in self.plan_prod.current_bobine_papier_store.bobines:
                line_bobine_papier = LineBobinePapier(parent=self, bobine=bobine)
                line_bobine_papier.ON_DBCLICK_SIGNAL.connect(self.handle_selected_bobine_papier)
                line_bobine_papier.setFixedHeight(20)
                self.vbox.addWidget(line_bobine_papier)
        if self.current_focus == "poly":
            for bobine in self.plan_prod.current_bobine_poly_store.bobines:
                line_bobine_poly = LineBobinePoly(parent=self, bobine=bobine)
                line_bobine_poly.ON_DBCLICK_SIGNAL.connect(self.handle_selected_bobine_poly)
                line_bobine_poly.setFixedHeight(20)
                self.vbox.addWidget(line_bobine_poly)
        # if self.vbox.count() ==0:
        #   ajout label : "Aucun item disponible dans la configuration actuelle"
        self.vbox.addStretch(0)
        self.update()

    def handle_selected_bobine(self, bobine):
        self.plan_prod.add_bobine_selected(bobine)

    def handle_selected_refente(self, refente):
        self.plan_prod.add_refente_selected(refente)

    def handle_selected_perfo(self, perfo):
        self.plan_prod.add_perfo_selected(perfo)

    def handle_selected_bobine_papier(self, bobine):
        self.plan_prod.add_bobine_papier_selected(bobine)

    def handle_selected_bobine_poly(self, bobine):
        self.plan_prod.add_bobine_poly_selected(bobine)
