# !/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QHBoxLayout, QLabel

from commun.constants.colors import color_rouge_clair, color_blanc
from commun.constants.stylesheets import black_14_label_stylesheet, line_edit_stylesheet
from commun.ui.public.mondon_widget import MondonWidget
from commun.ui.public.text_edit import TextEdit
from commun.ui.public.image import Image
from gestion.ui.widgets.selector_collum_filter import SelectorCollumFilter


class SelectorFilter(MondonWidget):

    def __init__(self, parent, set_filter_callback):
        super(SelectorFilter, self).__init__(parent=parent)
        self.set_background_color(color_rouge_clair)
        self.set_filter_callback = set_filter_callback
        self.setFixedHeight(50)
        self.init_widget()

    def init_widget(self):
        hbox = QHBoxLayout()
        hbox.setSpacing(10)
        hbox.addLayout(self.get_search_bar())
        hbox.addWidget(SelectorCollumFilter(parent=self, set_filter_callback=self.set_filter_callback))
        self.setLayout(hbox)

    @staticmethod
    def get_label(text):
        label = QLabel(text)
        label.setStyleSheet(black_14_label_stylesheet)
        return label

    def get_search_bar(self):
        search_code = TextEdit(upper_mode=True)
        search_code.setStyleSheet(line_edit_stylesheet)
        search_code.textChanged.connect(self.handle_search_code_changed)
        search_code.setFixedWidth(300-21)
        icone_search = Image(parent=self,
                             img="commun/assets/images/icon_search.png",
                             size=21,
                             background_color=color_blanc)
        layout_search_bar = QHBoxLayout()
        layout_search_bar.setSpacing(0)
        layout_search_bar.setContentsMargins(0, 0, 0, 0)
        layout_search_bar.addWidget(search_code)
        layout_search_bar.addWidget(icone_search)
        return layout_search_bar

    def handle_search_code_changed(self):
        self.set_filter_callback(search_code=self.search_code.text())