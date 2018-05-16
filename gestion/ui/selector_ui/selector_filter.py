# !/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QHBoxLayout, QLabel

from commun.constants.colors import color_bleu_gris, color_blanc
from commun.constants.stylesheets import black_14_label_stylesheet, line_edit_stylesheet
from commun.ui.public.image import Image
from commun.ui.public.mondon_widget import MondonWidget
from commun.ui.public.text_edit import TextEdit
from gestion.stores.filter_store import filter_store
from gestion.ui.selector_ui.selector_collum_filter import SelectorCollumFilter


class SelectorFilter(MondonWidget):

    def __init__(self, parent):
        super(SelectorFilter, self).__init__(parent=parent)
        self.setObjectName("SelectorFilter")
        if filter_store.data_type == "perfo":
            self.setFixedHeight(0)
            self.setMinimumWidth(1100)
        self.set_background_color(color_bleu_gris)
        self.search_code = TextEdit(upper_mode=True)
        self.init_widget()

    def init_widget(self):
        hbox = QHBoxLayout()
        hbox.setSpacing(10)
        if filter_store.data_type == "bobine":
            hbox.addLayout(self.get_search_bar())
        if filter_store.data_type == "bobine":
            for index in range(len(filter_store.list_filter_bobine_fille)):
                hbox.addWidget(SelectorCollumFilter(parent=self,
                                                    title=filter_store.title_filter_bobine_fille[index],
                                                    name_filter=filter_store.list_filter_bobine_fille[index],
                                                    sort_mode=filter_store.sort_mode_bobine_fille[index],
                                                    filter_mode=filter_store.filter_mode_bobine_fille[index]))
        if filter_store.data_type == "poly":
            for index in range(len(filter_store.list_filter_poly)):
                hbox.addWidget(SelectorCollumFilter(parent=self,
                                                    title=filter_store.title_filter_poly[index],
                                                    name_filter=filter_store.list_filter_poly[index],
                                                    sort_mode=filter_store.sort_mode_poly[index],
                                                    filter_mode=filter_store.filter_mode_poly[index]))
        if filter_store.data_type == "refente":
            for index in range(len(filter_store.list_filter_refente)):
                hbox.addWidget(SelectorCollumFilter(parent=self,
                                                    title=filter_store.title_filter_refente[index],
                                                    name_filter=filter_store.list_filter_refente[index],
                                                    sort_mode=filter_store.sort_mode_refente[index],
                                                    filter_mode=filter_store.filter_mode_refente[index]))
        self.setLayout(hbox)

    @staticmethod
    def get_label(text):
        label = QLabel(text)
        label.setStyleSheet(black_14_label_stylesheet)
        return label

    def get_search_bar(self):
        self.search_code.setStyleSheet(line_edit_stylesheet)
        self.search_code.textChanged.connect(self.handle_search_code_changed)
        self.search_code.setFixedWidth(250-21)
        icone_search = Image(parent=self,
                             img="commun/assets/images/icon_search.png",
                             size=21,
                             background_color=color_blanc)
        layout_search_bar = QHBoxLayout()
        layout_search_bar.setSpacing(0)
        layout_search_bar.setContentsMargins(0, 0, 0, 0)
        layout_search_bar.addWidget(self.search_code)
        layout_search_bar.addWidget(icone_search)
        return layout_search_bar

    def handle_search_code_changed(self):
        filter_store.set_search_code(search_code=self.search_code.text())
