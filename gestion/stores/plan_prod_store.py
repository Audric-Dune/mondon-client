# !/usr/bin/env python
# -*- coding: utf-8 -*-


from PyQt5.QtCore import pyqtSignal, QObject

from commun.lib.base_de_donnee import Database
from commun.stores.bobine_papier_store import bobine_papier_store
from commun.stores.refente_store import refente_store
from commun.stores.bobine_fille_store import bobine_fille_store
from commun.model.plan_prod import PlanProd


class PlanProdStore(QObject):
    SETTINGS_CHANGED_SIGNAL = pyqtSignal()

    def __init__(self):
        super(PlanProdStore, self).__init__()
        self.plan_prod_on_data_base = None
        self.plans_prods = []
        self.get_plan_prod_from_database()

    def get_plan_prod_from_database(self):
        plan_prod_on_data_base = Database.get_plan_prod()
        for plan_prod in plan_prod_on_data_base:
            new_plan_prod = PlanProd(plan_prod[1])
            new_plan_prod.bobine_papier_selected = self.get_bobine_papier(code=plan_prod[4])
            new_plan_prod.refente_selected = self.get_refente(code=plan_prod[5])
            new_plan_prod.tours = plan_prod[2]
            new_plan_prod.longueur = plan_prod[3]
            new_plan_prod.get_end()
            self.add_bobine_to_plan_prod(plan_prod=new_plan_prod, code_bobines_filles=plan_prod[6])
            new_plan_prod.update_all_current_store()
            new_plan_prod.get_new_item_selected_from_store()
            self.plans_prods.append(new_plan_prod)

    @staticmethod
    def get_bobine_papier(code):
        for bobine in bobine_papier_store.bobines:
            if bobine.code == code:
                return bobine

    @staticmethod
    def get_refente(code):
        for refente in refente_store.refentes:
            if refente.code == code:
                return refente

    def add_bobine_to_plan_prod(self, code_bobines_filles, plan_prod):
        code_bobines_filles_split = code_bobines_filles.split("_")
        for string in code_bobines_filles_split:
            if string and string[0] == "B":
                plan_prod.bobines_filles_selected.append(self.get_bobine_fille(code=string))

    @staticmethod
    def get_bobine_fille(code):
        for bobine in bobine_fille_store.bobines:
            if bobine.code == code:
                return bobine


plan_prod_store = PlanProdStore()