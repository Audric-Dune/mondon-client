# !/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QHBoxLayout, QWidget
from PyQt5.QtGui import QDrag
from PyQt5.QtCore import Qt, QMimeData

from commun.ui.public.bobine_fille_ui import BobineFille


class BobineFilleSelected(QWidget):

    def __init__(self, bobine_selected, parent=None):
        super(BobineFilleSelected, self).__init__(parent=parent)
        self.bobine = bobine_selected
        self.hbox = QHBoxLayout()
        self.setFixedHeight(150)
        self.setFixedWidth(self.bobine.laize*self.bobine.pose if self.bobine.pose else self.bobine.laize)
        self.init_widget()

    def init_widget(self):
        self.hbox.setContentsMargins(0, 0, 0, 0)
        self.hbox.setSpacing(0)
        if self.bobine.pose == 0:
            self.hbox.addWidget(BobineFille(parent=self, bobine=self.bobine))
        else:
            count_pose = 0
            while count_pose < self.bobine.pose:
                self.hbox.addWidget(BobineFille(parent=self, bobine=self.bobine))
                count_pose += 1
        self.hbox.addStretch()
        self.setLayout(self.hbox)

    def deleteLater(self):
        from commun.utils.layout import clear_layout
        clear_layout(self.hbox)
        super(BobineFilleSelected, self).deleteLater()

    def mouseMoveEvent(self, e):
        mime_data = QMimeData()
        data = "{}_{}_{}".format(self.bobine.code, self.bobine.pose, self.bobine.index)
        mime_data.setText(data)
        drag = QDrag(self)
        drag.setMimeData(mime_data)
        drag.exec_(Qt.MoveAction)
