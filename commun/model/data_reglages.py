# !/usr/bin/env python
# -*- coding: utf-8 -*-

from commun.model.data_reglage import DataReglage
from commun.stores.reglage_store import reglage_store


class DataReglages:

    def __init__(self, plan_prod):
        self.p = plan_prod
        self.last_p = None
        self.data_reglages = []
        self.init_data_reglage()
        self.time_aide = 0
        self.time_conducteur = 0
        self.time_reglage = 0

    def init_data_reglage(self):
        from commun.stores.reglage_store import reglage_store
        for reglage in reglage_store.reglages:
            self.add_reglage(reglage=reglage)

    def add_reglage(self, reglage):
        new_data_reglage = DataReglage(reglage=reglage)
        new_data_reglage.ON_DATA_CHANGED.connect(self.get_time)
        self.data_reglages.append(new_data_reglage)

    def set_last_plan_prod(self, last_plan_prod):
        self.last_p = last_plan_prod
        self.update_reglage()

    def get_time(self):
        self.time_aide = 0
        self.time_conducteur = 0
        for data_reglage in self.data_reglages:
            if data_reglage is None:
                continue
            if data_reglage.reglage.is_active(p=self.p, last_p=self.last_p) or data_reglage.reglage.is_optionnel():
                time = data_reglage.reglage.time * data_reglage.reglage.qty
                if data_reglage.check_box_conducteur and data_reglage.check_box_aide:
                    time = time / 2
                if data_reglage.check_box_conducteur:
                    self.time_conducteur += time
                if data_reglage.check_box_aide:
                    self.time_aide += time
        self.time_reglage = self.get_time_reglage()

    def get_time_reglage(self):
        time = 0
        for data_reglage in self.data_reglages:
            if data_reglage.reglage.cat == "CHAUFFE" and data_reglage.reglage.is_active(p=self.p, last_p=self.last_p):
                time = data_reglage.reglage.time if data_reglage.reglage.time > time else time
        time = self.time_aide if self.time_aide > time else time
        time = self.time_conducteur if self.time_conducteur > time else time
        return time

    def update_reglage(self):
        new_data_reglages = []
        for reglage in reglage_store.reglages:
            if reglage.is_active(p=self.p, last_p=self.last_p) or reglage.is_optionnel():
                data_reglage = self.get_data_reglage_from_id(id_reglage=reglage.id)
                if data_reglage:
                    new_data_reglages.append(data_reglage)
                else:
                    new_data_reglage = DataReglage(reglage=reglage)
                    new_data_reglages.append(new_data_reglage)
        self.data_reglages = new_data_reglages
        self.get_time()

    def get_data_reglage_from_id(self, id_reglage):
        for data_reglage in self.data_reglages:
            if data_reglage.reglage.id == id_reglage:
                return data_reglage
        return None

    def get_data_reglage_code(self):
        """
        Génère un code pour sauvegarde l'atribution des tâches entre conducteur et aide-conducteur
        X_BOOL_BOOL : code d'un réglage, avec X id du réglage, premier bool attribution à l'aide ocnducteur, deuxième
        bool attribution au conducteur
        :return: le code généré
        """
        code_data_reglages = ""
        for data_reglage in self.data_reglages:
            dr_id = data_reglage.reglage.id
            dr_aide = data_reglage.check_box_aide
            dr_conducteur = data_reglage.check_box_conducteur
            code_data_reglages += "{}_{}_{}_".format(dr_id, dr_aide, dr_conducteur)
        return code_data_reglages

    def update_data_reglage_from_code(self, code):
        index = 0
        if code:
            code_split = code.split("_")
            while code_split[index] != "":
                p_id = int(code_split[index])
                dr_aide = True if code_split[index+1] == "True" else False
                dr_conducteur = True if code_split[index+2] == "True" else False
                self.update_data_reglage(p_id=p_id, dr_aide=dr_aide, dr_conducteur=dr_conducteur)
                index += 3
        self.get_time()

    def update_data_reglage(self, p_id, dr_aide, dr_conducteur):
        data_reglage = self.get_data_reglage_from_id(id_reglage=p_id)
        data_reglage.check_box_conducteur = dr_conducteur
        data_reglage.check_box_aide = dr_aide
