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
        self.init_refente_store()
        self.perfo_store = PerfoStore()
        self.init_perfo_store()
        self.bobine_fille_store = BobineFilleStore()
        self.init_bobine_fille_store()
        self.bobine_papier_store = BobinePapierStore()
        self.init_bobine_papier_store()
        self.bobine_poly_store = BobinePolyStore()
        self.init_bobine_poly_store()
        self.refente_selected = None
        self.perfo_selected = None
        self.bobine_fille_selected = []
        self.bobine_papier_selected = None
        self.bobine_poly_selected = None

    def init_bobine_fille_store(self):
        from commun.stores.bobine_fille_store import bobine_fille_store
        for bobine in bobine_fille_store.bobines:
            self.bobine_fille_store.add_bobine(bobine)

    def init_refente_store(self):
        from commun.stores.refente_store import refente_store
        for refente in refente_store.refentes:
            self.refente_store.add_refente(refente)

    def init_perfo_store(self):
        from commun.stores.perfo_store import perfo_store
        for perfo in perfo_store.perfos:
            self.perfo_store.add_perfo(perfo)

    def init_bobine_papier_store(self):
        from commun.stores.bobine_papier_store import bobine_papier_store
        for bobine in bobine_papier_store.bobines:
            self.bobine_papier_store.add_bobine(bobine)

    def init_bobine_poly_store(self):
        from commun.stores.bobine_poly_store import bobine_poly_store
        for bobine in bobine_poly_store.bobines:
            self.bobine_poly_store.add_bobine(bobine)
