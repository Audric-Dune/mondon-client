# !/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLabel, QVBoxLayout

from commun.constants.colors import color_bleu_gris
from commun.constants.stylesheets import white_label_stylesheet
from commun.ui.public.mondon_widget import MondonWidget


class StatLegend(MondonWidget):
    def __init__(self, parent):
        super(StatLegend, self).__init__(parent=parent)
        self.set_background_color(color_bleu_gris)
        self.init_widgets()

    def init_widgets(self):
        vbox = QVBoxLayout(self)

        vbox.addStretch(1)
        titre = QLabel("Notes:")
        titre.setWordWrap(True)
        titre.setAlignment(Qt.AlignVCenter)
        titre.setStyleSheet(white_label_stylesheet)
        vbox.addWidget(titre)

        info_max = QLabel("100%: Production théorique à 172.5m/min de moyenne")
        info_max.setWordWrap(True)
        info_max.setAlignment(Qt.AlignVCenter)
        info_max.setStyleSheet(white_label_stylesheet)
        vbox.addWidget(info_max)

        info_82 = QLabel("82%: Production théorique avec changement de bobine mère")
        info_82.setWordWrap(True)
        info_82.setAlignment(Qt.AlignVCenter)
        info_82.setStyleSheet(white_label_stylesheet)
        vbox.addWidget(info_82)
        vbox.addStretch(1)

        vbox.addStretch()
