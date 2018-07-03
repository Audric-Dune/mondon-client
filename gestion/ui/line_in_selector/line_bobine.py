# !/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QHBoxLayout, QLabel
from PyQt5.QtCore import pyqtSignal, Qt

from commun.ui.public.mondon_widget import MondonWidget
from commun.constants.colors import color_blanc, color_vert_fonce, color_gris_fonce
from commun.constants.stylesheets import black_14_label_stylesheet,\
    red_14_bold_label_stylesheet,\
    black_14_bold_label_stylesheet
from commun.model.bobine_fille_valid import BobineFilleValid
from commun.constants.dimensions import dict_width_selector_bobine, width_search_bar

from gestion.stores.settings_store import settings_store_gestion


class LineBobine(MondonWidget):
    ON_DBCLICK_SIGNAL = pyqtSignal(BobineFilleValid)

    def __init__(self, parent=None, bobine=None):
        super(LineBobine, self).__init__(parent=parent)
        self.setObjectName(bobine.code)
        self.setFocusPolicy(Qt.ClickFocus)
        if bobine.sommeil:
            self.set_background_color(color_gris_fonce)
        else:
            self.set_background_color(color_blanc)
        self.memo_button_press = 0
        self.setFocus()
        self.bobine = bobine
        self.poses = QLabel()
        self.state = None
        self.installEventFilter(self)
        self.init_widget()
        self.update_widget()

    def update_widget(self):
        poses_value = "Neutre" if self.bobine.valid_poses[0] == 0 else self.bobine.valid_poses
        self.poses.setText(str(poses_value))

    def init_widget(self):
        hbox = QHBoxLayout()
        hbox.setContentsMargins(5, 0, 0, 0)
        hbox.setSpacing(10)
        code = QLabel(str(self.bobine.code))
        code.setAlignment(Qt.AlignVCenter)
        code.setStyleSheet(black_14_label_stylesheet)
        code.setFixedWidth(width_search_bar)
        hbox.addWidget(code)
        laize = QLabel(str(int(self.bobine.laize)))
        laize.setAlignment(Qt.AlignVCenter | Qt.AlignCenter)
        laize.setStyleSheet(black_14_label_stylesheet)
        hbox.addWidget(laize)
        color = QLabel(str(self.bobine.color))
        color.setAlignment(Qt.AlignVCenter | Qt.AlignCenter)
        color.setStyleSheet(black_14_label_stylesheet)
        hbox.addWidget(color)
        gr = QLabel("{}g".format(self.bobine.gr))
        gr.setAlignment(Qt.AlignVCenter | Qt.AlignCenter)
        gr.setStyleSheet(black_14_label_stylesheet)
        hbox.addWidget(gr)
        length = QLabel("{}m".format(self.bobine.length))
        length.setAlignment(Qt.AlignVCenter | Qt.AlignCenter)
        length.setStyleSheet(black_14_label_stylesheet)
        hbox.addWidget(length)
        self.poses.setAlignment(Qt.AlignVCenter | Qt.AlignCenter)
        self.poses.setStyleSheet(black_14_label_stylesheet)
        hbox.addWidget(self.poses)
        vente_mensuelle_value = 1 if 0 < self.bobine.vente_mensuelle < 1 else self.bobine.vente_mensuelle
        vente_mensuelle_value = str(int(vente_mensuelle_value))
        vente_mensuelle = QLabel(vente_mensuelle_value)
        vente_mensuelle.setAlignment(Qt.AlignVCenter | Qt.AlignCenter)
        vente_mensuelle.setStyleSheet(black_14_label_stylesheet)
        hbox.addWidget(vente_mensuelle)
        self.bobine.get_stock_at_time(time=settings_store_gestion.plan_prod.start)
        stock_at_time_value = str(int(self.bobine.stock_at_time))
        stock_at_time = QLabel(stock_at_time_value)
        stock_at_time.setAlignment(Qt.AlignVCenter | Qt.AlignCenter)
        stock_at_time.setStyleSheet(black_14_label_stylesheet)
        hbox.addWidget(stock_at_time)
        stock_therme_at_time_value = str(int(self.bobine.stock_therme_at_time))
        stock_therme_at_time = QLabel(stock_therme_at_time_value)
        stock_therme_at_time.setAlignment(Qt.AlignVCenter | Qt.AlignCenter)
        stock_therme_at_time.setStyleSheet(black_14_label_stylesheet)
        hbox.addWidget(stock_therme_at_time)
        etat_value = self.bobine.etat
        etat = QLabel(etat_value)
        etat.setAlignment(Qt.AlignVCenter | Qt.AlignCenter)
        if etat_value == "RUPTURE":
            etat_label_stylesheet = black_14_bold_label_stylesheet
        elif etat_value == "SURSTOCK":
            etat_label_stylesheet = red_14_bold_label_stylesheet
        else:
            etat_label_stylesheet = black_14_label_stylesheet
        etat.setStyleSheet(etat_label_stylesheet)
        hbox.addWidget(etat)
        sommeil_value = self.bobine.sommeil
        sommeil = QLabel(sommeil_value)
        sommeil.setAlignment(Qt.AlignVCenter | Qt.AlignCenter)
        sommeil.setStyleSheet(black_14_label_stylesheet)
        hbox.addWidget(sommeil)
        for key in dict_width_selector_bobine.keys():
            vars()[key].setMinimumWidth(dict_width_selector_bobine[key])
        self.setLayout(hbox)

    def mouseDoubleClickEvent(self, e):
        self.ON_DBCLICK_SIGNAL.emit(self.bobine)
        super(LineBobine, self).mouseDoubleClickEvent(e)

    def mousePressEvent(self, e):
        self.memo_button_press += 1
        if self.memo_button_press > 1:
            self.clearFocus()
        super(LineBobine, self).mousePressEvent(e)

    def focusInEvent(self, e):
        self.memo_button_press = 0
        self.set_border(color=color_vert_fonce, size=1)
        super(LineBobine, self).focusInEvent(e)

    def focusOutEvent(self, e):
        self.set_border(color=color_vert_fonce, size=0)
        super(LineBobine, self).focusOutEvent(e)
