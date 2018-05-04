# !/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QVBoxLayout
from commun.constants.colors import color_vert_fonce
from commun.ui.public.mondon_widget import MondonWidget
from gestion.ui.widgets.selector import Selector
from gestion.ui.widgets.selector_filter import SelectorFilter


class SelectorManager(MondonWidget):

    def __init__(self, plan_prod, parent):
        super(SelectorManager, self).__init__(parent=parent)
        self.set_background_color(color_vert_fonce)
        self.search_code = None
        self.bloc_focus = "bobine"
        self.selector = Selector(parent=self, plan_prod=plan_prod)
        self.selector_filter = SelectorFilter(parent=self, set_filter_callback=self.set_filter)
        self.init_widget()

    def init_widget(self):
        vbox = QVBoxLayout()
        vbox.setSpacing(0)
        vbox.addWidget(self.selector_filter)
        vbox.addWidget(self.selector)
        self.setLayout(vbox)

    def update_widget(self, bloc_focus):
        self.bloc_focus = bloc_focus

    def set_filter(self, search_code=None):
        if search_code is not None:
            self.search_code = search_code
        self.selector.update_list(search_code)
