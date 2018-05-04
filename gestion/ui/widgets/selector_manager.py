# !/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QVBoxLayout
from commun.constants.colors import color_vert_fonce
from commun.ui.public.mondon_widget import MondonWidget
from gestion.ui.widgets.selector import Selector


class SelectorManager(MondonWidget):

    def __init__(self, plan_prod, parent=None):
        super(SelectorManager, self).__init__(parent=parent)
        self.set_background_color(color_vert_fonce)
        self.selector = Selector(parent=self, plan_prod=plan_prod)
        self.init_widget()

    def init_widget(self):
        vbox = QVBoxLayout()
        vbox.addWidget(self.selector)
        self.setLayout(vbox)
