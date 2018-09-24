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
            new_plan_prod = PlanProd(last_plan_prod=self.get_last_plan_prod(start_plan_prod=start), data=data)
            self.plans_prods.append(new_plan_prod)
        self.sort_plans_prods()

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
