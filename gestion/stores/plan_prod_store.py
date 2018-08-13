# !/usr/bin/env python
# -*- coding: utf-8 -*-


from PyQt5.QtCore import QObject

from commun.lib.base_de_donnee import Database
from commun.utils.timestamp import timestamp_at_day_ago
from commun.stores.bobine_papier_store import bobine_papier_store
from commun.stores.bobine_poly_store import bobine_poly_store
from commun.stores.refente_store import refente_store
from commun.stores.bobine_fille_store import bobine_fille_store
from commun.model.plan_prod import PlanProd
from commun.model.bobine_fille_selected import BobineFilleSelected

from gestion.stores.settings_store import settings_store_gestion


class PlanProdStore(QObject):

    def __init__(self):
        super(PlanProdStore, self).__init__()
        settings_store_gestion.SETTINGS_CHANGED_SIGNAL.connect(self.get_plan_prod_from_database)
        self.plan_prod_on_data_base = None
        self.plans_prods = []

    def get_plan_prod_from_database(self):
        self.plans_prods = []
        plan_prod_on_data_base = Database.get_plan_prod()
        day_ago = settings_store_gestion.day_ago if settings_store_gestion.day_ago > 0 else 0
        start_ts = timestamp_at_day_ago(day_ago)
        for plan_prod in plan_prod_on_data_base:
            if start_ts < plan_prod[1]:
                new_plan_prod = PlanProd(start=plan_prod[1], p_id=plan_prod[0])
                new_plan_prod.bobine_papier_selected = self.get_bobine_papier(code=plan_prod[4])
                new_plan_prod.bobine_poly_selected = self.get_bobine_poly(code=plan_prod[7])
                new_plan_prod.refente_selected = self.get_refente(code=plan_prod[5])
                new_plan_prod.tours = plan_prod[2]
                new_plan_prod.longueur = plan_prod[3]
                new_plan_prod.encrier_1.set_color(plan_prod[8])
                new_plan_prod.encrier_2.set_color(plan_prod[9])
                new_plan_prod.encrier_3.set_color(plan_prod[10])
                new_plan_prod.get_end()
                self.add_bobine_to_plan_prod(plan_prod=new_plan_prod, code_bobines_filles=plan_prod[6])
                new_plan_prod.update_all_current_store()
                new_plan_prod.get_new_item_selected_from_store()
                new_plan_prod.set_bobines_fille_selected_to_encriers()
                self.plans_prods.append(new_plan_prod)
        self.sort_plans_prods()

    def sort_plans_prods(self):
        self.plans_prods = sorted(self.plans_prods, key=lambda b: b.get_start(), reverse=False)

    def get_last_plan_prod(self, start_plan_prod):
        self.get_plan_prod_from_database()
        last_plan_prod = None
        for plan_prod in self.plans_prods:
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
    def add_bobine_to_plan_prod(code_bobines_filles, plan_prod):
        code_bobines_filles_split = code_bobines_filles.split("_")
        bobine_fille = None
        pose = None
        for string in code_bobines_filles_split:
            if string and string[0] == "B":
                def get_bobine_fille(code):
                    for bobine in bobine_fille_store.bobines:
                        if bobine.code == code:
                            return bobine
                bobine_fille = get_bobine_fille(code=string)
            try:
                pose = int(string)
            except ValueError:
                pass
            if bobine_fille and pose is not None:
                new_bobine_fille = BobineFilleSelected(bobine=bobine_fille, index=None, pose=pose)
                plan_prod.bobines_filles_selected.append(new_bobine_fille)
                bobine_fille = None
                pose = None


plan_prod_store = PlanProdStore()
