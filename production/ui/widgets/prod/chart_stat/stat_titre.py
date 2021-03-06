# !/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QHBoxLayout

from commun.ui.public.mondon_widget import MondonWidget

from production.ui.widgets.prod.chart_stat.stat_bar import StatBar
from production.ui.widgets.prod.chart_stat.stat_legend import StatLegend


class StatTitre(MondonWidget):
    def __init__(self, parent=None, note=True):
        super(StatTitre, self).__init__(parent=parent)
        self.stat_legend = StatLegend(parent=self)
        self.stat_bar_matin = StatBar(parent=self, titre="Equipe du matin", moment="matin")
        self.stat_bar_soir = StatBar(parent=self, titre="Equipe du soir", moment="soir")
        self.stat_bar_total = StatBar(parent=self, titre="Journée complète", moment="total")
        self.init_widgets(note)

    def init_widgets(self, note):
        hbox = QHBoxLayout(self)
        hbox.setContentsMargins(0, 0, 0, 0)
        self.stat_legend.setFixedWidth(250)
        if note:
            hbox.addWidget(self.stat_legend)
        hbox.addWidget(self.stat_bar_matin)
        hbox.addWidget(self.stat_bar_soir)
        hbox.addWidget(self.stat_bar_total)

        self.setLayout(hbox)
