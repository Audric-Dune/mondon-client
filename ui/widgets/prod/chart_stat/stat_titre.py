# !/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QHBoxLayout
from ui.widgets.prod.chart_stat.stat_legend import StatLegend

from ui.widgets.prod.chart_stat.stat_bar import StatBar
from ui.widgets.public.mondon_widget import MondonWidget


class StatTitre(MondonWidget):
    def __init__(self, parent):
        super(StatTitre, self).__init__(parent=parent)
        self.stat_legend = StatLegend(parent=self)
        self.stat_bar_matin = StatBar(parent=self, titre="Equipe du matin", moment="matin")
        self.stat_bar_soir = StatBar(parent=self, titre="Equipe du soir", moment="soir")
        self.stat_bar_total = StatBar(parent=self, titre="Journée complète", moment="total")
        self.init_widgets()

    def init_widgets(self):
        hbox = QHBoxLayout(self)
        hbox.setContentsMargins(0, 0, 0, 0)
        self.stat_legend.setFixedWidth(250)
        hbox.addWidget(self.stat_legend)
        hbox.addWidget(self.stat_bar_matin)
        hbox.addWidget(self.stat_bar_soir)
        hbox.addWidget(self.stat_bar_total)

        self.setLayout(hbox)
