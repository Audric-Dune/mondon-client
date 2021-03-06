# !/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QScrollArea, QVBoxLayout, QWidget
from PyQt5.Qt import Qt

from gestion.ui.line_in_selector.line_bobine_poly import LineBobinePoly
from gestion.ui.line_in_selector.line_perfo import LinePerfo
from gestion.ui.line_in_selector.line_refente import LineRefente

from commun.constants.colors import color_bleu_gris
from commun.constants.stylesheets import scroll_bar_stylesheet
from commun.ui.public.mondon_widget import MondonWidget
from gestion.stores.filter_store import filter_store
from gestion.stores.settings_store import settings_store_gestion
from gestion.ui.line_in_selector.line_bobine_papier import LineBobinePapier


class Selector(MondonWidget):

    def __init__(self, plan_prod, parent):
        super(Selector, self).__init__(parent=parent)
        self.plan_prod = plan_prod
        self.parent = parent
        self.list_poly = []
        self.list_refente = []
        self.list_papier = []
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
        self.scroll_bar.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.content_scrollbar = QWidget(parent=self.scroll_bar)
        self.init_lists_lines()
        self.init_widget()
        self.update_widget()

    def init_lists_lines(self):
        self.init_list_lines_refente()
        self.init_list_lines_perfo()
        self.init_list_lines_papier()
        self.init_list_lines_poly()

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
        self.master_vbox.addWidget(self.scroll_bar)
        self.setLayout(self.master_vbox)

    def on_filter_changed(self):
        self.update_widget()

    def sort_bobine(self):
        if filter_store.data_type == "poly":
            self.list_poly = self.sort_item(self.list_poly, "code", True)
            self.list_poly = self.sort_item(self.list_poly, filter_store.sort_name, filter_store.sort_asc)
        if filter_store.data_type == "papier":
            self.list_papier = self.sort_item(self.list_papier, "code", True)
            self.list_papier = self.sort_item(self.list_papier, filter_store.sort_name, filter_store.sort_asc)
        if filter_store.data_type == "refente":
            self.list_refente = self.sort_item(self.list_refente, "laize", True)
            self.list_refente = self.sort_item(self.list_refente, filter_store.sort_name, filter_store.sort_asc)

    @staticmethod
    def sort_item(items, sort_name, sort_asc):
        items = sorted(items, key=lambda b: b.get_value(sort_name), reverse=not sort_asc)
        return items

    def update_list(self):
        if filter_store.data_type == "poly":
            self.list_poly = []
            for poly in self.plan_prod.current_bobine_poly_store.bobines:
                if self.is_valid_poly_from_filters(poly):
                    self.list_poly.append(poly)
        if filter_store.data_type == "papier":
            self.list_papier = []
            for papier in self.plan_prod.current_bobine_papier_store.bobines:
                if self.is_valid_papier_from_filters(papier):
                    self.list_papier.append(papier)
        if filter_store.data_type == "refente":
            self.list_refente = []
            for refente in self.plan_prod.current_refente_store.refentes:
                if self.is_valid_refente_from_filters(refente):
                    self.list_refente.append(refente)

    def is_valid_poly_from_filters(self, poly):
        from gestion.stores.filter_store import filter_store
        for name in filter_store.list_filter_poly:
            if not self.is_valid_poly_from_filter(poly, name):
                return False
        return True

    @staticmethod
    def is_valid_poly_from_filter(poly, name):
        dict_filter = filter_store.dicts_filter[name]
        if name == "famille":
            return True
        else:
            for key in dict_filter.keys():
                if key == getattr(poly, name) and dict_filter[key]:
                    return True
            return False

    def is_valid_papier_from_filters(self, papier):
        from gestion.stores.filter_store import filter_store
        for name in filter_store.list_filter_papier:
            if not self.is_valid_papier_from_filter(papier, name):
                return False
        return True

    @staticmethod
    def is_valid_papier_from_filter(papier, name):
        dict_filter = filter_store.dicts_filter[name]
        for key in dict_filter.keys():
            if key == getattr(papier, name) and dict_filter[key]:
                return True
        return False

    def is_valid_refente_from_filters(self, refente):
        from gestion.stores.filter_store import filter_store
        for name in filter_store.list_filter_refente:
            if not self.is_valid_refente_from_filter(refente, name):
                return False
        return True

    @staticmethod
    def is_valid_refente_from_filter(refente, name):
        dict_filter = filter_store.dicts_filter[name]
        if name == "laize_fille":
            for key in dict_filter.keys():
                for laize in refente.laizes:
                    if key == laize and dict_filter[key]:
                        return True
            return False
        else:
            for key in dict_filter.keys():
                if key == getattr(refente, name) and dict_filter[key]:
                    return True
        return False

    def update_widget(self):
        self.update_list()
        self.sort_bobine()
        current_data_type = filter_store.data_type
        self.hide_lines()
        self.vbox.takeAt(self.vbox.count()-1)
        if current_data_type == "refente":
            for refente in self.list_refente:
                line_refente = self.get_line_refente(refente)
                line_refente.show()
                self.vbox.addWidget(line_refente)
        if current_data_type == "perfo":
            for perfo in self.plan_prod.current_perfo_store.perfos:
                line_perfo = self.get_line_perfo(perfo)
                line_perfo.show()
                self.vbox.addWidget(line_perfo)
        if current_data_type == "papier":
            for bobine in self.list_papier:
                line_bobine_papier = self.get_line_papier(bobine)
                line_bobine_papier.show()
                self.vbox.addWidget(line_bobine_papier)
        if current_data_type == "poly":
            for bobine in self.list_poly:
                line_bobine_poly = self.get_line_poly(bobine)
                line_bobine_poly.show()
                self.vbox.addWidget(line_bobine_poly)
        self.vbox.addStretch()
        self.resize_window()

    def resize_window(self):
        self.setMinimumHeight(500)

    def hide_lines(self):
        for line_refente in self.lines_refente:
            line_refente.hide()
        for line_papier in self.lines_papier:
            line_papier.hide()
        for line_poly in self.lines_poly:
            line_poly.hide()
        for line_perfo in self.lines_perfo:
            line_perfo.hide()

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

    def handle_selected_refente(self, refente):
        self.plan_prod.add_refente_selected(refente)

    def handle_selected_perfo(self, perfo):
        self.plan_prod.add_perfo_selected(perfo)

    def handle_selected_bobine_papier(self, bobine):
        self.plan_prod.add_bobine_papier_selected(bobine)

    def handle_selected_bobine_poly(self, bobine):
        self.plan_prod.add_bobine_poly_selected(bobine)
