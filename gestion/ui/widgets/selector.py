# !/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QScrollArea, QVBoxLayout, QWidget
from commun.constants.colors import color_bleu_gris
from commun.constants.stylesheets import scroll_bar_stylesheet
from commun.ui.public.mondon_widget import MondonWidget
from commun.utils.layout import clear_layout
from gestion.ui.widgets.line_bobine import LineBobine
from gestion.ui.widgets.line_refente import LineRefente
from gestion.ui.widgets.line_perfo import LinePerfo
from gestion.ui.widgets.line_bobine_papier import LineBobinePapier
from gestion.ui.widgets.line_bobine_poly import LineBobinePoly
from gestion.ui.widgets.selector_pose import SelectorPose
from gestion.stores.settings_store import settings_store_gestion


class Selector(MondonWidget):

    def __init__(self, plan_prod, parent):
        super(Selector, self).__init__(parent=parent)
        self.plan_prod = plan_prod
        self.parent = parent
        self.list_bobines = []
        self.sort_name = "code"
        self.sort_asc = True
        self.current_focus = None
        self.background_color = color_bleu_gris
        self.master_vbox = QVBoxLayout()
        self.master_vbox.setContentsMargins(0, 0, 0, 0)
        self.master_vbox.setSpacing(0)
        self.selector_pose = None
        self.vbox = QVBoxLayout()
        self.scroll_bar = QScrollArea(parent=self)
        self.content_scrollbar = QWidget(parent=self.scroll_bar)
        self.init_widget()
        self.update_list()
        self.update_widget()

    def init_widget(self):
        self.vbox.setContentsMargins(0, 0, 0, 0)
        self.vbox.setSpacing(5)
        self.content_scrollbar.setLayout(self.vbox)
        self.content_scrollbar.setContentsMargins(0, 0, 0, 0)
        self.scroll_bar.setWidget(self.content_scrollbar)
        self.scroll_bar.setStyleSheet(scroll_bar_stylesheet)
        self.scroll_bar.setWidgetResizable(True)
        self.master_vbox.addWidget(self.scroll_bar)
        self.setLayout(self.master_vbox)

    def on_filter_changed(self):
        self.update_list()

    def sort_bobine(self):
        self.list_bobines = self.sort_bobines(self.list_bobines, "code", True)
        self.list_bobines = self.sort_bobines(self.list_bobines, self.sort_name, self.sort_asc)

    @staticmethod
    def sort_bobines(bobines, sort_name, sort_asc):
        bobines = sorted(bobines, key=lambda b: b.get_value(sort_name), reverse=not sort_asc)
        return bobines

    def update_list(self, search_code=None):
        self.list_bobines = []
        for bobine in self.plan_prod.current_bobine_fille_store.bobines:
            if self.is_valid_bobine_from_filters(bobine):
                self.list_bobines.append(bobine)
        self.update_widget()

    def is_valid_bobine_from_filters(self, bobine):
        from gestion.stores.filter_store import filter_store
        for name in filter_store.list_filter:
            if not self.is_valid_bobine_from_filter(bobine, name):
                return False
        return True

    @staticmethod
    def is_valid_bobine_from_filter(bobine, name):
        from gestion.stores.filter_store import filter_store
        dict_filter = filter_store.dicts_filter[name]
        if name == "poses":
            for key in dict_filter.keys():
                for pose in bobine.poses:
                    if key == pose and dict_filter[key]:
                        return True
            return False
        else:
            for key in dict_filter.keys():
                if key == getattr(bobine, name) and dict_filter[key]:
                    return True
            return False

    def update_widget(self):
        self.sort_bobine()
        self.current_focus = self.parent.bloc_focus
        clear_layout(self.vbox)
        if self.current_focus == "bobine" or not self.current_focus:
            for bobine in self.list_bobines:
                line_bobine = LineBobine(parent=self, bobine=bobine)
                line_bobine.ON_DBCLICK_SIGNAL.connect(self.handle_selected_bobine)
                line_bobine.setFixedHeight(20)
                self.vbox.addWidget(line_bobine)
        if self.current_focus == "refente":
            for refente in self.plan_prod.current_refente_store.refentes:
                line_refente = LineRefente(parent=self, refente=refente, ech=settings_store_gestion.ech)
                line_refente.ON_DBCLICK_SIGNAL.connect(self.handle_selected_refente)
                self.vbox.addWidget(line_refente)
        if self.current_focus == "perfo":
            for perfo in self.plan_prod.current_perfo_store.perfos:
                line_perfo = LinePerfo(parent=self, perfo=perfo, ech=settings_store_gestion.ech)
                line_perfo.ON_DBCLICK_SIGNAL.connect(self.handle_selected_perfo)
                self.vbox.addWidget(line_perfo)
        if self.current_focus == "papier":
            for bobine in self.plan_prod.current_bobine_papier_store.bobines:
                line_bobine_papier = LineBobinePapier(parent=self, bobine=bobine)
                line_bobine_papier.ON_DBCLICK_SIGNAL.connect(self.handle_selected_bobine_papier)
                line_bobine_papier.setFixedHeight(20)
                self.vbox.addWidget(line_bobine_papier)
        if self.current_focus == "poly":
            for bobine in self.plan_prod.current_bobine_poly_store.bobines:
                line_bobine_poly = LineBobinePoly(parent=self, bobine=bobine)
                line_bobine_poly.ON_DBCLICK_SIGNAL.connect(self.handle_selected_bobine_poly)
                line_bobine_poly.setFixedHeight(20)
                self.vbox.addWidget(line_bobine_poly)
        self.vbox.addStretch(0)
        self.update()

    def handle_selected_bobine(self, bobine, pose=None):
        if pose:
            self.plan_prod.add_bobine_selected(bobine, pose)
        elif len(bobine.poses) == 1:
            self.plan_prod.add_bobine_selected(bobine, bobine.poses[0])
        else:
            self.selector_pose = SelectorPose(self.handle_selected_bobine, bobine)
            self.selector_pose.show()

    def handle_selected_refente(self, refente):
        self.plan_prod.add_refente_selected(refente)

    def handle_selected_perfo(self, perfo):
        self.plan_prod.add_perfo_selected(perfo)

    def handle_selected_bobine_papier(self, bobine):
        self.plan_prod.add_bobine_papier_selected(bobine)

    def handle_selected_bobine_poly(self, bobine):
        self.plan_prod.add_bobine_poly_selected(bobine)
