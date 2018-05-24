# !/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QHBoxLayout, QWidget

from commun.ui.public.bobine_fille_ui import BobineFille


class BobineFilleSelected(QWidget):

    def __init__(self, bobine_selected, parent=None):
        super(BobineFilleSelected, self).__init__(parent=parent)
        self.bobine = bobine_selected
        self.init_widget()

    def init_widget(self):
        hbox = QHBoxLayout()
        hbox.setContentsMargins(0, 0, 0, 0)
        hbox.setSpacing(0)
        if self.bobine.pose == 0:
            hbox.addWidget(BobineFille(parent=self, bobine=self.bobine))
        else:
            count_pose = 0
            while count_pose < self.bobine.pose:
                hbox.addWidget(BobineFille(parent=self, bobine=self.bobine))
                count_pose += 1
        hbox.addStretch()
        self.setLayout(hbox)
