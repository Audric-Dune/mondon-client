# !/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QVBoxLayout, QLabel

from commun.utils.layout import clear_layout
from commun.constants.colors import color_blanc
from commun.ui.public.mondon_widget import MondonWidget
from commun.constants.stylesheets import white_12_bold_label_stylesheet, green_12_label_stylesheet, red_12_label_stylesheet


class BlocInformation(MondonWidget):
    def __init__(self, plan_prod, parent=None):
        super(BlocInformation, self).__init__(parent=parent)
        self.set_background_color(color_blanc)
        self.plan_prod = plan_prod
        self.master_vbox = QVBoxLayout()
        self.master_vbox.setContentsMargins(0, 0, 0, 0)
        self.vbox = QVBoxLayout()
        self.label_titre = QLabel("Information")
        self.label_titre.setStyleSheet(white_12_bold_label_stylesheet)
        self.init_ui()
        self.update_widget()

    def init_ui(self):
        self.label_titre.setFixedHeight(30)
        self.master_vbox.addWidget(self.label_titre)
        self.master_vbox.addLayout(self.vbox)
        self.setLayout(self.master_vbox)

    def update_widget(self):
        clear_layout(self.vbox)
        if self.plan_prod.is_completed():
            label_completed = QLabel("Production complète")
            label_completed.setStyleSheet(green_12_label_stylesheet)
            self.vbox.addWidget(label_completed)
        else:
            bobine_poly = "une bobine mère polypro "
            if self.plan_prod.bobine_papier_selected:
                bobine_poly = ""
            perfo = "une campagne de perforation "
            if self.plan_prod.bobine_papier_selected:
                perfo = ""
            bobine_papier = "une bobine mère papier "
            if self.plan_prod.bobine_papier_selected:
                bobine_papier = ""
            refente = "une refente "
            if self.plan_prod.bobine_papier_selected:
                refente = ""
            bobine_fille = "une ou des bobines filles"
            if self.plan_prod.refente_is_completed():
                bobine_fille = ""
            label_not_completed = QLabel("Production imcomplète, il manque : {}{}{}{}{}".format(bobine_poly,
                                                                                                    perfo,
                                                                                                    bobine_papier,
                                                                                                    refente,
                                                                                                    bobine_fille))
            label_not_completed.setStyleSheet(red_12_label_stylesheet)
            self.vbox.addWidget(label_not_completed)
        if not self.plan_prod.tours:
            label_not_tours = QLabel("Aucun nombre de tours rensigné")
            label_not_tours.setStyleSheet(red_12_label_stylesheet)
            self.vbox.addWidget(label_not_tours)
        elif not self.plan_prod.is_valid_tours():
            max_tour = self.plan_prod.get_max_tour()
            text = "La production est trop longue, nombre de tours maximum pour cette production : {}".format(max_tour)
            label_tours_to_hight = QLabel(text)
            label_tours_to_hight.setStyleSheet(red_12_label_stylesheet)
            self.vbox.addWidget(label_tours_to_hight)