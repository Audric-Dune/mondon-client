# !/usr/bin/env python
# -*- coding: utf-8 -*-

# Importation des module PyQt5
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QHBoxLayout, QSizePolicy
from stores.settings_store import settings_store
from ui.widgets.mondon_widget import MondonWidget
from ui.widgets.stat_bar import StatBar
from ui.widgets.stat_legend import StatLegend


class StatMenu(MondonWidget):
    def __init__(self, parent):
        super(StatMenu, self).__init__(parent=parent)
        self.day_ago = 0
        self.init_widgets()

    def init_widgets(self):
        hbox = QHBoxLayout(self)
        hbox.setContentsMargins(0, 0, 0, 0)

        stat_legend = StatLegend(parent=self)
        stat_legend.setFixedWidth(250)
        hbox.addWidget(stat_legend)

        stat_bar = StatBar(parent=self, titre="Equipe du matin", moment="matin")
        stat_bar.setSizePolicy(QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding))
        hbox.addWidget(stat_bar)

        stat_bar2 = StatBar(parent=self, titre="Equipe du soir", moment="soir")
        stat_bar2.setSizePolicy(QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding))
        hbox.addWidget(stat_bar2)

        stat_bar3 = StatBar(parent=self, titre="Journée complète", moment="total")
        stat_bar3.setSizePolicy(QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding))
        hbox.addWidget(stat_bar3)

        self.setLayout(hbox)

    def on_settings_changed(self, prev_live, prev_day_ago, prev_zoom):
        self.day_ago = settings_store.day_ago
        self.update()

    def on_data_changed(self):
        self.update()

    def paintEvent(self, event):
        p = QPainter()
        p.begin(self)
        self.draw(p)
        p.end()

    def draw(self, p):
        pass
