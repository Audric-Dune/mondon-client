# !/usr/bin/env python
# -*- coding: utf-8 -*-


from PyQt5.QtWidgets import QVBoxLayout, QLabel, QWidget
from PyQt5.QtCore import Qt

from commun.constants.colors import color_vert, color_rouge

from gestion.ui.plan_prod_creator_widget.bloc_information import BlocInformation
from gestion.ui.plan_prod_creator_widget.bloc_selected import BlocSelected
from gestion.ui.plan_prod_creator_widget.bloc_bt import BlocBt
from gestion.ui.selector_ui.selector_manager import SelectorManager
from gestion.stores.filter_store import filter_store
from gestion.stores.settings_store import settings_store_gestion
from gestion.ui.plan_prod_creator_widget.bloc_param_prod import BlocParamProd
from gestion.ui.plan_prod_creator_widget.line_encrier import LineEncrier


class PlanProdCreator(QWidget):

    def __init__(self, plan_prod, parent=None):
        super(PlanProdCreator, self).__init__(parent=parent)
        self.setAcceptDrops(True)
        self.setWindowFlags(Qt.Dialog)
        self.setFocusPolicy(Qt.ClickFocus)
        self.plan_prod = plan_prod
        self.plan_prod.ON_CHANGED_SIGNAL.connect(self.handle_plan_prod_changed)
        self.plan_prod.ON_TOURS_CHANGED.connect(self.handle_tours_plan_prod_changed)
        self.selector_manager = SelectorManager(parent=self, plan_prod=self.plan_prod)
        self.selector_manager.hide()
        self.bloc_param_prod = BlocParamProd(plan_prod=self.plan_prod, parent=self)
        self.titre_prod = QLabel("NOUVELLE PRODUCTION")
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
        self.bloc_poly_selected = BlocSelected(data_type="poly", parent=self, callback=self.show_selector)
        self.bloc_papier_selected = BlocSelected(data_type="papier", parent=self, callback=self.show_selector)
        self.bloc_perfo_selected = BlocSelected(data_type="perfo", parent=self, callback=self.show_selector)
        self.bloc_refente_selected = BlocSelected(data_type="refente", parent=self, callback=self.show_selector)
        self.bloc_bobines_selected = BlocSelected(data_type="bobine", parent=self, callback=self.show_selector)
        self.bloc_info = BlocInformation(parent=self, plan_prod=plan_prod)
        self.bloc_bt = BlocBt(parent=self, plan_prod=plan_prod, callback=self.handle_click_bt)
        self.init_ui()
        self.show()

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
        self.update_encriers()

    def hide_line_encrier_drag(self):
        self.line_encrier_1_drag.hide()
        self.line_encrier_2_drag.hide()
        self.line_encrier_3_drag.hide()

    def init_ui(self):
        master_vbox = QVBoxLayout()
        vbox = QVBoxLayout()
        vbox.setContentsMargins(0, 0, 0, 0)
        vbox.addWidget(self.bloc_refente_selected)
        vbox.addWidget(self.line_encrier_3)
        vbox.addWidget(self.line_encrier_2)
        vbox.addWidget(self.line_encrier_1)
        vbox.addWidget(self.bloc_papier_selected)
        vbox.addWidget(self.bloc_perfo_selected)
        vbox.addWidget(self.bloc_poly_selected)
        master_vbox.addWidget(self.bloc_param_prod)
        master_vbox.addWidget(self.bloc_bobines_selected)
        master_vbox.addLayout(vbox)
        master_vbox.addWidget(self.bloc_bt)
        master_vbox.addWidget(self.bloc_info)
        self.setLayout(master_vbox)

    def update_bloc_selected(self):
        self.bloc_poly_selected.update_widget()
        self.bloc_bobines_selected.update_widget()
        self.bloc_refente_selected.update_widget()
        self.bloc_perfo_selected.update_widget()
        self.bloc_papier_selected.update_widget()

    def update_encriers(self):
        self.line_encrier_1.update_widget()
        self.line_encrier_2.update_widget()
        self.line_encrier_3.update_widget()

    def handle_plan_prod_changed(self):
        self.update_bloc_selected()
        self.update_encriers()
        if filter_store.data_type != "bobine" or len(self.plan_prod.current_bobine_fille_store.bobines) == 0:
            self.selector_manager.hide()
        self.bloc_param_prod.update_label()
        self.bloc_info.update_widget()

    def handle_tours_plan_prod_changed(self):
        self.bloc_param_prod.update_label()
        self.bloc_info.update_widget()
        self.bloc_bobines_selected.update_widget()

    def handle_click_bt(self, bt_name):
        if bt_name == "valid":
            if self.plan_prod.p_id:
                settings_store_gestion.update_plan_prod_on_database(self.plan_prod)
            else:
                settings_store_gestion.save_plan_prod()
        if bt_name == "cancel":
            settings_store_gestion.plan_prod = None
        self.close()

    def show_selector(self):
        self.selector_manager.show()
