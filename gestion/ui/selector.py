# !/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QScrollArea, QVBoxLayout, QWidget
from commun.constants.colors import color_bleu_gris
from commun.constants.stylesheets import scroll_bar_stylesheet
from commun.ui.public.mondon_widget import MondonWidget
from commun.utils.layout import clear_layout
from gestion.ui.line_bobine import LigneBobine
from gestion.ui.line_refente import LigneRefente
from gestion.ui.line_perfo import LinePerfo


class Selector(MondonWidget):

    def __init__(self, plan_prod, parent=None):
        super(Selector, self).__init__(parent=parent)
        self.plan_prod = plan_prod
        self.current_focus = "refente"
        self.background_color = color_bleu_gris
        self.master_vbox = QVBoxLayout()
        self.vbox = QVBoxLayout()
        self.scroll_bar = QScrollArea(parent=self)
        self.content_scrollbar = QWidget(parent=self.scroll_bar)
        self.init_widget()
        self.update_widget()

    def init_widget(self):
        self.content_scrollbar.setLayout(self.vbox)
        self.scroll_bar.setWidget(self.content_scrollbar)
        self.scroll_bar.setStyleSheet(scroll_bar_stylesheet)
        self.scroll_bar.setWidgetResizable(True)
        self.master_vbox.addWidget(self.scroll_bar)
        self.setLayout(self.master_vbox)

    def update_widget(self):
        clear_layout(self.vbox)
        if self.current_focus == "bobine":
            for bobine in self.plan_prod.bobine_fille_store.bobines:
                line_bobine = LigneBobine(parent=self, bobine=bobine)
                line_bobine.setFixedHeight(20)
                self.vbox.addWidget(line_bobine)
        if self.current_focus == "refente":
            for refente in self.plan_prod.refente_store.refentes:
                line_refente = LigneRefente(parent=self, refente=refente)
                self.vbox.addWidget(line_refente)
        if self.current_focus == "perfo":
            for perfo in self.plan_prod.perfo_store.perfos:
                line_perfo = LinePerfo(parent=self, perfo=perfo)
                self.vbox.addWidget(line_perfo)
        self.vbox.addStretch(0)
