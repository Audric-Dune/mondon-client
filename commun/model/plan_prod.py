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

    def del_item_selected(self, data_type):
        if data_type == "bobine":
            self.bobine_fille_selected = []
        if data_type == "papier":
            self.bobine_papier_selected = None
        if data_type == "poly":
            self.bobine_poly_selected = None
        if data_type == "refente":
            self.refente_selected = None
        if data_type == "perfo":
            self.perfo_selected = None
        self.update_all_current_store()
        self.ON_CHANGED_SIGNAL.emit()

    def update_all_current_store(self):
        self.definied_plan_prod_param()
        self.filter_bobine_papier_from_plan_prod_param()
        self.filter_refente_from_plan_prod_param()
        self.filter_bobine_fille_from_plan_prod_param()
        self.filter_perfo_from_plan_prod_param()
        if self.bobine_fille_selected:
            self.filter_from_bobine_selected()
        self.filter_bobine_poly_from_bobine_papier()
        self.filter_perfo_from_refente()
        self.get_new_item_selected_from_store()

    def definied_plan_prod_param(self):
        self.definied_laize_plan_prod()
        self.definied_color_plan_prod()
        self.definied_gr_plan_prod()

    def definied_laize_plan_prod(self):
        self.laize_plan_prod = None
        if self.bobine_poly_selected:
            self.laize_plan_prod = int(self.bobine_poly_selected.laize)
        if self.bobine_papier_selected:
            self.laize_plan_prod = int(self.bobine_papier_selected.laize)
        if self.refente_selected:
            self.laize_plan_prod = int(self.refente_selected.laize)

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
            print(self.laize_plan_prod)
            print(refente.laize)
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

    def filter_perfo_from_plan_prod_param(self):
        if self.refente_selected:
            for perfo in self.current_perfo_store.perfos:
                if perfo.code == self.refente_selected.code_perfo:
                    self.perfo_selected = perfo

    def filter_from_bobine_selected(self):
        new_refente_store = self.filter_refente_from_bobine_fille()
        self.current_refente_store = new_refente_store

    def filter_refente_from_bobine_fille(self):
        new_refente_store = RefenteStore()
        for refente in self.current_refente_store.refentes:
            if self.refente_is_compatible_from_bobines_filles_selected(refente):
                new_refente_store.add_refente(refente)
        return new_refente_store

    def refente_is_compatible_from_bobines_filles_selected(self, refente):
        new_refente = refente
        for bobine in self.bobine_fille_selected:
            if self.refente_is_compatible_from_bobine(bobine, new_refente):
                new_refente = self.get_new_refente_with_bobine(new_refente, bobine)
                continue
            else:
                return False
        return True

    @staticmethod
    def refente_is_compatible_from_bobine(bobine, refente):
        counter_pose = 0
        for laize_refente in refente.laizes:
            if laize_refente and laize_refente == bobine.laize:
                counter_pose += 1
                if counter_pose >= bobine.pose:
                    return True
            else:
                counter_pose = 0
        return False

    @staticmethod
    def get_new_refente_with_bobine(refente, bobine):
        start_index = 0
        counter_pose = 0
        for laize_refente in refente.laizes:
            if laize_refente and laize_refente == bobine.laize:
                counter_pose += 1
                if counter_pose >= bobine.pose:
                    break
            else:
                counter_pose = 0
                start_index += 1
        from commun.model.refente import Refente
        new_refente = Refente()
        index_refente = 0
        for laize_refente in refente.laizes:
            if index_refente < start_index or index_refente >= start_index + bobine.pose:
                new_refente.laizes[index_refente] = laize_refente
            index_refente += 1
        return new_refente

    def filter_bobine_poly_from_bobine_papier(self):
        new_bobine_poly_store = BobinePolyStore()
        for bobine_poly in bobine_poly_store.bobines:
            if self.is_compatible_bobine_poly_from_bobine_papier_store(bobine_poly):
                new_bobine_poly_store.add_bobine(bobine_poly)
        self.current_bobine_poly_store = new_bobine_poly_store

    def is_compatible_bobine_poly_from_bobine_papier_store(self, bobine_poly):
        for bobine_papier in self.current_bobine_papier_store.bobines:
            if bobine_poly.laize == bobine_papier.laize:
                return True
        return False

    def filter_perfo_from_refente(self):
        new_perfo_store = PerfoStore()
        for perfo in perfo_store.perfos:
            if self.is_compatible_perfo_from_refente_store(perfo):
                new_perfo_store.add_perfo(perfo)
        self.current_perfo_store = new_perfo_store

    def is_compatible_perfo_from_refente_store(self, perfo):
        for refente in self.current_refente_store.refentes:
            if refente.code_perfo == perfo.code:
                return True
        return False

    def get_new_item_selected_from_store(self):
        if len(self.current_bobine_poly_store.bobines) == 1:
            self.bobine_poly_selected = self.current_bobine_poly_store.bobines[0]
        if len(self.current_perfo_store.perfos) == 1:
            self.perfo_selected = self.current_perfo_store.perfos[0]
        if len(self.current_bobine_papier_store.bobines) == 1:
            self.bobine_papier_selected = self.current_bobine_papier_store.bobines[0]
        if len(self.current_refente_store.refentes) == 1:
            self.refente_selected = self.current_refente_store.refentes[0]
