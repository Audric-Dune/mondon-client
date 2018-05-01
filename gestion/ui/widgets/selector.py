# !/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QScrollArea, QVBoxLayout, QWidget, QLabel
from PyQt5.QtCore import Qt
from commun.constants.colors import color_bleu_gris
from commun.constants.stylesheets import scroll_bar_stylesheet, white_12_bold_label_stylesheet
from commun.ui.public.mondon_widget import MondonWidget
from commun.utils.layout import clear_layout
from gestion.ui.widgets.line_bobine import LineBobine
from gestion.ui.widgets.line_refente import LineRefente
from gestion.ui.widgets.line_perfo import LinePerfo
from gestion.ui.widgets.line_bobine_papier import LineBobinePapier
from gestion.ui.widgets.line_bobine_poly import LineBobinePoly
from gestion.ui.widgets.selector_pose import SelectorPose
from gestion.stores.settings_store import settings_store_gestion


class Selector(MondonWidget):

    def __init__(self, plan_prod, parent=None):
        super(Selector, self).__init__(parent=parent)
        self.plan_prod = plan_prod
        self.parent = parent
        self.sort_name = "code"
        self.sort_asc = True
        self.current_focus = "perfo"
        self.background_color = color_bleu_gris
        self.master_vbox = QVBoxLayout()
        self.master_vbox.setContentsMargins(0, 0, 0, 0)
        self.master_vbox.setSpacing(0)
        self.selector_pose = None
        self.vbox = QVBoxLayout()
        self.titre = QLabel()
        self.scroll_bar = QScrollArea(parent=self)
        self.content_scrollbar = QWidget(parent=self.scroll_bar)
        self.init_widget()
        self.update_widget()

    def init_widget(self):
        self.content_scrollbar.setLayout(self.vbox)
        self.scroll_bar.setWidget(self.content_scrollbar)
        self.scroll_bar.setStyleSheet(scroll_bar_stylesheet)
        self.scroll_bar.setWidgetResizable(True)
        self.titre.setFixedHeight(30)
        self.titre.setStyleSheet(white_12_bold_label_stylesheet)
        self.titre.setContentsMargins(5, 0, 0, 0)
        self.master_vbox.addWidget(self.titre, Qt.AlignVCenter)
        self.master_vbox.addWidget(self.scroll_bar)
        self.setLayout(self.master_vbox)

    def sort_bobine(self):
        self.plan_prod.current_bobine_fille_store.sort_bobines("code", True)
        self.plan_prod.current_bobine_fille_store.sort_bobines(self.sort_name, self.sort_asc)

    def update_widget(self):
        self.sort_bobine()
        self.current_focus = self.parent.bloc_focus
        clear_layout(self.vbox)
        # MODE NORMAL
        if self.current_focus == "bobine" or not self.current_focus:
            self.titre.setText("SELECTION BOBINE FILLE")
            for bobine in self.plan_prod.current_bobine_fille_store.bobines:
                line_bobine = LineBobine(parent=self, bobine=bobine)
                line_bobine.ON_DBCLICK_SIGNAL.connect(self.handle_selected_bobine)
                line_bobine.setFixedHeight(20)
                self.vbox.addWidget(line_bobine)
        # # MODE DEBUG
        # if self.current_focus == "bobine" or not self.current_focus:
        #     self.titre.setText("SELECTION BOBINE FILLE MODE DEBUG")
        #     for bobine in bobine_fille_store.bobines:
        #         if bobine in self.plan_prod.current_bobine_fille_store.bobines:
        #             disabled = False
        #         else:
        #             disabled = True
        #         line_bobine = LineBobine(parent=self, bobine=bobine, disabled=disabled)
        #         line_bobine.ON_DBCLICK_SIGNAL.connect(self.handle_selected_bobine)
        #         line_bobine.setFixedHeight(20)
        #         self.vbox.addWidget(line_bobine)
        if self.current_focus == "refente":
            self.titre.setText("SELECTION REFENTE")
            for refente in self.plan_prod.current_refente_store.refentes:
                line_refente = LineRefente(parent=self, refente=refente, ech=settings_store_gestion.ech)
                line_refente.ON_DBCLICK_SIGNAL.connect(self.handle_selected_refente)
                self.vbox.addWidget(line_refente)
        if self.current_focus == "perfo":
            self.titre.setText("SELECTION PERFO")
            for perfo in self.plan_prod.current_perfo_store.perfos:
                line_perfo = LinePerfo(parent=self, perfo=perfo, ech=settings_store_gestion.ech)
                line_perfo.ON_DBCLICK_SIGNAL.connect(self.handle_selected_perfo)
                self.vbox.addWidget(line_perfo)
        if self.current_focus == "papier":
            self.titre.setText("SELECTION BOBINE PAPIER")
            for bobine in self.plan_prod.current_bobine_papier_store.bobines:
                line_bobine_papier = LineBobinePapier(parent=self, bobine=bobine)
                line_bobine_papier.ON_DBCLICK_SIGNAL.connect(self.handle_selected_bobine_papier)
                line_bobine_papier.setFixedHeight(20)
                self.vbox.addWidget(line_bobine_papier)
        if self.current_focus == "poly":
            self.titre.setText("SELECTION BOBINE POLYPRO")
            for bobine in self.plan_prod.current_bobine_poly_store.bobines:
                line_bobine_poly = LineBobinePoly(parent=self, bobine=bobine)
                line_bobine_poly.ON_DBCLICK_SIGNAL.connect(self.handle_selected_bobine_poly)
                line_bobine_poly.setFixedHeight(20)
                self.vbox.addWidget(line_bobine_poly)
        self.vbox.addStretch(0)
        self.update()

    def handle_selected_bobine(self, bobine, pose=None):
        if pose:
            self.plan_prod.add_bobine_selected(bobine, pose)
        elif len(bobine.poses) == 1:
            self.plan_prod.add_bobine_selected(bobine, bobine.poses[0])
        else:
            self.selector_pose = SelectorPose(self.handle_selected_bobine, bobine)
            self.selector_pose.show()

    def handle_selected_refente(self, refente):
        self.plan_prod.add_refente_selected(refente)

    def handle_selected_perfo(self, perfo):
        self.plan_prod.add_perfo_selected(perfo)

    def handle_selected_bobine_papier(self, bobine):
        self.plan_prod.add_bobine_papier_selected(bobine)

    def handle_selected_bobine_poly(self, bobine):
        self.plan_prod.add_bobine_poly_selected(bobine)
