# !/usr/bin/env python
# -*- coding: utf-8 -*-

from commun.stores.refente_store import RefenteStore
from commun.stores.perfo_store import PerfoStore
from commun.stores.bobine_fille_store import BobineFilleStore
from commun.stores.bobine_papier_store import BobinePapierStore
from commun.stores.bobine_poly_store import BobinePolyStore
from commun.ui.public.mondon_widget import MondonWidget


class PlanProd(MondonWidget):

    def __init__(self, parent=None):
        super(PlanProd, self).__init__(parent=parent)
        self.refente_store = RefenteStore()
        self.perfo_store = PerfoStore()
        self.bobine_fille_store = BobineFilleStore()
        self.init_bobine_fille_store()
        self.bobine_papier_store = BobinePapierStore()
        self.bobine_poly_store = BobinePolyStore()
        self.refente_selected = None
        self.perfo_selected = None
        self.bobine_fille_selected = []
        self.bobine_papier_selected = None
        self.bobine_poly_selected = None

    def init_bobine_fille_store(self):
        from commun.stores.bobine_fille_store import bobine_fille_store
        for bobine in bobine_fille_store.bobines:
            self.bobine_fille_store.add_bobine(bobine)

    def update_bobine_fille_store(self):
        new_bobine_fille_store = BobineFilleStore()
        current_color = self.bobine_fille_selected[0].color
        for bobine in self.bobine_fille_store.bobines:
            if bobine.color == current_color:
                new_bobine_fille_store.add_bobine(bobine)
            else:
                continue
        self.bobine_fille_store = new_bobine_fille_store

    def add_bobine_fille(self, bobine_code):
        bobine = self.get_bobine_with_code(bobine_code)
        self.bobine_fille_selected.append(bobine)
        self.update_bobine_fille_store()

    @staticmethod
    def get_bobine_with_code(bobine_code):
        from commun.stores.bobine_fille_store import bobine_fille_store
        for bobine in bobine_fille_store.bobines:
            if bobine.code == bobine_code:
                return bobine
