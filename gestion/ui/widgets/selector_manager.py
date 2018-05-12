# !/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QVBoxLayout
from commun.constants.colors import color_vert_fonce
from commun.ui.public.mondon_widget import MondonWidget
from gestion.ui.widgets.selector import Selector
from gestion.ui.widgets.selector_filter import SelectorFilter
from gestion.stores.filter_store import filter_store


class SelectorManager(MondonWidget):

    def __init__(self, plan_prod, parent):
        super(SelectorManager, self).__init__(parent=parent)
        self.set_background_color(color_vert_fonce)
        self.search_code = None
        self.selector = Selector(parent=self, plan_prod=plan_prod)
        self.selector_filter = SelectorFilter(parent=self)
        self.init_widget()

    def init_widget(self):
        vbox = QVBoxLayout()
        vbox.setSpacing(0)
        vbox.addWidget(self.selector_filter)
        vbox.addWidget(self.selector)
        self.setLayout(vbox)

    def update_widget(self):
        self.selector.update_widget()

    def on_filter_changed(self):
        if filter_store.bloc_focus == "bobine" or not filter_store.bloc_focus:
            self.selector_filter.show()
        else:
            self.selector_filter.hide()
