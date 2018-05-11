# !/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QHBoxLayout, QLabel
from PyQt5.QtCore import pyqtSignal
from commun.ui.public.mondon_widget import MondonWidget
from commun.constants.colors import color_blanc
from commun.constants.stylesheets import black_14_label_stylesheet,\
    red_14_bold_label_stylesheet,\
    black_14_bold_label_stylesheet
from commun.model.bobine_fille import BobineFille


class LineBobine(MondonWidget):
    ON_DBCLICK_SIGNAL = pyqtSignal(BobineFille)

    def __init__(self, parent=None, bobine=None):
        super(LineBobine, self).__init__(parent=parent)
        self.setObjectName(bobine.code)
        self.set_background_color(color_blanc)
        self.bobine = bobine
        self.state = None
        self.installEventFilter(self)
        self.init_widget()

    def init_widget(self):
        hbox = QHBoxLayout()
        hbox.setContentsMargins(5, 0, 0, 0)
        hbox.setSpacing(10)
        code = QLabel(str(self.bobine.code))
        code.setStyleSheet(black_14_label_stylesheet)
        code.setFixedWidth(300)
        hbox.addWidget(code)
        laize = QLabel(str(int(self.bobine.laize)))
        laize.setStyleSheet(black_14_label_stylesheet)
        hbox.addWidget(laize)
        color = QLabel(str(self.bobine.color))
        color.setStyleSheet(black_14_label_stylesheet)
        hbox.addWidget(color)
        gr = QLabel("{}g".format(self.bobine.gr))
        gr.setStyleSheet(black_14_label_stylesheet)
        hbox.addWidget(gr)
        lenght = QLabel("{}m".format(self.bobine.lenght))
        lenght.setStyleSheet(black_14_label_stylesheet)
        hbox.addWidget(lenght)
        poses = QLabel(str(self.bobine.poses))
        poses.setStyleSheet(black_14_label_stylesheet)
        hbox.addWidget(poses)
        vente_mensuelle = 1 if 0 < self.bobine.vente_mensuelle < 1 else self.bobine.vente_mensuelle
        vente_mensuelle = str(int(vente_mensuelle))
        vente_mensuelle_label = QLabel(vente_mensuelle)
        vente_mensuelle_label.setStyleSheet(black_14_label_stylesheet)
        hbox.addWidget(vente_mensuelle_label)
        stock = str(int(self.bobine.stock))
        stock_label = QLabel(stock)
        stock_label.setStyleSheet(black_14_label_stylesheet)
        hbox.addWidget(stock_label)
        stock_therme = str(int(self.bobine.stock_therme))
        stock_therme_label = QLabel(stock_therme)
        stock_therme_label.setStyleSheet(black_14_label_stylesheet)
        hbox.addWidget(stock_therme_label)
        etat = self.bobine.etat
        etat_label = QLabel(etat)
        if etat == "RUPTURE":
            etat_label_stylesheet = black_14_bold_label_stylesheet
        elif etat == "SURSTOCK":
            etat_label_stylesheet = red_14_bold_label_stylesheet
        else:
            etat_label_stylesheet = black_14_label_stylesheet
        etat_label.setStyleSheet(etat_label_stylesheet)
        hbox.addWidget(etat_label)
        self.setLayout(hbox)

    def mouseDoubleClickEvent(self, e):
        self.ON_DBCLICK_SIGNAL.emit(self.bobine)
