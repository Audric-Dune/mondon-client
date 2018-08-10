# !/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QHBoxLayout, QWidget
from PyQt5.QtGui import QPen, QPainter, QColor, QDrag

from commun.constants.colors import color_blanc
from commun.utils.layout import clear_layout
from commun.ui.public.cliche_ui import ClicheUi
from PyQt5.QtCore import Qt, QMimeData


class LineEncrier(QWidget):

    def __init__(self, parent=None, encrier=None, index=None):
        super(LineEncrier, self).__init__(parent=parent)
        self.setFixedHeight(80)
        self.encrier = encrier
        self.index = index
        self.hbox = QHBoxLayout()
        self.init_widget()
        self.update_widget()

    def mouseMoveEvent(self, e):
        mime_data = QMimeData()
        mime_data.setText(str(self.index))
        drag = QDrag(self)
        drag.setMimeData(mime_data)
        drag.exec_(Qt.MoveAction)

    def init_widget(self):
        self.hbox.setContentsMargins(10, 0, 0, 10)
        self.hbox.setSpacing(0)
        self.setLayout(self.hbox)

    def update_widget(self):
        clear_layout(self.hbox)
        refente = self.encrier.refente
        if refente:
            self.hbox.addSpacing(980-refente.laize-refente.dec)
        else:
            self.hbox.addStretch()
        current_index = 0
        new_index = 0
        if refente:
            while current_index < 7:
                laize = refente.laizes[current_index]
                if laize is None:
                    break
                else:
                    if self.encrier.bobines_filles_selected:
                        for bobine in self.encrier.bobines_filles_selected:
                            if bobine.pose == 0:
                                continue
                            if self.encrier.color in bobine.colors_cliche and current_index == bobine.index:
                                self.hbox.addWidget(ClicheUi(parent=self,
                                                             bobine_selected=bobine,
                                                             color=self.encrier.color))
                                new_index += bobine.pose
                    if current_index == new_index:
                        self.hbox.addSpacing(laize)
                        current_index += 1
                        new_index = current_index
                    else:
                        current_index = new_index
        else:
            if self.encrier.bobines_filles_selected:
                for bobine in self.encrier.bobines_filles_selected:
                    if bobine.pose == 0:
                        continue
                    elif self.encrier.color in bobine.colors_cliche:
                        self.hbox.addWidget(ClicheUi(parent=self, bobine_selected=bobine, color=self.encrier.color))
        self.hbox.addStretch()

    def paintEvent(self, e):
        p = QPainter(self)
        color = color_blanc.rgb_components
        qcolor = QColor(color[0], color[1], color[2])
        pen = QPen()
        pen.setColor(qcolor)
        p.setPen(pen)
        p.drawRect(0, 0, self.width()-1, self.height()-1)
        super(LineEncrier, self).paintEvent(e)
