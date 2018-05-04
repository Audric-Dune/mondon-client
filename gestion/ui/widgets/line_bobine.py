# !/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QHBoxLayout, QLabel
from PyQt5.QtCore import pyqtSignal
from commun.ui.public.mondon_widget import MondonWidget
from commun.constants.colors import color_blanc, color_orange
from commun.constants.stylesheets import black_14_label_stylesheet
from commun.model.bobine_fille import BobineFille


class LineBobine(MondonWidget):
    ON_DBCLICK_SIGNAL = pyqtSignal(BobineFille)

    def __init__(self, parent=None, bobine=None, height=None):
        super(LineBobine, self).__init__(parent=parent)
        self.set_background_color(color_blanc)
        self.bobine = bobine
        self.height = height
        if self.bobine.vente_annuelle and self.bobine.stock_therme and self.bobine.vente_annuelle/12 > self.bobine.stock_therme:
            self.set_background_color(color_orange)
        self.state = None
        self.installEventFilter(self)
        self.init_widget()

    def init_widget(self):
        hbox = QHBoxLayout()
        hbox.setContentsMargins(5, 0, 0, 0)
        self.setLayout(hbox)
        code = QLabel(str(self.bobine.code))
        code.setFixedHeight(self.height)
        code.setStyleSheet(black_14_label_stylesheet)
        code.setFixedWidth(300)
        hbox.addWidget(code)
        laize = QLabel(str(int(self.bobine.laize)))
        laize.setStyleSheet(black_14_label_stylesheet)
        hbox.addWidget(laize)
        # lenght = QLabel("{}m".format(self.bobine.lenght))
        # hbox.addWidget(lenght)
        # gr = QLabel("{}g".format(self.bobine.gr))
        # hbox.addWidget(gr)
        # color = QLabel(str(self.bobine.color))
        # hbox.addWidget(color)
        # # code_cliche = QLabel(str(self.bobine.codes_cliche))
        # # hbox.addWidget(code_cliche)
        # poses = QLabel(str(self.bobine.poses))
        # hbox.addWidget(poses)
        # if self.bobine.vente_annuelle:
        #     vente_annuelle = str(int(self.bobine.vente_annuelle))
        # else:
        #     vente_annuelle = "-"
        # vente_annuelle_label = QLabel(vente_annuelle)
        # hbox.addWidget(vente_annuelle_label)
        # if self.bobine.stock_therme:
        #     stock_therme = str(int(self.bobine.stock_therme))
        # else:
        #     stock_therme = "-"
        # stock_therme_label = QLabel(stock_therme)
        # hbox.addWidget(stock_therme_label)

    def mouseDoubleClickEvent(self, e):
        self.ON_DBCLICK_SIGNAL.emit(self.bobine)
