# !/usr/bin/env python
# -*- coding: utf-8 -*-


from PyQt5.QtCore import QObject

from commun.lib.base_de_donnee import Database
from commun.stores.bobine_papier_store import bobine_papier_store
from commun.stores.bobine_poly_store import bobine_poly_store
from commun.stores.refente_store import refente_store
from commun.stores.perfo_store import perfo_store
from commun.stores.bobine_fille_store import bobine_fille_store
from commun.model.plan_prod import PlanProd
from commun.model.bobine_fille_selected import BobineFilleSelected


class PlanProdStore(QObject):

    def __init__(self):
        super(PlanProdStore, self).__init__()
        self.plans_prods = []

    def get_plan_prod_from_database(self):
        self.plans_prods = []
        plan_prod_on_data_base = Database.get_plan_prod()
        for data_plan_prod in plan_prod_on_data_base:
            new_plan_prod = PlanProd(start=data_plan_prod[1], p_id=data_plan_prod[0])
            new_plan_prod.bobine_papier_selected = self.get_bobine_papier(code=data_plan_prod[4])
            new_plan_prod.bobine_poly_selected = self.get_bobine_poly(code=data_plan_prod[7])
            new_plan_prod.refente_selected = self.get_refente(code=data_plan_prod[5])
            new_plan_prod.perfo_selected = self.get_perfo_from_refente(new_plan_prod.refente_selected)
            new_plan_prod.tours = data_plan_prod[2]
            new_plan_prod.longueur = data_plan_prod[3]
            new_plan_prod.encrier_1.set_color(data_plan_prod[8])
            new_plan_prod.encrier_2.set_color(data_plan_prod[9])
            new_plan_prod.encrier_3.set_color(data_plan_prod[10])
            self.add_bobine_to_plan_prod(plan_prod=new_plan_prod, code_bobines_filles=data_plan_prod[6])
            new_plan_prod.get_end()
            new_plan_prod.set_bobines_fille_selected_to_encriers()
            new_plan_prod.update_all_current_store()
            self.plans_prods.append(new_plan_prod)
        self.sort_plans_prods()
        self.update_plan_prod_from_last_plan_prod()

    def update_plan_prod_from_last_plan_prod(self):
        for plan_prod in self.plans_prods:
            plan_prod.get_last_plan_prod()
            plan_prod.set_color_encrier_from_last_plan_prod()

    def sort_plans_prods(self):
        self.plans_prods = sorted(self.plans_prods, key=lambda b: b.get_start(), reverse=False)

    def get_last_plan_prod(self, start_plan_prod):
        last_plan_prod = None
        for plan_prod in self.plans_prods:
            if plan_prod is None:
                continue
            if plan_prod.start < start_plan_prod:
                last_plan_prod = plan_prod
        return last_plan_prod

    @staticmethod
    def get_bobine_papier(code):
        for bobine in bobine_papier_store.bobines:
            if bobine.code == code:
                return bobine

    @staticmethod
    def get_bobine_poly(code):
        for bobine in bobine_poly_store.bobines:
            if bobine.code == code:
                return bobine

    @staticmethod
    def get_refente(code):
        for refente in refente_store.refentes:
            if refente.code == code:
                return refente

    @staticmethod
    def get_perfo_from_refente(refente):
        for perfo in perfo_store.perfos:
            if perfo.code == refente.code_perfo:
                return perfo

    @staticmethod
    def add_bobine_to_plan_prod(code_bobines_filles, plan_prod):
        code_bobines_filles_split = code_bobines_filles.split("_")
        index = 0
        while True:
            if code_bobines_filles_split[index]:
                bobine = bobine_fille_store.get_bobine(code_bobines_filles_split[index])
                bobine_selected = BobineFilleSelected(bobine=bobine,
                                                      pose=int(code_bobines_filles_split[index+1]),
                                                      index=int(code_bobines_filles_split[index+2]))
                plan_prod.bobines_filles_selected.append(bobine_selected)
                index += 3
            else:
                break


plan_prod_store = PlanProdStore()
