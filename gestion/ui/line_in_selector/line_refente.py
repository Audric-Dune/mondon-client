# !/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QHBoxLayout, QLabel
from PyQt5.QtCore import pyqtSignal, Qt

from gestion.ui.line_in_selector.line_selector import LineSelector
from commun.constants.stylesheets import black_14_label_stylesheet
from commun.model.refente import Refente
from commun.ui.public.refente_ui import RefenteUi
from commun.constants.colors import color_blanc
from commun.constants.dimensions import dict_width_selector_refente


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
        self.hbox.setContentsMargins(5, 5, 0, 5)
        self.hbox.setSpacing(10)
        code_perfo = QLabel("Perfo. " + chr(96 + refente.code_perfo).capitalize())
        code_perfo.setStyleSheet(black_14_label_stylesheet)
        self.hbox.addWidget(code_perfo)
        refente_ui = RefenteUi(refente=refente)
        self.hbox.addWidget(refente_ui)
        laize = QLabel(str(refente.laize))
        laize.setAlignment(Qt.AlignCenter)
        laize.setStyleSheet(black_14_label_stylesheet)
        self.hbox.addWidget(laize)
        for key in dict_width_selector_refente.keys():
            if key == "laize_fille":
                refente_ui.setMinimumWidth(dict_width_selector_refente[key])
                continue
            vars()[key].setMinimumWidth(dict_width_selector_refente[key])
        self.hbox.addStretch(0)
        self.setLayout(self.hbox)

    def mouseDoubleClickEvent(self, e):
        self.ON_DBCLICK_SIGNAL.emit(self.refente)
