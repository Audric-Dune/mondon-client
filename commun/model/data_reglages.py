# !/usr/bin/env python
# -*- coding: utf-8 -*-

from commun.model.data_reglage import DataReglage
from commun.stores.reglage_store import reglage_store


class DataReglages:

    def __init__(self, plan_prod):
        self.p = plan_prod
        self.last_p = None
        self.data_reglages = []

    def add_reglage(self, reglage):
        new_data_reglage = DataReglage(reglage=reglage)
        self.data_reglages.append(new_data_reglage)

    def set_last_plan_prod(self, last_plan_prod):
        self.last_p = last_plan_prod
        self.update_reglage()

    def update_reglage(self):
        new_data_reglages = []
        for reglage in reglage_store.reglages:
            if reglage.is_active(p=self.p, last_p=self.last_p):
                data_reglage = self.get_data_reglage_from_id(id_reglage=reglage.id)
                if data_reglage:
                    new_data_reglages.append(data_reglage)
                else:
                    new_data_reglage = DataReglage(reglage=reglage)
                    new_data_reglages.append(new_data_reglage)
        self.data_reglages = new_data_reglages

    def get_data_reglage_from_id(self, id_reglage):
        for data_reglage in self.data_reglages:
            if data_reglage.reglage.id == id_reglage:
                return data_reglage
        return None
