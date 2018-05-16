# !/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QHBoxLayout, QLabel
from PyQt5.QtCore import pyqtSignal

from gestion.ui.line_in_selector.line_selector import LineSelector
from commun.constants.stylesheets import black_14_label_stylesheet
from commun.model.refente import Refente
from commun.ui.public.refente_ui import RefenteUi
from commun.constants.colors import color_blanc


class LineRefente(LineSelector):
    ON_DBCLICK_SIGNAL = pyqtSignal(Refente)

    def __init__(self, parent=None, refente=None, ech=1, bobines=None):
        super(LineRefente, self).__init__(parent=parent)
        self.set_background_color(color_blanc)
        self.setObjectName(str(refente.code))
        self.bobines = bobines
        self.ech = ech
        self.refente = refente
        self.hbox = QHBoxLayout()
        self.init_widget(refente)

    def init_widget(self, refente):
        self.hbox.setSpacing(30)
        label_refente = QLabel("Perfo. " + chr(96 + refente.code_perfo).capitalize())
        label_refente.setStyleSheet(black_14_label_stylesheet)
        self.hbox.addWidget(label_refente)
        self.hbox.addWidget(RefenteUi(refente=refente))
        label_laize = QLabel(str(refente.laize))
        label_laize.setStyleSheet(black_14_label_stylesheet)
        self.hbox.addWidget(label_laize)
        self.hbox.addStretch(0)
        self.setLayout(self.hbox)

    def mouseDoubleClickEvent(self, e):
        self.ON_DBCLICK_SIGNAL.emit(self.refente)
