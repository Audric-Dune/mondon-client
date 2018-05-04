# !/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QVBoxLayout
from commun.constants.colors import color_rouge_clair
from commun.ui.public.mondon_widget import MondonWidget
from gestion.ui.widgets.selector import Selector


class SelectorFilter(MondonWidget):

    def __init__(self, parent=None):
        super(SelectorFilter, self).__init__(parent=parent)
        self.set_background_color(color_rouge_clair)
        self.init_widget()

    def init_widget(self):
        vbox = QVBoxLayout()
        self.setLayout(vbox)