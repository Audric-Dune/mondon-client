# !/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtCore import pyqtSignal

from commun.stores.refente_store import RefenteStore
from commun.stores.perfo_store import PerfoStore
from commun.stores.bobine_fille_store import BobineFilleStore
from commun.stores.bobine_papier_store import BobinePapierStore
from commun.stores.bobine_poly_store import BobinePolyStore
from commun.ui.public.mondon_widget import MondonWidget
from commun.stores.bobine_papier_store import bobine_papier_store
from commun.stores.bobine_fille_store import bobine_fille_store
from commun.stores.perfo_store import perfo_store
from commun.stores.refente_store import refente_store
from commun.stores.bobine_poly_store import bobine_poly_store


class PlanProd(MondonWidget):
    ON_CHANGED_SIGNAL = pyqtSignal()

    def __init__(self, parent=None):
        super(PlanProd, self).__init__(parent=parent)
        self.current_refente_store = RefenteStore()
        self.init_refente_store()
        self.current_perfo_store = PerfoStore()
        self.init_perfo_store()
        self.current_bobine_fille_store = BobineFilleStore()
        self.init_bobine_fille_store()
        self.current_bobine_papier_store = BobinePapierStore()
        self.init_bobine_papier_store()
        self.current_bobine_poly_store = BobinePolyStore()
        self.init_bobine_poly_store()
        self.refente_selected = None
        self.perfo_selected = None
        self.bobine_fille_selected = []
        self.bobine_papier_selected = None
        self.bobine_poly_selected = None
        self.laize_plan_prod = None
        self.color_plan_prod = None
        self.gr_plan_prod = None

    def init_bobine_fille_store(self):
        for bobine in bobine_fille_store.bobines:
            self.current_bobine_fille_store.add_bobine(bobine)

    def init_refente_store(self):
        for refente in refente_store.refentes:
            self.current_refente_store.add_refente(refente)

    def init_perfo_store(self):
        for perfo in perfo_store.perfos:
            self.current_perfo_store.add_perfo(perfo)

    def init_bobine_papier_store(self):
        for bobine in bobine_papier_store.bobines:
            self.current_bobine_papier_store.add_bobine(bobine)

    def init_bobine_poly_store(self):
        for bobine in bobine_poly_store.bobines:
            self.current_bobine_poly_store.add_bobine(bobine)

    def add_bobine_selected(self, bobine):
        self.bobine_fille_selected.append(bobine)
        self.update_all_current_store()
        self.ON_CHANGED_SIGNAL.emit()

    def add_refente_selected(self, refente):
        self.refente_selected = refente
        self.update_all_current_store()
        self.ON_CHANGED_SIGNAL.emit()

    def add_perfo_selected(self, perfo):
        self.perfo_selected = perfo
        self.update_all_current_store()
        self.ON_CHANGED_SIGNAL.emit()

    def add_bobine_papier_selected(self, bobine):
        self.bobine_papier_selected = bobine
        self.update_all_current_store()
        self.ON_CHANGED_SIGNAL.emit()

    def add_bobine_poly_selected(self, bobine):
        self.bobine_poly_selected = bobine
        self.update_all_current_store()
        self.ON_CHANGED_SIGNAL.emit()

    def update_all_current_store(self):
        self.definied_plan_prod_param()
        self.filter_bobine_papier_from_plan_prod_param()
        self.filter_refente_from_plan_prod_param()
        self.filter_bobine_fille_from_plan_prod_param()
        self.get_new_item_selected_from_store()

    def definied_plan_prod_param(self):
        self.definied_laize_plan_prod()
        self.definied_color_plan_prod()
        self.definied_gr_plan_prod()

    def definied_laize_plan_prod(self):
        self.laize_plan_prod = None
        if self.bobine_poly_selected:
            self.laize_plan_prod = self.bobine_poly_selected.laize
        if self.bobine_papier_selected:
            self.laize_plan_prod = self.bobine_papier_selected.laize
        if self.refente_selected:
            self.laize_plan_prod = self.refente_selected.laize

    def definied_color_plan_prod(self):
        self.color_plan_prod = None
        if self.bobine_papier_selected:
            self.color_plan_prod = self.bobine_papier_selected.color
        if self.bobine_fille_selected:
            self.color_plan_prod = self.bobine_fille_selected[0].color

    def definied_gr_plan_prod(self):
        self.gr_plan_prod = None
        if self.bobine_papier_selected:
            self.gr_plan_prod = self.bobine_papier_selected.gr
        if self.bobine_fille_selected:
            self.gr_plan_prod = self.bobine_fille_selected[0].gr

    def filter_bobine_papier_from_plan_prod_param(self):
        new_bobine_papier_store = BobinePapierStore()
        for bobine in bobine_papier_store.bobines:
            if self.color_plan_prod and bobine.color != self.color_plan_prod:
                continue
            if self.gr_plan_prod and bobine.gr != self.gr_plan_prod:
                continue
            if self.laize_plan_prod and bobine.laize != self.laize_plan_prod:
                continue
            new_bobine_papier_store.add_bobine(bobine)
        self.current_bobine_papier_store = new_bobine_papier_store

    def filter_refente_from_plan_prod_param(self):
        new_refente_store = RefenteStore()
        for refente in refente_store.refentes:
            if self.laize_plan_prod and refente.laize != self.laize_plan_prod:
                continue
            if self.perfo_selected and refente.code_perfo != self.perfo_selected.code:
                continue
            new_refente_store.add_refente(refente)
        self.current_refente_store = new_refente_store

    def filter_bobine_fille_from_plan_prod_param(self):
        new_bobine_fille_store = BobineFilleStore()
        for bobine in bobine_fille_store.bobines:
            if self.color_plan_prod and bobine.color != self.color_plan_prod:
                continue
            if self.gr_plan_prod and bobine.gr != self.gr_plan_prod:
                continue
            new_bobine_fille_store.add_bobine(bobine)
        self.current_bobine_fille_store = new_bobine_fille_store

    def get_new_item_selected_from_store(self):
        if len(self.current_bobine_poly_store.bobines) == 1:
            self.bobine_poly_selected = self.current_bobine_poly_store.bobines[0]
        if len(self.current_perfo_store.perfos) == 1:
            self.perfo_selected = self.current_perfo_store.perfos[0]
        if len(self.current_bobine_papier_store.bobines) == 1:
            self.bobine_papier_selected = self.current_bobine_papier_store.bobines[0]
        if len(self.current_refente_store.refentes) == 1:
            self.refente_selected = self.current_refente_store.refentes[0]
