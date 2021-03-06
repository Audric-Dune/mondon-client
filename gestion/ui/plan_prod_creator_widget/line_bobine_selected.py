# !/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QHBoxLayout, QLabel
from PyQt5.QtCore import Qt

from commun.ui.public.mondon_widget import MondonWidget
from commun.constants.stylesheets import black_14_label_stylesheet,\
    red_14_bold_label_stylesheet,\
    black_14_bold_label_stylesheet, \
    button_delete_bobine_selected_stylesheet
from commun.constants.colors import color_noir
from commun.ui.public.pixmap_button import PixmapButton

from gestion.stores.settings_store import settings_store_gestion


class LineBobineSelected(MondonWidget):

    def __init__(self, bobine, amount, parent=None):
        super(LineBobineSelected, self).__init__(parent=parent)
        self.parent = parent
        self.set_border(color=color_noir)
        self.bobine = bobine
        self.amount = amount
        self.clear_bt = PixmapButton(parent=self)
        self.init_button()
        self.stock_prev_value = 0
        self.production = QLabel()
        self.stock_prev = QLabel()
        self.etat = QLabel()
        self.init_widget()
        self.update_widget()
        self.setFixedHeight(30)

    def init_button(self):
        # Bouton jour plus
        self.clear_bt.setToolTip("Suppression bobine fille")
        self.clear_bt.clicked.connect(self.handle_clicked_bt_delete)
        self.clear_bt.setStyleSheet(button_delete_bobine_selected_stylesheet)
        self.clear_bt.setContentsMargins(0)
        self.clear_bt.setFixedSize(15, 15)
        self.clear_bt.add_image("commun/assets/images/delete.png")

    def init_widget(self):
        hbox = QHBoxLayout()
        hbox.setContentsMargins(0, 0, 5, 0)
        code = QLabel(str(self.bobine.code))
        code.setAlignment(Qt.AlignVCenter)
        code.setStyleSheet(black_14_label_stylesheet)
        code.setFixedWidth(200)
        hbox.addWidget(code)
        laize = QLabel(str(int(self.bobine.laize)))
        laize.setAlignment(Qt.AlignVCenter | Qt.AlignCenter)
        laize.setStyleSheet(black_14_label_stylesheet)
        laize.setFixedWidth(80)
        hbox.addWidget(laize)
        amount = QLabel(str(int(self.amount)))
        amount.setAlignment(Qt.AlignVCenter | Qt.AlignCenter)
        amount.setStyleSheet(black_14_label_stylesheet)
        amount.setFixedWidth(80)
        hbox.addWidget(amount)
        stock_value = str(int(self.bobine.stock_at_time))
        stock = QLabel(stock_value)
        stock.setAlignment(Qt.AlignVCenter | Qt.AlignCenter)
        stock.setStyleSheet(black_14_label_stylesheet)
        hbox.addWidget(stock)
        stock_therme_value = str(int(self.bobine.stock_therme_at_time))
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
        self.etat.setAlignment(Qt.AlignVCenter | Qt.AlignCenter)
        hbox.addWidget(self.etat)
        hbox.addWidget(self.clear_bt)
        self.setLayout(hbox)

    def get_etat(self):
        if self.bobine.vente_mensuelle > self.stock_prev_value:
            return "RUPTURE"
        elif self.bobine.vente_annuelle < self.stock_prev_value:
            return "SURSTOCK"
        return "OK"

    def get_production(self):
        tours = settings_store_gestion.plan_prod.tours
        production = self.amount * tours
        return production

    def update_widget(self):
        self.production.setText("+{}".format(self.get_production()))
        self.stock_prev_value = int(self.get_production()+self.bobine.stock_therme_at_time)
        self.stock_prev.setText(str(self.stock_prev_value))
        etat_value = self.get_etat()
        self.etat.setText(etat_value)
        if etat_value == "RUPTURE":
            etat_label_stylesheet = black_14_bold_label_stylesheet
        elif etat_value == "SURSTOCK":
            etat_label_stylesheet = red_14_bold_label_stylesheet
        else:
            etat_label_stylesheet = black_14_label_stylesheet
        self.etat.setStyleSheet(etat_label_stylesheet)

    def handle_clicked_bt_delete(self):
        from gestion.stores.settings_store import settings_store_gestion
        settings_store_gestion.plan_prod.del_bobine_selected(bobine=self.bobine)
