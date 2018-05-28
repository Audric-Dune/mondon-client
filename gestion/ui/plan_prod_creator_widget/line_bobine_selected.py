# !/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QHBoxLayout, QLabel
from PyQt5.QtCore import Qt

from commun.ui.public.mondon_widget import MondonWidget
from commun.constants.stylesheets import black_14_label_stylesheet,\
    red_14_bold_label_stylesheet,\
    black_14_bold_label_stylesheet

from gestion.stores.settings_store import settings_store_gestion


class LineBobineSelected(MondonWidget):

    def __init__(self, bobine, amount, parent=None):
        super(LineBobineSelected, self).__init__(parent=parent)
        self.bobine = bobine
        self.amount = amount
        self.production = QLabel()
        self.stock_prev = QLabel()
        self.init_widget()
        self.update_widget()

    def init_widget(self):
        hbox = QHBoxLayout()
        hbox.setContentsMargins(0, 0, 0, 0)
        code = QLabel(str(self.bobine.code))
        code.setAlignment(Qt.AlignVCenter)
        code.setStyleSheet(black_14_label_stylesheet)
        hbox.addWidget(code)
        laize = QLabel(str(int(self.bobine.laize)))
        laize.setAlignment(Qt.AlignVCenter | Qt.AlignCenter)
        laize.setStyleSheet(black_14_label_stylesheet)
        hbox.addWidget(laize)
        amount = QLabel(str(int(self.amount)))
        amount.setAlignment(Qt.AlignVCenter | Qt.AlignCenter)
        amount.setStyleSheet(black_14_label_stylesheet)
        hbox.addWidget(amount)
        stock_value = str(int(self.bobine.stock))
        stock = QLabel(stock_value)
        stock.setAlignment(Qt.AlignVCenter | Qt.AlignCenter)
        stock.setStyleSheet(black_14_label_stylesheet)
        hbox.addWidget(stock)
        stock_therme_value = str(int(self.bobine.stock_therme))
        stock_therme = QLabel(stock_therme_value)
        stock_therme.setAlignment(Qt.AlignVCenter | Qt.AlignCenter)
        stock_therme.setStyleSheet(black_14_label_stylesheet)
        hbox.addWidget(stock_therme)
        self.production.setAlignment(Qt.AlignVCenter | Qt.AlignCenter)
        self.production.setStyleSheet(black_14_bold_label_stylesheet)
        hbox.addWidget(self.production)
        self.stock_prev.setAlignment(Qt.AlignVCenter | Qt.AlignCenter)
        self.stock_prev.setStyleSheet(black_14_bold_label_stylesheet)
        hbox.addWidget(self.stock_prev)
        etat_value = self.bobine.etat
        etat = QLabel(etat_value)
        etat.setAlignment(Qt.AlignVCenter | Qt.AlignCenter)
        if etat_value == "RUPTURE":
            etat_label_stylesheet = black_14_bold_label_stylesheet
        elif etat_value == "SURSTOCK":
            etat_label_stylesheet = red_14_bold_label_stylesheet
        else:
            etat.setText("OK")
            etat_label_stylesheet = black_14_label_stylesheet
        etat.setStyleSheet(etat_label_stylesheet)
        hbox.addWidget(etat)
        self.setLayout(hbox)

    def get_production(self):
        tours = settings_store_gestion.plan_prod.tours
        production = self.amount * tours
        return production

    def update_widget(self):
        self.production.setText("+{}".format(self.get_production()))
        self.stock_prev.setText(str(int(self.get_production()+self.bobine.stock)))
