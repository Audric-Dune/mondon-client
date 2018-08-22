# !/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtCore import QPoint

from commun.ui.public.bobine_fille_selected_ui import BobineFilleSelected
from commun.ui.public.chute_ui import ChuteUi
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
        self.valid_index = []
        self.set_background_color(color_blanc)
        self.ech = ech
        self.refente = refente
        self.hbox = QHBoxLayout()
        self.bobines_selected = bobines_selected
        self.init_widget(refente)

    def dragEnterEvent(self, e):
        e.accept()

    def dragMoveEvent(self, e):
        split_mime_data = e.mimeData().text().split("_")
        code_bobine = split_mime_data[0]
        pose = int(split_mime_data[1])
        index = int(split_mime_data[2])
        mouse_pos = e.pos()
        self.drag_ui(code_bobine, pose, index, mouse_pos)
        if not self.valid_index:
            self.valid_index = self.get_valid_index_from_bobine(bobine=self.bobine_drag.bobine)
        print("self.valid_index", self.valid_index)
        e.accept()

    def get_valid_index_from_bobine(self, bobine):
        valid_index = []
        for index in range(len(self.refente.laizes)):
            bobines_buffer = self.bobines_selected.copy()
            refente_buffer = self.refente.laizes.copy()
            if self.can_apply_bobine_at_index(bobine, index, refente=refente_buffer, pose=bobine.pose):
                self.apply_bobine(bobine=bobine, start_index=index, refente=refente_buffer)
                bobines_buffer.remove(bobine)
            else:
                continue
            if self.is_valid_refente_buffer_with_bobines_buffer(bobines_buffer=bobines_buffer,
                                                                refente_buffer=refente_buffer):
                valid_index.append(index)
        return valid_index

    def is_valid_refente_buffer_with_bobines_buffer(self, bobines_buffer, refente_buffer):
        bb = bobines_buffer.copy()
        rb = refente_buffer.copy()
        if self.is_complete_refente(rb):
            return True
        index = 0
        for laize in rb:
            if laize is None:
                pass
            else:
                for p_bobine in bb:
                    if self.can_apply_bobine_at_index(p_bobine,
                                                      index=index,
                                                      refente=rb,
                                                      pose=p_bobine.pose):
                        self.apply_bobine(bobine=p_bobine, start_index=index, refente=rb)
                        bb.remove(p_bobine)
                        if self.is_valid_refente_buffer_with_bobines_buffer(bb, rb):
                            return True
            index += 1
        return False

    @staticmethod
    def is_complete_refente(refente):
        for laize in refente:
            if laize:
                return False
        return True

    def can_apply_bobine_at_index(self, bobine, index, refente, pose):
        if index >= 7:
            return False
        if refente[index] == bobine.laize:
            pose -= 1
            if pose <= 0:
                return True
            index += 1
            if self.can_apply_bobine_at_index(bobine, index, refente, pose):
                return True
        else:
            return False

    @staticmethod
    def remove_bobine(bobine, bobines):
        for current_bobine in bobines:
            if current_bobine.code == bobine.code and current_bobine.index == bobine.index:
                bobines.remove(bobine)

    @staticmethod
    def apply_bobine(bobine, start_index, refente):
        pose = bobine.pose if bobine.pose > 0 else 1
        counter = 0
        index = start_index
        while counter < pose:
            refente[index] = None
            counter += 1
            index += 1

    def drag_ui(self, code_bobine, pose, index, mouse_pos):
        bobine_pos = QPoint(0, 0)
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
                try:
                    bobine = bobine_widget.bobine
                except AttributeError:
                    continue
                if bobine.code == code_bobine and bobine.pose == pose and bobine.index == index:
                    bobine_pos = bobine_widget.pos()
            if self.delta_x_drag is None:
                self.delta_x_drag = mouse_pos.x() - bobine_pos.x()
                self.delta_y_drag = mouse_pos.y() - bobine_pos.y()
            self.bobine_drag.move(mouse_pos.x() - self.delta_x_drag, mouse_pos.y() - self.delta_y_drag)

    @staticmethod
    def get_bobine_buffer(bobines):
        bobines_buffer = {}
        for bobine in bobines:
            bobines_buffer[bobine.index] = bobine
        import collections
        bobines_buffer = collections.OrderedDict(sorted(bobines_buffer.items()))
        return bobines_buffer

    def dragLeaveEvent(self, e):
        self.delete_bobine_drag()
        e.accept()

    def dropEvent(self, e):
        if self.valid_index:
            index_drop = self.get_index_at_pos(e.pos())
            print("index_drop", index_drop)
            valid_index_drop = min(self.valid_index, key=lambda x: abs(x-index_drop))
            print("valid_index_drop", valid_index_drop)
            if index_drop == self.bobine_drag.bobine.index:
                pass
            elif valid_index_drop in self.valid_index:
                self.get_new_bobines_fille_selected(bobine=self.bobine_drag.bobine,
                                                    index_bobine=valid_index_drop,
                                                    bobines=self.bobines_selected)
                from gestion.stores.settings_store import settings_store_gestion
                settings_store_gestion.plan_prod.bobines_filles_selected = self.bobines_selected
                settings_store_gestion.plan_prod.ON_CHANGED_SIGNAL.emit()
        self.delta_x_drag = None
        self.delta_y_drag = None
        self.valid_index = []
        self.delete_bobine_drag()
        e.accept()

    def get_index_at_pos(self, pos):
        counter = 0
        index = 0
        for laize in self.refente.laizes:
            counter += laize
            if pos.x() < counter:
                counter_decimal = counter-laize
                while counter_decimal <= counter:
                    counter_decimal += laize/10
                    if pos.x() < counter_decimal:
                        return index
                    index += 0.1
            index += 1

    def get_new_bobines_fille_selected(self, bobine, bobines, index_bobine):
        bobines_buffer = self.get_bobine_buffer(bobines)
        bobines_buffer = self.remove_value_in_buffer(buffer=bobines_buffer, element=bobine)
        index = 0
        while index < len(self.refente.laizes):
            laize = self.refente.laizes[index]
            if laize is None:
                index += 1
            elif index == index_bobine:
                bobine.index = index
                index += bobine.pose if bobine.pose else 1
            else:
                for k, p_bobine in bobines_buffer.items():
                    if laize == p_bobine.laize and index in self.get_valid_index_from_bobine(p_bobine):
                        p_bobine.index = index
                        index += p_bobine.pose if p_bobine.pose else 1
                        bobines_buffer = self.remove_value_in_buffer(buffer=bobines_buffer, element=p_bobine)
                        break

    @staticmethod
    def remove_value_in_buffer(buffer, element):
        for k, v in buffer.items():
            if v == element:
                del buffer[k]
                return buffer

    def delete_bobine_drag(self):
        if self.bobine_drag:
            self.bobine_drag.deleteLater()
            self.bobine_drag = None

    def init_widget(self, refente):
        self.hbox.setSpacing(0)
        self.hbox.setContentsMargins(0, 0, 0, 0)
        index = 0
        if refente.chute:
            self.hbox.addWidget(ChuteUi(parent=self, chute=refente.chute))
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
