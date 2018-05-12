# !/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QVBoxLayout, QWidget
from PyQt5.QtCore import Qt
from commun.constants.colors import color_bleu_gris
from commun.ui.public.mondon_widget import MondonWidget
from gestion.ui.widgets.selector import Selector
from gestion.ui.widgets.selector_filter import SelectorFilter
from gestion.stores.filter_store import filter_store


class SelectorManager(QWidget):

    def __init__(self, plan_prod, parent):
        super(SelectorManager, self).__init__(parent=parent)
        self.setWindowFlags(Qt.Window)
        self.search_code = None
        self.selector = Selector(parent=self, plan_prod=plan_prod)
        self.selector_filter = SelectorFilter(parent=self)
        filter_store.ON_CHANGED_SIGNAL.connect(self.on_filter_changed)
        self.init_widget()

    def init_widget(self):
        vbox = QVBoxLayout()
        vbox.setContentsMargins(5, 0, 5, 5)
        vbox.setSpacing(0)
        vbox.addWidget(self.selector_filter)
        vbox.addWidget(self.selector)
        self.setLayout(vbox)

    def update_widget(self):
        self.selector.update_widget()

    def closeEvent(self, e):
        self.hide()

    def on_filter_changed(self):
        if filter_store.data_type == "bobine" or not filter_store.data_type:
            self.selector_filter.show()
        else:
            self.selector_filter.hide()
