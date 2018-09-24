# !/usr/bin/env python
# -*- coding: utf-8 -*-


from PyQt5.QtCore import QObject

from commun.lib.base_de_donnee import Database
from commun.model.plan_prod import PlanProd


class PlanProdStore(QObject):

    def __init__(self):
        super(PlanProdStore, self).__init__()
        self.plans_prods = []

    def get_plan_prod_from_database(self):
        data_plan_prod_on_data_base = Database.get_plan_prod()
        for data in data_plan_prod_on_data_base:
            start = data[1]
            new_plan_prod = PlanProd(last_plan_prod=self.get_last_plan_prod(start_plan_prod=start))
            new_plan_prod.update_from_data(data=data)
        # self.plans_prods = []
        # plan_prod_on_data_base = Database.get_plan_prod()
        # for data_plan_prod in plan_prod_on_data_base:
        #     new_plan_prod = PlanProd(start=data_plan_prod[1], p_id=data_plan_prod[0])
        #     new_plan_prod.bobine_papier_selected = self.get_bobine_papier(code=data_plan_prod[4])
        #     new_plan_prod.bobine_poly_selected = self.get_bobine_poly(code=data_plan_prod[7])
        #     new_plan_prod.refente_selected = self.get_refente(code=data_plan_prod[5])
        #     new_plan_prod.perfo_selected = self.get_perfo_from_refente(new_plan_prod.refente_selected)
        #     new_plan_prod.tours = data_plan_prod[2]
        #     new_plan_prod.longueur = data_plan_prod[3]
        #     new_plan_prod.encrier_1.set_color(data_plan_prod[8])
        #     new_plan_prod.encrier_2.set_color(data_plan_prod[9])
        #     new_plan_prod.encrier_3.set_color(data_plan_prod[10])
        #     self.add_bobine_to_plan_prod(plan_prod=new_plan_prod, code_bobines_filles=data_plan_prod[6])
        #     new_plan_prod.set_bobines_fille_selected_to_encriers()
        #     new_plan_prod.update_all_current_store()
        #     new_plan_prod.data_reglages.update_data_reglage_from_code(data_plan_prod[11])
        #     new_plan_prod.get_end()
        #     self.plans_prods.append(new_plan_prod)
        # self.sort_plans_prods()
        # self.update_plan_prod_from_last_plan_prod()

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


plan_prod_store = PlanProdStore()
