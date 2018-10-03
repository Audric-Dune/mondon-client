# !/usr/bin/env python
# -*- coding: utf-8 -*-


from PyQt5.QtCore import pyqtSignal, QObject

from commun.utils.timestamp import timestamp_to_hour_little
from commun.utils import filter
from commun.model.contraintes import Contrainte
from commun.model.encrier import Encrier
from commun.stores.refente_store import RefenteStore
from commun.stores.perfo_store import PerfoStore
from commun.stores.bobine_fille_store import BobineFilleStore
from commun.stores.bobine_papier_store import BobinePapierStore
from commun.stores.bobine_poly_store import BobinePolyStore
from commun.stores.bobine_fille_store import bobine_fille_store
from commun.stores.perfo_store import perfo_store
from commun.stores.refente_store import refente_store
from commun.stores.bobine_papier_store import bobine_papier_store
from commun.stores.bobine_poly_store import bobine_poly_store
from commun.model.data_reglages import DataReglages

from gestion.utils import get_refente, get_perfo_from_refente, get_bobines,\
    get_bobine_papier, get_bobine_poly, init_store, init_bobine_fille_store,\
    get_time_prod, get_color_encrier_last_plan_prod


class PlanProd(QObject):
    ON_CHANGED_SIGNAL = pyqtSignal()
    ON_TOURS_CHANGED = pyqtSignal()

    def __init__(self, last_plan_prod, data=None, start=None):
        super(PlanProd, self).__init__()
        self.p_id = None
        self.start = None
        self.end = None
        self.data_reglages = None
        self.tours = 1
        self.longueur = None
        self.refente_selected = None
        self.perfo_selected = None
        self.bobines_filles_selected = []
        self.bobine_papier_selected = None
        self.bobine_poly_selected = None
        self.encrier_1 = Encrier()
        self.encrier_2 = Encrier()
        self.encrier_3 = Encrier()
        self.encriers = [self.encrier_1, self.encrier_2, self.encrier_3]
        self.last_plan_prod = last_plan_prod
        self.data_reglages = DataReglages(plan_prod=self, last_plan_prod=self.last_plan_prod)
        self.current_refente_store = None
        self.current_perfo_store = None
        self.current_bobine_fille_store = None
        self.current_bobine_papier_store = None
        self.current_bobine_poly_store = None
        self.init_current_store()
        if data:
            self.new_plan = False
            self.update_from_data(data=data)
        else:
            self.new_plan = True
            import random
            self.p_id = random.randint(0, 100000000)
            self.start = start
            self.end = start
            self.update_from_last_plan_prod()

    def init_current_store(self):
        self.current_refente_store = init_store(store=RefenteStore(), items=refente_store.refentes)
        self.current_perfo_store = init_store(store=PerfoStore(), items=perfo_store.perfos)
        self.current_bobine_fille_store = init_bobine_fille_store(store=BobineFilleStore(),
                                                                  bobines=bobine_fille_store.bobines)
        self.current_bobine_papier_store = init_store(store=BobinePapierStore(), items=bobine_papier_store.bobines)
        self.current_bobine_poly_store = init_store(store=BobinePolyStore(), items=bobine_poly_store.bobines)

    def update_from_data(self, data):
        self.p_id = data[0]
        self.start = data[1]
        self.tours = data[2]
        self.longueur = data[3]
        self.bobine_papier_selected = get_bobine_papier(code=data[4])
        self.set_refente(refente=get_refente(code=data[5]))
        self.set_bobines_filles_selected(bobines=get_bobines(code_bobines_filles=data[6]))
        self.bobine_poly_selected = get_bobine_poly(code=data[7])
        self.perfo_selected = get_perfo_from_refente(refente=self.refente_selected)
        self.encrier_1.set_color(data[8])
        self.encrier_2.set_color(data[9])
        self.encrier_3.set_color(data[10])
        self.data_reglages.update_data_reglage_from_code(data[11])
        self.end = self.get_end()

    def update_from_start(self, start, last_plan_prod):
        self.start = start
        self.last_plan_prod = last_plan_prod
        self.update_from_last_plan_prod()
        self.end = self.get_end()

    def update_from_last_plan_prod(self):
        self.data_reglages.last_p = self.last_plan_prod
        self.data_reglages.update_reglage()
        self.set_color_encrier_from_last_plan_prod()

    def set_color_encrier_from_last_plan_prod(self):
        if self.last_plan_prod:
            if self.encrier_1.color is None or self.encrier_1.color[0] == "_":
                self.encrier_1.set_color(get_color_encrier_last_plan_prod(self.last_plan_prod.encrier_1.color))
            if self.encrier_2.color is None or self.encrier_2.color[0] == "_":
                self.encrier_2.set_color(get_color_encrier_last_plan_prod(self.last_plan_prod.encrier_2.color))
            if self.encrier_3.color is None or self.encrier_3.color[0] == "_":
                self.encrier_3.set_color(get_color_encrier_last_plan_prod(self.last_plan_prod.encrier_3.color))

    def get_end(self):
        if not self.longueur or not self.tours:
            self.end = self.start
        else:
            self.end = self.start + get_time_prod(plan_prod=self)
        self.end += self.data_reglages.time_reglage*60
        return self.end

    def get_start(self):
        return self.start

    def set_refente(self, refente):
        self.refente_selected = refente
        for encrier in self.encriers:
            encrier.refente = self.refente_selected

    def set_bobines_filles_selected(self, bobines):
        self.bobines_filles_selected = bobines
        self.set_bobines_fille_selected_to_encriers()

    def set_tours(self, tours):
        self.tours = tours
        self.get_end()
        self.ON_TOURS_CHANGED.emit()

    def set_color_encrier_from_bobine(self, color, colors_cliche):

        def color_available_in_encrier(encriers, p_color):
            for encrier in encriers:
                if encrier.color is None:
                    continue
                if encrier.color[1:] == p_color:
                    encrier.set_color(p_color)
                    return True
                if encrier.color == p_color:
                    if p_color[0] == "_":
                        encrier.set_color(p_color[1:])
                    return True
            return False

        def get_free_encrier(encriers, p_colors_cliche):
            for encrier in encriers:
                if encrier.color is None or encrier.color[0] == "_":
                    if encrier.color and encrier.color[1:] in p_colors_cliche:
                        continue
                    return encrier
            return False

        if color_available_in_encrier(encriers=self.encriers, p_color=color):
            pass
        else:
            free_encrier = get_free_encrier(encriers=self.encriers, p_colors_cliche=colors_cliche)
            free_encrier.set_color(color)

    def set_bobines_fille_selected_to_encriers(self):
        for encrier in self.encriers:
            encrier.bobines_filles_selected = self.bobines_filles_selected

    def update_encrier(self):
        self.set_bobines_fille_selected_to_encriers()
        for encrier in self.encriers:
            encrier.reset_color()
        self.set_color_encrier_from_last_plan_prod()
        for bobine in self.bobines_filles_selected:
            if bobine.colors_cliche is not None:
                for color in bobine.colors_cliche:
                    self.set_color_encrier_from_bobine(color, bobine.colors_cliche)

    def add_bobine_selected(self, bobine, pose):
        from commun.model.bobine_fille_selected import BobineFilleSelected
        new_bobine = BobineFilleSelected(bobine, pose=pose)
        self.bobines_filles_selected.append(new_bobine)
        self.update_all_current_store()
        self.update_encrier()
        self.ON_CHANGED_SIGNAL.emit()

    def del_bobine_selected(self, bobine):
        self.bobines_filles_selected.remove(bobine)
        self.update_all_current_store()
        self.update_encrier()
        self.ON_CHANGED_SIGNAL.emit()

    def add_refente_selected(self, refente):
        self.set_refente(refente)
        self.update_all_current_store()
        self.ON_CHANGED_SIGNAL.emit()

    def del_refente_selected(self):
        self.set_refente(refente=None)
        self.update_all_current_store()
        self.ON_CHANGED_SIGNAL.emit()

    def add_perfo_selected(self, perfo):
        self.perfo_selected = perfo
        self.update_all_current_store()
        self.ON_CHANGED_SIGNAL.emit()

    def del_perfo_selected(self):
        self.perfo_selected = None
        self.update_all_current_store()
        self.ON_CHANGED_SIGNAL.emit()

    def add_bobine_papier_selected(self, bobine):
        self.bobine_papier_selected = bobine
        self.update_all_current_store()
        self.ON_CHANGED_SIGNAL.emit()

    def del_papier_selected(self):
        self.bobine_papier_selected = None
        self.update_all_current_store()
        self.ON_CHANGED_SIGNAL.emit()

    def add_bobine_poly_selected(self, bobine):
        self.bobine_poly_selected = bobine
        self.update_all_current_store()
        self.ON_CHANGED_SIGNAL.emit()

    def del_poly_selected(self):
        self.bobine_poly_selected = None
        self.update_all_current_store()
        self.ON_CHANGED_SIGNAL.emit()

    def definied_longueur(self):
        self.longueur = None
        if self.bobines_filles_selected:
            self.longueur = self.bobines_filles_selected[0].length

    def update_all_current_store(self):
        self.init_current_store()
        self.definied_longueur()
        if not self.plan_prod_is_empty():
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
        print('filter_bobine_papier_bobine_fille_refente_store')
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
    
    def plan_prod_is_empty(self):
        if self.bobines_filles_selected:
            return False
        if self.refente_selected:
            return False
        if self.bobine_papier_selected:
            return False
        if self.perfo_selected:
            return False
        if self.bobine_poly_selected:
            return False
        return True

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

    def __repr__(self):
        return "ID{}, {}-{}, {}".format(self.p_id,
                                        timestamp_to_hour_little(self.start),
                                        timestamp_to_hour_little(self.end),
                                        self.bobine_papier_selected.color if self.bobine_papier_selected else None,
                                        self.bobine_poly_selected)
