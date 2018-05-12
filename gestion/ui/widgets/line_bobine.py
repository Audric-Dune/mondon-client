# !/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QHBoxLayout, QLabel
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QFocusEvent
from commun.ui.public.mondon_widget import MondonWidget
from commun.constants.colors import color_blanc, color_vert_fonce
from commun.constants.stylesheets import black_14_label_stylesheet,\
    red_14_bold_label_stylesheet,\
    black_14_bold_label_stylesheet
from commun.model.bobine_fille import BobineFille


class LineBobine(MondonWidget):
    ON_DBCLICK_SIGNAL = pyqtSignal(BobineFille)

    def __init__(self, parent=None, bobine=None):
        super(LineBobine, self).__init__(parent=parent)
        self.setObjectName(bobine.code)
        self.setFocusPolicy(Qt.ClickFocus)
        self.memo_button_press = 0
        self.setFocus()
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
        code.setFixedWidth(250)
        hbox.addWidget(code)
        laize = QLabel(str(int(self.bobine.laize)))
        laize.setStyleSheet(black_14_label_stylesheet)
        hbox.addWidget(laize, alignment=Qt.AlignCenter)
        color = QLabel(str(self.bobine.color))
        color.setStyleSheet(black_14_label_stylesheet)
        hbox.addWidget(color, alignment=Qt.AlignCenter)
        gr = QLabel("{}g".format(self.bobine.gr))
        gr.setStyleSheet(black_14_label_stylesheet)
        hbox.addWidget(gr, alignment=Qt.AlignCenter)
        lenght = QLabel("{}m".format(self.bobine.lenght))
        lenght.setStyleSheet(black_14_label_stylesheet)
        hbox.addWidget(lenght, alignment=Qt.AlignCenter)
        poses = QLabel(str(self.bobine.poses))
        poses.setStyleSheet(black_14_label_stylesheet)
        hbox.addWidget(poses, alignment=Qt.AlignCenter)
        vente_mensuelle = 1 if 0 < self.bobine.vente_mensuelle < 1 else self.bobine.vente_mensuelle
        vente_mensuelle = str(int(vente_mensuelle))
        vente_mensuelle_label = QLabel(vente_mensuelle)
        vente_mensuelle_label.setStyleSheet(black_14_label_stylesheet)
        hbox.addWidget(vente_mensuelle_label, alignment=Qt.AlignCenter)
        stock = str(int(self.bobine.stock))
        stock_label = QLabel(stock)
        stock_label.setStyleSheet(black_14_label_stylesheet)
        hbox.addWidget(stock_label, alignment=Qt.AlignCenter)
        stock_therme = str(int(self.bobine.stock_therme))
        stock_therme_label = QLabel(stock_therme)
        stock_therme_label.setStyleSheet(black_14_label_stylesheet)
        hbox.addWidget(stock_therme_label, alignment=Qt.AlignCenter)
        etat = self.bobine.etat
        etat_label = QLabel(etat)
        if etat == "RUPTURE":
            etat_label_stylesheet = black_14_bold_label_stylesheet
        elif etat == "SURSTOCK":
            etat_label_stylesheet = red_14_bold_label_stylesheet
        else:
            etat_label_stylesheet = black_14_label_stylesheet
        etat_label.setStyleSheet(etat_label_stylesheet)
        hbox.addWidget(etat_label, alignment=Qt.AlignCenter)
        self.setLayout(hbox)

    def mouseDoubleClickEvent(self, e):
        self.ON_DBCLICK_SIGNAL.emit(self.bobine)
        super(LineBobine, self).mouseDoubleClickEvent(e)

    def mousePressEvent(self, e):
        self.memo_button_press += 1
        if self.memo_button_press > 1:
            focus_out_event = QFocusEvent()
            self.focusOutEvent(focus_out_event)

    def focusInEvent(self, e):
        self.memo_button_press = 0
        self.set_border(color=color_vert_fonce, size=1)
        super(LineBobine, self).focusInEvent(e)

    def focusOutEvent(self, e):
        self.set_border(color=color_vert_fonce, size=0)
        super(LineBobine, self).focusOutEvent(e)
