# !/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QHBoxLayout
from commun.constants.colors import color_rouge_clair
from commun.ui.public.mondon_widget import MondonWidget
from commun.ui.public.text_edit import TextEdit


class SelectorFilter(MondonWidget):

    def __init__(self, parent, set_filter_callback):
        super(SelectorFilter, self).__init__(parent=parent)
        self.set_background_color(color_rouge_clair)
        self.set_filter_callback = set_filter_callback
        self.search_code = TextEdit(upper_mode=True)
        self.search_code.textChanged.connect(self.handle_search_code_changed)
        self.setFixedHeight(50)
        self.init_widget()

    def init_widget(self):
        hbox = QHBoxLayout()
        hbox.addWidget(self.search_code)
        self.setLayout(hbox)

    def handle_search_code_changed(self):
        self.set_filter_callback(search_code=self.search_code.text())