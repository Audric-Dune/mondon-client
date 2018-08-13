# !/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QWidget, QVBoxLayout

from commun.constants.colors import color_vert, color_rouge
from gestion.ui.plan_prod_creator_widget.line_encrier import LineEncrier


class BlocEncrier(QWidget):
    def __init__(self, parent=None, plan_prod=None):
        super(BlocEncrier, self).__init__(parent=parent)
        self.setAcceptDrops(True)
        self.parent = parent
        self.plan_prod = plan_prod
        self.line_encrier_1 = LineEncrier(parent=self, plan_prod=plan_prod, index=1)
        self.line_encrier_2 = LineEncrier(parent=self, plan_prod=plan_prod, index=2)
        self.line_encrier_3 = LineEncrier(parent=self, plan_prod=plan_prod, index=3)
        self.line_encrier_1_drag = LineEncrier(parent=self, plan_prod=plan_prod, index=1)
        self.line_encrier_1_drag.hide()
        self.line_encrier_2_drag = LineEncrier(parent=self, plan_prod=plan_prod, index=2)
        self.line_encrier_2_drag.hide()
        self.line_encrier_3_drag = LineEncrier(parent=self, plan_prod=plan_prod, index=3)
        self.line_encrier_3_drag.hide()
        self.delta_x_drag = None
        self.delta_y_drag = None
        self.master_vbox = QVBoxLayout()
        self.init_ui()

    def init_ui(self):
        self.master_vbox.setContentsMargins(0, 0, 0, 0)
        self.master_vbox.addWidget(self.line_encrier_3)
        self.master_vbox.addWidget(self.line_encrier_2)
        self.master_vbox.addWidget(self.line_encrier_1)
        self.setLayout(self.master_vbox)

    def dragEnterEvent(self, e):
        e.accept()

    def dragMoveEvent(self, e):
        index_drag = e.mimeData().text()
        if index_drag == "1":
            self.show_encrier_drag(encrier_drag=self.line_encrier_1_drag,
                                   mouse_pos=e.pos(),
                                   encrier=self.line_encrier_1)
            self.line_encrier_1_drag.width_F = 2
            if self.is_correct_drop_pos(index_drag=index_drag, mouse_pos=e.pos()):
                self.line_encrier_1_drag.border_color = color_vert
            else:
                self.line_encrier_1_drag.border_color = color_rouge
        elif index_drag == "2":
            self.show_encrier_drag(encrier_drag=self.line_encrier_2_drag,
                                   mouse_pos=e.pos(),
                                   encrier=self.line_encrier_2)
            self.line_encrier_2_drag.width_F = 2
            if self.is_correct_drop_pos(index_drag=index_drag, mouse_pos=e.pos()):
                self.line_encrier_2_drag.border_color = color_vert
            else:
                self.line_encrier_2_drag.border_color = color_rouge
        elif index_drag == "3":
            self.show_encrier_drag(encrier_drag=self.line_encrier_3_drag,
                                   mouse_pos=e.pos(),
                                   encrier=self.line_encrier_3)
            self.line_encrier_3_drag.width_F = 2
            if self.is_correct_drop_pos(index_drag=index_drag, mouse_pos=e.pos()):
                self.line_encrier_3_drag.border_color = color_vert
            else:
                self.line_encrier_3_drag.border_color = color_rouge

    def show_encrier_drag(self, encrier_drag, mouse_pos, encrier):
        encrier_drag.setFixedSize(encrier.size())
        encrier_drag.update_widget()
        encrier_pos = encrier.pos()
        if self.delta_x_drag is None:
            self.delta_x_drag = mouse_pos.x()-encrier_pos.x()
            self.delta_y_drag = mouse_pos.y()-encrier_pos.y()
        encrier_drag.move(mouse_pos.x()-self.delta_x_drag, mouse_pos.y()-self.delta_y_drag)
        encrier_drag.show()
        encrier_drag.activateWindow()
        encrier_drag.raise_()

    def is_correct_drop_pos(self, index_drag, mouse_pos):
        if self.line_encrier_1.geometry().contains(mouse_pos) and index_drag != "1":
            return True
        if self.line_encrier_2.geometry().contains(mouse_pos) and index_drag != "2":
            return True
        if self.line_encrier_3.geometry().contains(mouse_pos) and index_drag != "3":
            return True
        return False

    def dragLeaveEvent(self, e):
        self.hide_line_encrier_drag()
        e.accept()

    def dropEvent(self, e):
        self.hide_line_encrier_drag()
        self.delta_x_drag = None
        self.delta_y_drag = None
        index_drag = e.mimeData().text()
        index_drop = None
        if self.line_encrier_1.geometry().contains(e.pos()) and index_drag != 1:
            index_drop = 1
        if self.line_encrier_2.geometry().contains(e.pos()) and index_drag != 2:
            index_drop = 2
        if self.line_encrier_3.geometry().contains(e.pos()) and index_drag != 3:
            index_drop = 3
        if index_drop is None:
            e.ignore()
        else:
            self.swap_encrier(index_1=int(index_drag), index_2=int(index_drop))
            e.accept()

    def swap_encrier(self, index_1, index_2):
        color_encrier_1 = self.plan_prod.encriers[index_1-1].color
        color_encrier_2 = self.plan_prod.encriers[index_2-1].color
        self.plan_prod.encriers[index_1-1].color = color_encrier_2
        self.plan_prod.encriers[index_2-1].color = color_encrier_1
        self.parent.update_encriers()

    def hide_line_encrier_drag(self):
        self.line_encrier_1_drag.hide()
        self.line_encrier_2_drag.hide()
        self.line_encrier_3_drag.hide()
3