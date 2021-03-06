# !/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QHBoxLayout, QLabel
from PyQt5.QtGui import QDrag

from commun.constants.colors import color_noir, color_blanc
from commun.constants.stylesheets import black_16_italic_label_stylesheet
from commun.utils.layout import clear_layout
from commun.ui.public.cliche_ui import ClicheUi
from commun.ui.public.mondon_widget import MondonWidget
from PyQt5.QtCore import Qt, QMimeData


class LineEncrier(MondonWidget):

    def __init__(self, parent=None, plan_prod=None, index=None):
        super(LineEncrier, self).__init__(parent=parent)
        self.setFixedHeight(80)
        self.background_color = color_blanc
        self.set_border(color=color_noir)
        self.width_F = 1
        self.plan_prod = plan_prod
        self.index = index
        self.hbox = QHBoxLayout()
        self.init_widget()
        self.update_widget()

    def init_widget(self):
        self.hbox.setContentsMargins(0, 0, 0, 0)
        self.hbox.setSpacing(0)
        self.setLayout(self.hbox)

    def update_widget(self):
        clear_layout(self.hbox)
        encrier = self.plan_prod.encriers[self.index-1]
        refente = encrier.refente
        if encrier.color is None or encrier.color[0] == "_":
            if encrier.color is None:
                text_label = "Encrier vide"
            else:
                color = encrier.color[1:]
                text_label = "Couleur actuelle encrier: {}".format(color)
            label_color_encrier = QLabel(text_label)
            label_color_encrier.setStyleSheet(black_16_italic_label_stylesheet)
            label_color_encrier.setAlignment(Qt.AlignCenter)
            self.hbox.addWidget(label_color_encrier)
            return
        if refente:
            self.hbox.addSpacing(980-refente.laize-refente.dec+refente.chute)
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
                            if self.is_valid_encrier_from_bobine(encrier=encrier, bobine=bobine, index=current_index):
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

    def is_valid_encrier_from_bobine(self, encrier, bobine, index):
        if index != bobine.index:
            return False
        if encrier.color not in bobine.colors_cliche:
            return False
        encriers = self.plan_prod.encriers
        for p_encrier in encriers:
            if p_encrier == encrier:
                return True
            if p_encrier.color == encrier.color:
                return False
        return True

    def mouseMoveEvent(self, e):
        color_encrier = self.plan_prod.encriers[self.index-1].color
        if color_encrier is None or color_encrier[0] == "_":
            e.ignore()
        else:
            mime_data = QMimeData()
            mime_data.setText(str(self.index))
            drag = QDrag(self)
            drag.setMimeData(mime_data)
            drag.exec_(Qt.MoveAction)
