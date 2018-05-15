# !/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QScrollArea, QVBoxLayout, QWidget

from commun.constants.colors import color_bleu_gris
from commun.constants.stylesheets import scroll_bar_stylesheet
from commun.ui.public.mondon_widget import MondonWidget
from gestion.ui.widgets.line_bobine import LineBobine
from gestion.ui.widgets.line_refente import LineRefente
from gestion.ui.widgets.line_perfo import LinePerfo
from gestion.ui.widgets.line_bobine_papier import LineBobinePapier
from gestion.ui.widgets.line_bobine_poly import LineBobinePoly
from gestion.ui.widgets.selector_pose import SelectorPose
from gestion.stores.settings_store import settings_store_gestion
from gestion.stores.filter_store import filter_store


class Selector(MondonWidget):

    def __init__(self, plan_prod, parent):
        super(Selector, self).__init__(parent=parent)
        self.plan_prod = plan_prod
        self.parent = parent
        self.list_bobines = []
        self.lines_bobine = []
        self.lines_refente = []
        self.lines_papier = []
        self.lines_poly = []
        self.lines_perfo = []
        self.background_color = color_bleu_gris
        self.master_vbox = QVBoxLayout()
        self.master_vbox.setContentsMargins(0, 0, 0, 0)
        self.master_vbox.setSpacing(0)
        self.selector_pose = None
        self.vbox = QVBoxLayout()
        self.scroll_bar = QScrollArea(parent=self)
        self.content_scrollbar = QWidget(parent=self.scroll_bar)
        self.update_list()
        self.init_lists_lines()
        self.init_widget()
        self.update_widget()

    def init_lists_lines(self):
        self.init_list_lines_bobine()
        self.init_list_lines_refente()
        self.init_list_lines_perfo()
        self.init_list_lines_papier()
        self.init_list_lines_poly()

    def init_list_lines_bobine(self):
        for bobine in self.list_bobines:
            line_bobine = LineBobine(parent=self, bobine=bobine)
            line_bobine.ON_DBCLICK_SIGNAL.connect(self.handle_selected_bobine)
            line_bobine.setFixedHeight(20)
            line_bobine.hide()
            self.lines_bobine.append(line_bobine)

    def init_list_lines_refente(self):
        for refente in self.plan_prod.current_refente_store.refentes:
            line_refente = LineRefente(parent=self, refente=refente, ech=settings_store_gestion.ech)
            line_refente.ON_DBCLICK_SIGNAL.connect(self.handle_selected_refente)
            line_refente.hide()
            self.lines_refente.append(line_refente)

    def init_list_lines_perfo(self):
        for perfo in self.plan_prod.current_perfo_store.perfos:
            line_perfo = LinePerfo(parent=self, perfo=perfo, ech=settings_store_gestion.ech)
            line_perfo.ON_DBCLICK_SIGNAL.connect(self.handle_selected_perfo)
            line_perfo.hide()
            self.lines_perfo.append(line_perfo)

    def init_list_lines_papier(self):
        for bobine in self.plan_prod.current_bobine_papier_store.bobines:
            line_bobine_papier = LineBobinePapier(parent=self, bobine=bobine)
            line_bobine_papier.ON_DBCLICK_SIGNAL.connect(self.handle_selected_bobine_papier)
            line_bobine_papier.setFixedHeight(20)
            line_bobine_papier.hide()
            self.lines_papier.append(line_bobine_papier)

    def init_list_lines_poly(self):
        for bobine in self.plan_prod.current_bobine_poly_store.bobines:
            line_bobine_poly = LineBobinePoly(parent=self, bobine=bobine)
            line_bobine_poly.ON_DBCLICK_SIGNAL.connect(self.handle_selected_bobine_poly)
            line_bobine_poly.setFixedHeight(20)
            line_bobine_poly.hide()
            self.lines_poly.append(line_bobine_poly)

    def init_widget(self):
        self.vbox.setContentsMargins(0, 0, 0, 0)
        self.vbox.setSpacing(5)
        for line_bobine in self.lines_bobine:
            self.vbox.addWidget(line_bobine)
        for line_refente in self.lines_refente:
            self.vbox.addWidget(line_refente)
        for line_papier in self.lines_papier:
            self.vbox.addWidget(line_papier)
        for line_poly in self.lines_poly:
            self.vbox.addWidget(line_poly)
        for line_perfo in self.lines_perfo:
            self.vbox.addWidget(line_perfo)
        self.vbox.addStretch()
        self.content_scrollbar.setLayout(self.vbox)
        self.content_scrollbar.setContentsMargins(0, 0, 0, 0)
        self.scroll_bar.setWidget(self.content_scrollbar)
        self.scroll_bar.setStyleSheet(scroll_bar_stylesheet)
        self.scroll_bar.setWidgetResizable(True)
        self.scroll_bar.setMinimumWidth(1200)
        self.scroll_bar.setMinimumHeight(500)
        self.master_vbox.addWidget(self.scroll_bar)
        self.setLayout(self.master_vbox)

    def on_filter_changed(self):
        self.update_widget()

    def sort_bobine(self):
        self.list_bobines = self.sort_bobines(self.list_bobines, "code", True)
        self.list_bobines = self.sort_bobines(self.list_bobines, filter_store.sort_name, filter_store.sort_asc)

    @staticmethod
    def sort_bobines(bobines, sort_name, sort_asc):
        bobines = sorted(bobines, key=lambda b: b.get_value(sort_name), reverse=not sort_asc)
        return bobines

    def update_list(self):
        self.list_bobines = []
        for bobine in self.plan_prod.current_bobine_fille_store.bobines:
            if self.is_valid_bobine_from_filters(bobine) and self.is_valid_from_search_code(bobine):
                self.list_bobines.append(bobine)

    @staticmethod
    def is_valid_from_search_code(bobine):
        if not filter_store.search_code:
            return True
        elif filter_store.search_code in bobine.code:
            return True
        else:
            return False

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
        self.update_list()
        self.sort_bobine()
        current_data_type = filter_store.data_type
        self.hide_lines()
        self.vbox.takeAt(self.vbox.count()-1)
        if current_data_type == "bobine" or not current_data_type:
            for bobine in self.list_bobines:
                line_bobine = self.get_line_bobine(bobine)
                line_bobine.show()
                self.vbox.addWidget(line_bobine)
        if current_data_type == "refente":
            for refente in self.plan_prod.current_refente_store.refentes:
                line_refente = self.get_line_refente(refente)
                line_refente.show()
                self.vbox.addWidget(line_refente)
        if current_data_type == "perfo":
            for perfo in self.plan_prod.current_perfo_store.perfos:
                line_perfo = self.get_line_perfo(perfo)
                line_perfo.show()
                self.vbox.addWidget(line_perfo)
        if current_data_type == "papier":
            for bobine in self.plan_prod.current_bobine_papier_store.bobines:
                line_bobine_papier = self.get_line_papier(bobine)
                line_bobine_papier.show()
                self.vbox.addWidget(line_bobine_papier)
        if current_data_type == "poly":
            for bobine in self.plan_prod.current_bobine_poly_store.bobines:
                line_bobine_poly = self.get_line_poly(bobine)
                line_bobine_poly.show()
                self.vbox.addWidget(line_bobine_poly)
        self.update()
        self.vbox.addStretch()

    def hide_lines(self):
        for line_bobine in self.lines_bobine:
            line_bobine.hide()
        for line_refente in self.lines_refente:
            line_refente.hide()
        for line_papier in self.lines_papier:
            line_papier.hide()
        for line_poly in self.lines_poly:
            line_poly.hide()
        for line_perfo in self.lines_perfo:
            line_perfo.hide()

    def get_line_bobine(self, bobine):
        for line_bobine in self.lines_bobine:
            if line_bobine.objectName() == bobine.code:
                return line_bobine

    def get_line_refente(self, refente):
        for line_refente in self.lines_refente:
            if int(line_refente.objectName()) == refente.code:
                return line_refente

    def get_line_perfo(self, perfo):
        for line_perfo in self.lines_perfo:
            if int(line_perfo.objectName()) == perfo.code:
                return line_perfo

    def get_line_papier(self, bobine):
        for line_papier in self.lines_papier:
            if line_papier.objectName() == bobine.code:
                return line_papier

    def get_line_poly(self, bobine):
        for line_poly in self.lines_poly:
            if line_poly.objectName() == bobine.code:
                return line_poly

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
