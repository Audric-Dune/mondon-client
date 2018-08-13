# !/usr/bin/env python
# -*- coding: utf-8 -*-


from PyQt5.QtCore import pyqtSignal, QObject

from commun.constants.param import PERCENT_PROD_THEROIQUE_MAXI
from commun.utils.timestamp import timestamp_to_hour_little
from commun.utils import filter
from commun.model.refente import Refente
from commun.model.contraintes import Contrainte
from commun.model.bobine_fille_valid import BobineFilleValid
from commun.model.encrier import Encrier
from commun.stores.refente_store import RefenteStore
from commun.stores.perfo_store import PerfoStore
from commun.stores.bobine_fille_store import BobineFilleStore
from commun.stores.bobine_papier_store import BobinePapierStore
from commun.stores.bobine_poly_store import BobinePolyStore
from commun.stores.bobine_papier_store import bobine_papier_store
from commun.stores.bobine_fille_store import bobine_fille_store
from commun.stores.perfo_store import perfo_store
from commun.stores.refente_store import refente_store
from commun.stores.bobine_poly_store import bobine_poly_store


class PlanProd(QObject):
    ON_CHANGED_SIGNAL = pyqtSignal()
    ON_TOURS_CHANGED = pyqtSignal()

    def __init__(self, start, parent=None, p_id=None):
        super(PlanProd, self).__init__(parent=parent)
        self.p_id = p_id
        self.start = start
        self.end = start
        self.tours = 12
        self.encrier_1 = Encrier()
        self.encrier_2 = Encrier()
        self.encrier_3 = Encrier()
        self.encriers = [self.encrier_1, self.encrier_2, self.encrier_3]
        self.longueur = None
        self.current_refente_store = RefenteStore()
        self.current_perfo_store = PerfoStore()
        self.current_bobine_fille_store = BobineFilleStore()
        self.current_bobine_papier_store = BobinePapierStore()
        self.current_bobine_poly_store = BobinePolyStore()
        self.init_current_store()
        self.refente_selected = None
        self.perfo_selected = None
        self.bobines_filles_selected = []
        self.bobine_papier_selected = None
        self.bobine_poly_selected = None
        if p_id is None:
            self.set_color_encrier_from_last_plan_prod()

    def __repr__(self):
        return "{}-{}, {}".format(timestamp_to_hour_little(self.start),
                                  timestamp_to_hour_little(self.end),
                                  self.bobine_papier_selected.color)

    def set_index_to_bobines_filles_selected(self):
        index = 0
        for bobine in self.bobines_filles_selected:
            bobine.index = index
            print(bobine)
            index += bobine.pose

    def set_refente_encrier(self):
        for encrier in self.encriers:
            encrier.refente = self.refente_selected

    def set_color_encrier_from_last_plan_prod(self):
        from gestion.stores.plan_prod_store import plan_prod_store
        last_plan_prod = plan_prod_store.get_last_plan_prod(start_plan_prod=self.start)
        if last_plan_prod:
            self.encrier_1.color_last_prod = last_plan_prod.encrier_1.color
            self.encrier_2.color_last_prod = last_plan_prod.encrier_2.color
            self.encrier_3.color_last_prod = last_plan_prod.encrier_3.color

    def set_color_encrier_from_bobine(self, color):

        def color_available_in_encrier(encriers, p_color):
            for encrier in encriers:
                if encrier.color == p_color:
                    return True
            return False

        def get_free_encrier(encriers):
            for encrier in encriers:
                if encrier.color_last_prod is None and encrier.color is None:
                    return encrier
            for encrier in encriers:
                if encrier.color is None:
                    return encrier
            return False

        if color_available_in_encrier(encriers=self.encriers, p_color=color):
            pass
        else:
            free_encrier = get_free_encrier(encriers=self.encriers)
            free_encrier.set_color(color)

    def set_bobines_fille_selected_to_encriers(self):
        self.set_index_to_bobines_filles_selected()
        self.encrier_1.bobines_filles_selected = self.bobines_filles_selected
        self.encrier_2.bobines_filles_selected = self.bobines_filles_selected
        self.encrier_3.bobines_filles_selected = self.bobines_filles_selected

    def update_encrier(self, bobine):
        self.set_bobines_fille_selected_to_encriers()
        if bobine.colors_cliche is not None:
            for color in bobine.colors_cliche:
                self.set_color_encrier_from_bobine(color)

    def get_plan_prod_param(self, plan_prod):
        self.start = plan_prod.start
        self.end = plan_prod.end
        self.tours = plan_prod.tours
        self.longueur = plan_prod.longueur
        self.refente_selected = plan_prod.refente_selected
        self.bobines_filles_selected = plan_prod.bobines_filles_selected
        self.bobine_papier_selected = plan_prod.bobine_papier_selected
        self.bobine_poly_selected = plan_prod.bobine_poly_selected

    def get_start(self):
        return self.start

    def is_valid(self):
        if not self.tours:
            return False
        if not self.is_valid_tours():
            return False
        if not self.is_completed():
            return False
        return True

    def is_completed(self):
        if not self.bobine_poly_selected:
            return False
        if not self.bobine_papier_selected:
            return False
        if not self.perfo_selected:
            return False
        if not self.refente_selected:
            return False
        if not self.refente_is_completed():
            return False
        return True

    def is_valid_tours(self):
        end_day_ts = self.get_end_day()
        if self.end > end_day_ts:
            return False
        return True

    def get_end_day(self):
        from gestion.stores.settings_store import settings_store_gestion
        return settings_store_gestion.get_max_end(self.start)

    def get_max_tour(self, end=None):
        if end is None:
            end = self.get_end_day()
        max_prod_ts = end - self.start
        max_tour = (max_prod_ts*3/(PERCENT_PROD_THEROIQUE_MAXI/100)/self.longueur)
        return int(max_tour)

    def refente_is_completed(self):
        new_refente = self.refente_selected
        if not self.bobines_filles_selected or not new_refente:
            return False
        for bobine in self.bobines_filles_selected:
            new_refente = self.get_new_refente_with_bobine(refente=new_refente, bobine=bobine)
        return self.refente_is_complete(refente=new_refente)

    @staticmethod
    def get_new_refente_with_bobine(refente, bobine):
        start_index = 0
        counter_pose = 0
        bobine_pose = bobine.pose
        if bobine.pose == 0:
            bobine_pose = 1
        for laize_refente in refente.laizes:
            if laize_refente and laize_refente == bobine.laize:
                counter_pose += 1
                if counter_pose >= bobine_pose:
                    break
            else:
                counter_pose = 0
                start_index += 1
        new_refente = Refente()
        index_refente = 0
        for laize_refente in refente.laizes:
            if index_refente < start_index or index_refente >= start_index + bobine_pose:
                new_refente.laizes[index_refente] = laize_refente
            index_refente += 1
        return new_refente

    def get_end(self):
        if not self.longueur or not self.tours:
            self.end = self.start
        else:
            self.end = self.start + (((self.longueur * self.tours)/3)*(PERCENT_PROD_THEROIQUE_MAXI/100))
        return self.end

    def set_tours(self, tours):
        self.tours = tours
        self.get_end()
        self.ON_TOURS_CHANGED.emit()

    def init_bobine_fille_store(self):
        for bobine in bobine_fille_store.bobines:
            new_bobine = BobineFilleValid(bobine=bobine)
            self.current_bobine_fille_store.add_bobine(new_bobine)

    def init_refente_store(self):
        for refente in refente_store.refentes:
            self.current_refente_store.add_refente(refente)

    def init_perfo_store(self):
        for perfo in perfo_store.perfos:
            self.current_perfo_store.add_perfo(perfo)

    def init_bobine_papier_store(self):
        for bobine in bobine_papier_store.bobines:
            self.current_bobine_papier_store.add_bobine(bobine)

    def init_bobine_poly_store(self):
        for bobine in bobine_poly_store.bobines:
            self.current_bobine_poly_store.add_bobine(bobine)

    def add_bobine_selected(self, bobine, pose):
        from commun.model.bobine_fille_selected import BobineFilleSelected
        new_bobine = BobineFilleSelected(bobine, pose=pose)
        self.bobines_filles_selected.append(new_bobine)
        self.update_all_current_store()
        self.update_encrier(bobine=bobine)
        self.ON_CHANGED_SIGNAL.emit()

    def add_refente_selected(self, refente):
        self.refente_selected = refente
        self.set_refente_encrier()
        self.update_all_current_store()
        self.ON_CHANGED_SIGNAL.emit()

    def add_perfo_selected(self, perfo):
        self.perfo_selected = perfo
        self.update_all_current_store()
        self.ON_CHANGED_SIGNAL.emit()

    def add_bobine_papier_selected(self, bobine):
        self.bobine_papier_selected = bobine
        self.update_all_current_store()
        self.ON_CHANGED_SIGNAL.emit()

    def add_bobine_poly_selected(self, bobine):
        self.bobine_poly_selected = bobine
        self.update_all_current_store()
        self.ON_CHANGED_SIGNAL.emit()

    def del_item_selected(self, data_type):
        if data_type == "bobine":
            self.bobines_filles_selected = []
        if data_type == "papier":
            self.bobine_papier_selected = None
        if data_type == "poly":
            self.bobine_poly_selected = None
        if data_type == "refente":
            self.refente_selected = None
        if data_type == "perfo":
            self.perfo_selected = None
        self.update_all_current_store()
        self.ON_CHANGED_SIGNAL.emit()

    def clear_plan_prod(self):
        self.bobines_filles_selected = []
        self.bobine_papier_selected = None
        self.bobine_poly_selected = None
        self.refente_selected = None
        self.perfo_selected = None
        self.init_current_store()
        self.ON_CHANGED_SIGNAL.emit()

    def definied_longueur(self):
        self.longueur = None
        if self.bobines_filles_selected:
            self.longueur = self.bobines_filles_selected[0].length
        self.get_end()

    def init_current_store(self):
        self.current_refente_store = RefenteStore()
        self.init_refente_store()
        self.current_perfo_store = PerfoStore()
        self.init_perfo_store()
        self.current_bobine_fille_store = BobineFilleStore()
        self.init_bobine_fille_store()
        self.current_bobine_papier_store = BobinePapierStore()
        self.init_bobine_papier_store()
        self.current_bobine_poly_store = BobinePolyStore()
        self.init_bobine_poly_store()

    def update_all_current_store(self):
        self.init_current_store()
        self.definied_longueur()
        contrainte = self.get_contrainte()
        self.current_bobine_papier_store.bobines = \
            filter.filter_bobines_papier_for_contrainte(bobines_papier=self.current_bobine_papier_store.bobines,
                                                        contrainte=contrainte)
        self.current_refente_store.refentes = \
            filter.filter_refentes_for_contrainte(refentes=self.current_refente_store.refentes,
                                                  contrainte=contrainte)
        self.current_bobine_fille_store.bobines = \
            filter.filter_bobines_fille_for_contrainte(bobines_fille=self.current_bobine_fille_store.bobines,
                                                       contrainte=contrainte)
        self.filter_bobine_papier_bobine_fille_refente_store(contrainte)
        self.current_bobine_poly_store.bobines = \
            filter.filter_bobines_poly_for_bobines_papier(bobines_poly=self.current_bobine_poly_store.bobines,
                                                          bobines_papier=self.current_bobine_papier_store.bobines)
        self.current_perfo_store.perfos = \
            filter.filter_perfos_for_refentes(perfos=self.current_perfo_store.perfos,
                                              refentes=self.current_refente_store.refentes)
        self.ON_CHANGED_SIGNAL.emit()

    def filter_bobine_papier_bobine_fille_refente_store(self, contrainte):
        length_bobines_papier = len(self.current_bobine_papier_store.bobines)
        length_bobines_fille = len(self.current_bobine_fille_store.bobines)
        length_refentes = len(self.current_refente_store.refentes)
        self.current_bobine_papier_store.bobines = \
            filter.filter_bobines_papier_for_refentes(bobines_papier=self.current_bobine_papier_store.bobines,
                                                      refentes=self.current_refente_store.refentes)
        self.current_bobine_papier_store.bobines = \
            filter.filter_bobines_papier_for_bobines_fille(bobines_papier=self.current_bobine_papier_store.bobines,
                                                           bobines_fille=self.current_bobine_fille_store.bobines)
        self.current_refente_store.refentes = \
            filter.filter_refentes_for_bobines_papier(refentes=self.current_refente_store.refentes,
                                                      bobines_papier=self.current_bobine_papier_store.bobines)
        self.current_refente_store.refentes = \
            filter.filter_refentes_for_bobines_fille(refentes=self.current_refente_store.refentes,
                                                     bobines_fille=self.current_bobine_fille_store.bobines,
                                                     bobines_fille_selected=contrainte.bobines_fille)
        self.current_bobine_fille_store.bobines = \
            filter.filter_bobines_fille(bobines_fille=self.current_bobine_fille_store.bobines,
                                        refentes=self.current_refente_store.refentes,
                                        bobines_fille_selected=contrainte.bobines_fille,
                                        bobines_papier=self.current_bobine_papier_store.bobines)
        new_length_bobines_papier = len(self.current_bobine_papier_store.bobines)
        new_length_bobines_fille = len(self.current_bobine_fille_store.bobines)
        new_length_refentes = len(self.current_refente_store.refentes)
        if new_length_bobines_fille != length_bobines_fille\
                or new_length_bobines_papier != length_bobines_papier\
                or new_length_refentes != length_refentes:
            self.filter_bobine_papier_bobine_fille_refente_store(contrainte)

    def get_contrainte(self):
        bobine_poly = None
        if self.bobine_poly_selected:
            bobine_poly = self.bobine_poly_selected
        perfo = None
        if self.perfo_selected:
            perfo = self.perfo_selected
        bobine_papier = None
        if self.bobine_papier_selected:
            bobine_papier = self.bobine_papier_selected
        refente = None
        if self.refente_selected:
            refente = self.refente_selected
        bobines_filles = None
        if self.bobines_filles_selected:
            bobines_filles = self.bobines_filles_selected
        contrainte = Contrainte(bobine_poly=bobine_poly,
                                bobine_papier=bobine_papier,
                                perfo=perfo,
                                refente=refente,
                                bobines_fille=bobines_filles)
        return contrainte

    @staticmethod
    def refente_is_complete(refente):
        for laize in refente.laizes:
            if laize:
                return False
        return True

    def get_new_item_selected_from_store(self):
        if len(self.current_bobine_poly_store.bobines) == 1:
            self.bobine_poly_selected = self.current_bobine_poly_store.bobines[0]
        if len(self.current_perfo_store.perfos) == 1:
            self.perfo_selected = self.current_perfo_store.perfos[0]
        if self.refente_selected:
            for perfo in perfo_store.perfos:
                if perfo.code == self.refente_selected.code_perfo:
                    self.perfo_selected = perfo
        if len(self.current_bobine_papier_store.bobines) == 1:
            self.bobine_papier_selected = self.current_bobine_papier_store.bobines[0]
        if len(self.current_refente_store.refentes) == 1:
            self.add_refente_selected(self.current_refente_store.refentes[0])
        self.ON_CHANGED_SIGNAL.emit()

    @staticmethod
    def remove_bobine_in_bobines_fille_store(bobine_to_remove, bobine_store):
        new_bobine_fille_store = BobineFilleStore()
        for bobine in bobine_store.bobines:
            if bobine.code != bobine_to_remove.code:
                new_bobine_fille_store.add_bobine(bobine)
        return new_bobine_fille_store
