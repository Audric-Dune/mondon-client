# !/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtCore import QPoint

from commun.ui.public.bobine_fille_selected_ui import BobineFilleSelected
from commun.ui.public.bobine_fille_ui import BobineFille
from commun.ui.public.mondon_widget import MondonWidget
from commun.constants.colors import color_blanc


class RefenteUi(MondonWidget):

    def __init__(self, parent=None, refente=None, bobines_selected=None, ech=1):
        super(RefenteUi, self).__init__(parent=parent)
        self.setAcceptDrops(True)
        self.bobine_drag = None
        self.delta_x_drag = None
        self.delta_y_drag = None
        self.set_background_color(color_blanc)
        self.ech = ech
        self.refente = refente
        self.hbox = QHBoxLayout()
        self.bobines_selected = bobines_selected
        self.init_widget(refente)

    def dragEnterEvent(self, e):
        e.accept()

    def dragMoveEvent(self, e):
        bobine_pos = QPoint(0, 0)
        split_mime_data = e.mimeData().text().split("_")
        code_bobine = split_mime_data[0]
        pose = int(split_mime_data[1])
        index = int(split_mime_data[2])
        for bobine in self.bobines_selected:
            if bobine.code == code_bobine and bobine.pose == pose and bobine.index == index:
                if self.bobine_drag is None:
                    self.bobine_drag = BobineFilleSelected(bobine_selected=bobine, parent=self)
                    self.bobine_drag.show()
        if self.bobine_drag is not None:
            for p_index in range(self.hbox.count()):
                bobine_widget = self.hbox.itemAt(p_index).widget()
                if not bobine_widget:
                    continue
                bobine = bobine_widget.bobine
                if bobine.code == code_bobine and bobine.pose == pose and bobine.index == index:
                    print("bobine_pos")
                    bobine_pos = bobine_widget.pos()
            if self.delta_x_drag is None:
                self.delta_x_drag = e.pos().x() - bobine_pos.x()
                self.delta_y_drag = e.pos().y() - bobine_pos.y()
            self.bobine_drag.move(e.pos().x() - self.delta_x_drag, e.pos().y() - self.delta_y_drag)
        e.accept()

    def dragLeaveEvent(self, e):
        self.delete_bobine_drag()
        e.accept()

    def dropEvent(self, e):
        self.delta_x_drag = None
        self.delta_y_drag = None
        self.delete_bobine_drag()
        e.accept()

    def delete_bobine_drag(self):
        self.bobine_drag.deleteLater()
        self.bobine_drag = None

    def init_widget(self, refente):
        self.hbox.setSpacing(0)
        self.hbox.setContentsMargins(0, 0, 0, 0)
        index = 0
        while index < len(refente.laizes):
            laize = refente.laizes[index]
            if laize:
                bobine_selected = self.get_bobine_for_index_in_laize(index=index, laize=laize)
                if bobine_selected:
                    self.hbox.addWidget(BobineFilleSelected(parent=self, bobine_selected=bobine_selected))
                    bobine_selected.index = index
                    index += bobine_selected.pose if bobine_selected.pose else 1
                else:
                    self.hbox.addWidget(BobineFille(parent=self, laize=laize, number=index+1))
                    index += 1
            else:
                index += 1
        self.hbox.addStretch()
        self.setLayout(self.hbox)

    def get_bobine_for_index_in_laize(self, index, laize):
        if self.bobines_selected is None:
            return False
        for bobine in self.bobines_selected:
            if bobine.index == index:
                return bobine
        for bobine in self.bobines_selected:
            if bobine.laize == laize and bobine.index is None:
                if self.is_valid_bobine_in_refente_at_index(bobine=bobine, index=index):
                    return bobine
                else:
                    continue
        return False

    def is_valid_bobine_in_refente_at_index(self, bobine, index):
        init_index = index
        if bobine.pose == 0:
            return True
        while index < init_index+bobine.pose:
            if bobine.laize == self.refente.laizes[index]:
                index += 1
            else:
                return False
        return True
