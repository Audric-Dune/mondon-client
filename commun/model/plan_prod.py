# !/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtCore import pyqtSignal

from commun.stores.refente_store import RefenteStore
from commun.stores.perfo_store import PerfoStore
from commun.stores.bobine_fille_store import BobineFilleStore
from commun.stores.bobine_papier_store import BobinePapierStore
from commun.stores.bobine_poly_store import BobinePolyStore
from commun.ui.public.mondon_widget import MondonWidget


class PlanProd(MondonWidget):
    ON_CHANGED_SIGNAL = pyqtSignal()

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

    def add_bobine_selected(self, bobine):
        self.bobine_fille_selected.append(bobine)
        self.update_refente_store()
        self.ON_CHANGED_SIGNAL.emit()

    def update_refente_store(self):
        for bobine in self.bobine_fille_selected:
            self.get_refente_from_bobine(bobine)

    def get_refente_from_bobine(self, bobine):
        new_refente_store = RefenteStore()
        for refente in self.refente_store.refentes:
            if self.is_compatible_refente_from_bobine(refente, bobine):
                new_refente_store.add_refente(refente)
        self.refente_store = new_refente_store

    def is_compatible_refente_from_bobine(self, refente, bobine):
        laize_bobine = bobine.laize
        pose_bobine = bobine.pose
        color_bobine = bobine.color
        laize_bobine_mere_refente = self.get_laize_bobine_mere_from_refente(refente)
        if not self.compatible_bobine_mere_from_refente(color_bobine, laize_bobine_mere_refente):
            return False
        if pose_bobine == 0:
            return True
        count_pose = 0
        for laize_refente in refente.laizes:
            if laize_refente == laize_bobine:
                count_pose += 1
                if count_pose == pose_bobine:
                    return True
            elif not laize_refente:
                return False
            else:
                count_pose = 0
        return False

    @staticmethod
    def get_laize_bobine_mere_from_refente(refente):
        laize_bobine_mere_refente = 0
        for laize in refente.laizes:
            if laize:
                laize_bobine_mere_refente += laize
        return laize_bobine_mere_refente

    def compatible_bobine_mere_from_refente(self, color, laize):
        for bobine in self.bobine_papier_store.bobines:
            if bobine.color == color and bobine.laize == laize:
                return True
        return False
