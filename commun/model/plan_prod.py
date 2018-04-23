# !/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtCore import pyqtSignal

from commun.constants.param import FIN_PROD_SOIR, PERCENT_PROD_THEROIQUE_MAXI
from commun.utils.timestamp import get_hour_in_timestamp, timestamp_at_time
from commun.model.refente import Refente
from commun.stores.refente_store import RefenteStore
from commun.stores.perfo_store import PerfoStore
from commun.stores.bobine_fille_store import BobineFilleStore
from commun.stores.bobine_papier_store import BobinePapierStore
from commun.stores.bobine_poly_store import BobinePolyStore
from commun.ui.public.mondon_widget import MondonWidget
from commun.stores.bobine_papier_store import bobine_papier_store
from commun.stores.bobine_fille_store import bobine_fille_store
from commun.stores.perfo_store import perfo_store
from commun.stores.refente_store import refente_store
from commun.stores.bobine_poly_store import bobine_poly_store


class PlanProd(MondonWidget):
    ON_CHANGED_SIGNAL = pyqtSignal()
    ON_TOURS_CHANGED = pyqtSignal()

    def __init__(self, start, parent=None, index=None):
        super(PlanProd, self).__init__(parent=parent)
        self.index = index
        self.start = start
        self.end = start
        self.tours = 12
        self.get_end()
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
        self.longueur = None
        self.refente_selected = None
        self.perfo_selected = None
        self.bobines_filles_selected = []
        self.bobine_papier_selected = None
        self.bobine_poly_selected = None
        # self.laize_plan_prod = None
        # self.color_plan_prod = None
        # self.gr_plan_prod = None

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
        from gestion.stores.event_store import event_store
        if event_store.events:
            for event in event_store.events:
                if event.type == "stop":
                    if get_hour_in_timestamp(event.end) == FIN_PROD_SOIR:
                        return timestamp_at_time(self.start, hours=get_hour_in_timestamp(event.start))
        return timestamp_at_time(self.start, hours=FIN_PROD_SOIR)

    def get_max_tour(self):
        end_day_ts = self.get_end_day()
        max_prod_ts = end_day_ts - self.start
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

    def set_tours(self, tours):
        self.tours = tours
        self.get_end()
        self.ON_TOURS_CHANGED.emit()

    def init_bobine_fille_store(self):
        for bobine in bobine_fille_store.bobines:
            self.current_bobine_fille_store.add_bobine(bobine)

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

    def add_bobine_selected(self, bobine):
        self.bobines_filles_selected.append(bobine)
        self.update_all_current_store()
        self.ON_CHANGED_SIGNAL.emit()

    def add_refente_selected(self, refente):
        self.refente_selected = refente
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
        self.ON_CHANGED_SIGNAL.emit()

    def definied_longueur(self):
        self.longueur = None
        if self.bobines_filles_selected:
            self.longueur = self.bobines_filles_selected[0].lenght

    # def update_all_current_store(self):
    #     self.definied_plan_prod_param()
    #     self.definied_longueur()
    #     self.update_current_bobine_fille_store()
    #     self.update_current_refente_store()
    #     self.update_current_bobine_papier_store()
    #     self.filter_bobine_poly_from_bobine_papier()
    #     self.filter_perfo_from_refente()
    #     self.get_end()
    #
    #
    # def definied_plan_prod_param(self):
    #     self.definied_laize_plan_prod()
    #     self.definied_color_plan_prod()
    #     self.definied_gr_plan_prod()
    #
    # def definied_laize_plan_prod(self):
    #     self.laize_plan_prod = None
    #     if self.bobine_poly_selected:
    #         self.laize_plan_prod = self.bobine_poly_selected.laize
    #     if self.bobine_papier_selected:
    #         self.laize_plan_prod = self.bobine_papier_selected.laize
    #     if self.refente_selected:
    #         self.laize_plan_prod = self.refente_selected.laize
    #
    # def definied_color_plan_prod(self):
    #     self.color_plan_prod = None
    #     if self.bobine_papier_selected:
    #         self.color_plan_prod = self.bobine_papier_selected.color
    #     if self.bobines_filles_selected:
    #         self.color_plan_prod = self.bobines_filles_selected[0].color
    #
    # def definied_gr_plan_prod(self):
    #     self.gr_plan_prod = None
    #     if self.bobine_papier_selected:
    #         self.gr_plan_prod = self.bobine_papier_selected.gr
    #     if self.bobines_filles_selected:
    #         self.gr_plan_prod = self.bobines_filles_selected[0].gr
    #
    # def update_current_bobine_fille_store(self):
    #     # Crée un nouveau magasin de bobine fille vide
    #     new_bobine_fille_store = BobineFilleStore()
    #     # Parcour les bobines filles du magasin bobine fille
    #     for bobine in bobine_fille_store.bobines:
    #         # Initialise paramètre de production courant
    #         current_laize_plan_prod = self.laize_plan_prod
    #         current_gr_plan_prod = self.gr_plan_prod
    #         current_color_plan_prod = self.color_plan_prod
    #         # Test bobine est déjà sélectionnée et nécessite une impression
    #         if self.bobine_is_selected_and_printed(bobine):
    #             continue
    #         else:
    #             pass
    #         # Test bobine compatible avec paramètre production courant
    #         if self.bobine_is_compatible_with_current_param_plan_prod(bobine=bobine,
    #                                                                   gr=current_gr_plan_prod,
    #                                                                   color=current_color_plan_prod):
    #             pass
    #         else:
    #             continue
    #         # Update paramètre de production courant
    #         current_gr_plan_prod = self.gr_plan_prod if self.gr_plan_prod else bobine.gr
    #         current_color_plan_prod = self.color_plan_prod if self.color_plan_prod else bobine.color
    #         # Recherche une combinaison refente et bobine papier compatible avec la bobine
    #         if self.get_refente_and_bobine_papier_compatible_with_bobine(bobine=bobine,
    #                                                                      laize_prod=current_laize_plan_prod,
    #                                                                      gr_prod=current_gr_plan_prod,
    #                                                                      color_prod=current_color_plan_prod):
    #             pass
    #         else:
    #             continue
    #         # Ajoute bobine au nouveau magasin de bobine fille
    #         new_bobine_fille_store.add_bobine(bobine)
    #     # Remplace le magasin de bobine fille courant par le nouveau magasin de bobine fille
    #     self.current_bobine_fille_store = new_bobine_fille_store
    #
    # def get_refente_and_bobine_papier_compatible_with_bobine(self, bobine, laize_prod, gr_prod, color_prod):
    #     if self.refente_selected:
    #         if self.refente_is_compatible_from_bobine_and_bobine_papier(refente=self.refente_selected,
    #                                                                     bobine=bobine,
    #                                                                     color_prod=color_prod,
    #                                                                     gr_prod=gr_prod,
    #                                                                     laize_prod=laize_prod):
    #             return True
    #     else:
    #         for refente in refente_store.refentes:
    #             if self.refente_is_compatible_from_bobine_and_bobine_papier(refente=refente,
    #                                                                         bobine=bobine,
    #                                                                         color_prod=color_prod,
    #                                                                         gr_prod=gr_prod,
    #                                                                         laize_prod=laize_prod):
    #                 return True
    #     return False
    #
    # def update_current_refente_store(self):
    #     new_refente_store = RefenteStore()
    #     for refente in refente_store.refentes:
    #         if self.refente_is_compatible_with_perfo(refente):
    #             if self.refente_is_comptatible_with_current_param_plan_prod(refente=refente, laize=self.laize_plan_prod):
    #                 if self.refente_is_compatible_from_bobines_filles_selected(refente=refente):
    #                     new_refente = refente
    #                     for bobine_fille_selected in self.bobines_filles_selected:
    #                         new_refente = self.get_new_refente_with_bobine(new_refente, bobine_fille_selected)
    #                     refente_is_ok = True
    #                     if self.refente_is_complete(new_refente):
    #                         pass
    #                     else:
    #                         for laize in new_refente.laizes:
    #                             if self.laize_is_compatible_with_current_bobine_fille_store(laize):
    #                                 continue
    #                             else:
    #                                 refente_is_ok = False
    #                                 break
    #                     if refente_is_ok:
    #                         new_refente_store.add_refente(refente)
    #     self.current_refente_store = new_refente_store
    #
    # def update_current_bobine_papier_store(self):
    #     new_bobine_papier_store = BobinePapierStore()
    #     for bobine_papier in bobine_papier_store.bobines:
    #         if self.bobine_papier_is_compatible_with_current_param_plan_prod(bobine=bobine_papier,
    #                                                                          laize=self.laize_plan_prod,
    #                                                                          color=self.color_plan_prod,
    #                                                                          gr=self.gr_plan_prod):
    #             if self.bobine_papier_is_compatible_with_current_refente_store(bobine_papier):
    #                 if self.bobine_papier_is_compatible_with_current_bobine_store(bobine_papier):
    #                     new_bobine_papier_store.add_bobine(bobine_papier)
    #     self.current_bobine_papier_store = new_bobine_papier_store
    #
    # def laize_is_compatible_with_current_bobine_fille_store(self, laize):
    #     for bobine in self.current_bobine_fille_store.bobines:
    #         if bobine.laize == laize or not laize:
    #             return True
    #     return False
    #
    # @staticmethod
    # def refente_is_complete(refente):
    #     for laize in refente.laizes:
    #         if laize:
    #             return False
    #     return True
    #
    # def refente_is_compatible_from_bobine_and_bobine_papier(self, refente, bobine, laize_prod, gr_prod, color_prod):
    #     if self.refente_is_compatible_with_perfo(refente):
    #         if self.refente_is_comptatible_with_current_param_plan_prod(refente, laize_prod):
    #             if self.get_bobine_papier_compatible_with_refente(refente, gr_prod, color_prod):
    #                 if self.bobines_filles_selected:
    #                     if self.refente_is_compatible_from_bobines_filles_selected(refente):
    #                         new_refente = refente
    #                         for bobine_fille_selected in self.bobines_filles_selected:
    #                             new_refente = self.get_new_refente_with_bobine(new_refente, bobine_fille_selected)
    #                         if self.refente_is_compatible_from_bobine(bobine=bobine, refente=new_refente):
    #                             return True
    #                 else:
    #                     if self.refente_is_compatible_from_bobine(bobine=bobine, refente=refente):
    #                         return True
    #     return False
    #
    # def refente_is_compatible_with_perfo(self, refente):
    #     if self.perfo_selected:
    #         if self.perfo_selected.code == refente.code_perfo:
    #             return True
    #         else:
    #             return False
    #     return True
    #
    # def get_bobine_papier_compatible_with_refente(self, refente, gr_prod, color_prod):
    #     if self.bobine_papier_selected:
    #         if self.bobine_papier_selected.laize == refente.laize \
    #                 and (self.bobine_papier_selected.gr == gr_prod or not gr_prod) \
    #                 and (self.bobine_papier_selected.color == color_prod or not color_prod):
    #             return True
    #         else:
    #             return False
    #     else:
    #         for bobine_papier in bobine_papier_store.bobines:
    #             if bobine_papier.laize == refente.laize \
    #                     and (bobine_papier.gr == gr_prod or not gr_prod) \
    #                     and (bobine_papier.color == color_prod or not color_prod):
    #                 return True
    #             else:
    #                 continue
    #         return False
    #
    # def bobine_papier_is_compatible_with_current_refente_store(self, bobine):
    #     if self.refente_selected:
    #         if self.refente_selected.laize == bobine.laize:
    #             return True
    #         else:
    #             return False
    #     else:
    #         for refente in self.current_refente_store.refentes:
    #             if refente.laize == bobine.laize:
    #                 return True
    #         return False
    #
    # def bobine_papier_is_compatible_with_current_bobine_store(self, bobine_papier):
    #     if self.bobines_filles_selected:
    #         return True
    #     else:
    #         for bobine in self.current_bobine_fille_store.bobines:
    #             if bobine_papier.color == bobine.color and bobine_papier.gr == bobine.gr:
    #                 return True
    #         return False
    #
    # @staticmethod
    # def bobine_papier_is_compatible_with_current_param_plan_prod(bobine, laize, color, gr):
    #     if (bobine.color == color or not color) and (bobine.laize == laize or not laize) and (bobine.gr == gr or not gr):
    #         return True
    #     else:
    #         return False
    #
    # @staticmethod
    # def bobine_is_compatible_with_current_param_plan_prod(bobine, gr, color):
    #     if (bobine.color == color or not color) and (bobine.gr == gr or not gr):
    #         return True
    #     else:
    #         return False
    #
    # def bobine_is_selected_and_printed(self, bobine):
    #     if self.bobines_filles_selected:
    #         for bobine_selected in self.bobines_filles_selected:
    #             if bobine_selected.code == bobine.code and bobine.pose > 0:
    #                 return True
    #         return False
    #     return False
    #
    # @staticmethod
    # def refente_is_comptatible_with_current_param_plan_prod(refente, laize):
    #     if refente.laize == laize or not laize:
    #         return True
    #     else:
    #         return False
    #
    # def refente_is_compatible_from_bobines_filles_selected(self, refente):
    #     new_refente = refente
    #     for bobine in self.bobines_filles_selected:
    #         if self.refente_is_compatible_from_bobine(bobine, new_refente):
    #             new_refente = self.get_new_refente_with_bobine(new_refente, bobine)
    #             continue
    #         else:
    #             return False
    #     return True
    #
    # @staticmethod
    # def refente_is_compatible_from_bobine(bobine, refente):
    #     counter_pose = 0
    #     for laize_refente in refente.laizes:
    #         if laize_refente and laize_refente == bobine.laize:
    #             counter_pose += 1
    #             if counter_pose >= bobine.pose:
    #                 return True
    #         else:
    #             counter_pose = 0
    #     return False
    #
    # def filter_bobine_poly_from_bobine_papier(self):
    #     new_bobine_poly_store = BobinePolyStore()
    #     for bobine_poly in bobine_poly_store.bobines:
    #         if self.is_compatible_bobine_poly_from_bobine_papier_store(bobine_poly):
    #             new_bobine_poly_store.add_bobine(bobine_poly)
    #     self.current_bobine_poly_store = new_bobine_poly_store
    #
    # def is_compatible_bobine_poly_from_bobine_papier_store(self, bobine_poly):
    #     for bobine_papier in self.current_bobine_papier_store.bobines:
    #         if bobine_poly.laize == bobine_papier.laize:
    #             return True
    #     return False
    #
    # def filter_perfo_from_refente(self):
    #     new_perfo_store = PerfoStore()
    #     for perfo in perfo_store.perfos:
    #         if self.is_compatible_perfo_from_refente_store(perfo):
    #             new_perfo_store.add_perfo(perfo)
    #     self.current_perfo_store = new_perfo_store
    #
    # def is_compatible_perfo_from_refente_store(self, perfo):
    #     for refente in self.current_refente_store.refentes:
    #         if refente.code_perfo == perfo.code:
    #             return True
    #     return False
    #
    # def get_new_item_selected_from_store(self):
    #     if len(self.current_bobine_poly_store.bobines) == 1:
    #         self.bobine_poly_selected = self.current_bobine_poly_store.bobines[0]
    #     if len(self.current_perfo_store.perfos) == 1:
    #         self.perfo_selected = self.current_perfo_store.perfos[0]
    #     if self.refente_selected:
    #         for perfo in perfo_store.perfos:
    #             if perfo.code == self.refente_selected.code_perfo:
    #                 self.perfo_selected = perfo
    #     if len(self.current_bobine_papier_store.bobines) == 1:
    #         self.bobine_papier_selected = self.current_bobine_papier_store.bobines[0]
    #     if len(self.current_refente_store.refentes) == 1:
    #         self.refente_selected = self.current_refente_store.refentes[0]
    #     if self.refente_selected:
    #         new_refente = self.refente_selected
    #         for bobine in self.bobines_filles_selected:
    #             new_refente = self.get_new_refente_with_bobine(new_refente, bobine)
    #         for laize in new_refente.laizes:
    #             count_bobine_compatible_with_laize = 0
    #             bobine_compatible_with_laize = None
    #             for bobine in self.current_bobine_fille_store.bobines:
    #                 if bobine.laize == laize:
    #                     count_bobine_compatible_with_laize += 1
    #                     bobine_compatible_with_laize = bobine
    #                 if count_bobine_compatible_with_laize > 1:
    #                     bobine_compatible_with_laize = None
    #                     break
    #             if bobine_compatible_with_laize:
    #                 self.bobines_filles_selected.append(bobine_compatible_with_laize)
    #                 self.update_current_bobine_fille_store()
    #     self.ON_CHANGED_SIGNAL.emit()
