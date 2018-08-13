# !/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QHBoxLayout, QWidget, QLabel
from PyQt5.QtGui import QPen, QPainter, QColor, QDrag, QFont

from commun.constants.colors import color_noir, color_blanc
from commun.constants.stylesheets import black_16_italic_label_stylesheet
from commun.utils.layout import clear_layout
from commun.ui.public.cliche_ui import ClicheUi
from PyQt5.QtCore import Qt, QMimeData


class LineEncrier(QWidget):

    def __init__(self, parent=None, plan_prod=None, index=None):
        super(LineEncrier, self).__init__(parent=parent)
        self.setFixedHeight(80)
        self.border_color = color_noir
        self.width_F = 1
        self.plan_prod = plan_prod
        self.index = index
        self.hbox = QHBoxLayout()
        self.init_widget()
        self.update_widget()

    def init_widget(self):
        self.hbox.setContentsMargins(10, 0, 0, 10)
        self.hbox.setSpacing(0)
        self.setLayout(self.hbox)

    def update_widget(self):
        clear_layout(self.hbox)
        encrier = self.plan_prod.encriers[self.index-1]
        print(encrier)
        refente = encrier.refente
        if encrier.color is None or encrier.color == "None":
            if encrier.color_last_prod is None or encrier.color_last_prod == "None":
                text_label = "Encrier vide"
            else:
                text_label = "Couleur actuelle encrier: {}".format(encrier.color_last_prod)
            label_color_encrier = QLabel(text_label)
            label_color_encrier.setStyleSheet(black_16_italic_label_stylesheet)
            label_color_encrier.setAlignment(Qt.AlignCenter)
            self.hbox.addWidget(label_color_encrier)
            return
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
                    if encrier.bobines_filles_selected:
                        for bobine in encrier.bobines_filles_selected:
                            if bobine.pose == 0:
                                continue
                            if encrier.color in bobine.colors_cliche and current_index == bobine.index:
                                self.hbox.addWidget(ClicheUi(parent=self,
                                                             bobine_selected=bobine,
                                                             color=encrier.color))
                                new_index += bobine.pose
                    if current_index == new_index:
                        self.hbox.addSpacing(laize)
                        current_index += 1
                        new_index = current_index
                    else:
                        current_index = new_index
        else:
            if encrier.bobines_filles_selected:
                for bobine in encrier.bobines_filles_selected:
                    if bobine.pose == 0:
                        continue
                    elif encrier.color in bobine.colors_cliche:
                        self.hbox.addWidget(ClicheUi(parent=self, bobine_selected=bobine, color=encrier.color))
        self.hbox.addStretch()

    def mouseMoveEvent(self, e):
        if self.plan_prod.encriers[self.index-1].color is None:
            e.ignore()
        else:
            mime_data = QMimeData()
            mime_data.setText(str(self.index))
            drag = QDrag(self)
            drag.setMimeData(mime_data)
            drag.exec_(Qt.MoveAction)

    def paintEvent(self, e):
        p = QPainter(self)
        color = self.border_color.rgb_components
        qcolor = QColor(color[0], color[1], color[2])
        pen = QPen()
        pen.setWidthF(self.width_F)
        pen.setColor(qcolor)
        p.setPen(pen)
        color = color_blanc.rgb_components
        qcolor = QColor(color[0], color[1], color[2])
        p.fillRect(0, 0, self.width(), self.height(), qcolor)
        p.drawRect(0.5*self.width_F, 0.5*self.width_F, self.width()-self.width_F, self.height()-self.width_F)
        p.setFont(QFont('Decorative', 12))
        p.translate(self.width()-5, self.height()-8)
        p.rotate(-90)
        color = color_noir.rgb_components
        qcolor = QColor(color[0], color[1], color[2])
        pen.setColor(qcolor)
        p.drawText(0, 0, "Encrier {}".format(self.index))
