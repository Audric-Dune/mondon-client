# !/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.Qt import Qt
from PyQt5.QtGui import QColor, QPainter, QPen
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel, QWidget, QPushButton, QSizePolicy

from commun.constants.colors import color_blanc, color_gris_noir, color_noir, color_orange
from commun.constants.stylesheets import gray_18_label_stylesheet, button_delete_bobine_selected_stylesheet
from commun.ui.public.pixmap_button import PixmapButton
from commun.ui.public.mondon_widget import MondonWidget
from commun.ui.public.bobine_mere_ui import BobineMereUI
from commun.ui.public.refente_ui import RefenteUi
from commun.ui.public.perfo_ui import PerfoUi
from commun.ui.public.dec_bobine_refente import DecBobineRefente
from commun.utils.layout import clear_layout
from commun.utils.bobines import group_bobine

from gestion.stores.filter_store import filter_store
from gestion.ui.plan_prod_creator_widget.line_bobine_selected import LineBobineSelected
from gestion.ui.plan_prod_creator_widget.legend_bobine_selected import LegendBobineSelected


class BlocSelected(MondonWidget):

    def __init__(self, data_type, callback,  parent=None):
        super(BlocSelected, self).__init__(parent=parent)
        self.background_color = color_blanc
        self.set_border(color=color_noir)
        self.data_type = data_type
        self.parent = parent
        self.callback = callback
        self.master_hbox = QHBoxLayout()
        self.master_hbox.setContentsMargins(0, 0, 10, 0)
        self.clear_bt = PixmapButton(parent=self)
        self.init_button()
        self.init_ui()

    def init_ui(self):
        self.master_hbox.addLayout(self.get_content())
        if self.data_type != "bobine":
            self.master_hbox.addWidget(self.clear_bt)
        else:
            self.clear_bt.hide()
            self.master_hbox.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.master_hbox)

    def init_button(self):
        self.clear_bt.clicked.connect(self.handle_clicked_bt_delete)
        self.clear_bt.setStyleSheet(button_delete_bobine_selected_stylesheet)
        self.clear_bt.setContentsMargins(0)
        self.clear_bt.setFixedSize(15, 15)
        self.clear_bt.add_image("commun/assets/images/delete.png")

    def update_widget(self):
        clear_layout(self.master_hbox)
        self.clear_bt = PixmapButton(parent=self)
        self.init_button()
        self.master_hbox.addLayout(self.get_content())
        if self.data_type != "bobine":
            self.master_hbox.addWidget(self.clear_bt)

    def get_content(self):
        content_layout = QVBoxLayout()
        content_layout.setContentsMargins(0, 0, 0, 0)
        if self.data_type == "perfo":
            if self.parent.plan_prod.perfo_selected:
                perfo_ui = PerfoUi(perfo=self.parent.plan_prod.perfo_selected)
                content_ui = QHBoxLayout()
                content_ui.setContentsMargins(1, 5, 0, 5)
                content_ui.addWidget(perfo_ui)
                content_ui.addStretch(0)
                content_layout.addLayout(content_ui)
            else:
                self.clear_bt.hide()
                content_layout.addLayout(self.get_ui_select(text="une campagne de perforation"))
            return content_layout
        if self.data_type == "papier":
            if self.parent.plan_prod.bobine_papier_selected:
                if self.parent.plan_prod.refente_selected:
                    refente = self.parent.plan_prod.refente_selected
                    content_ui = QHBoxLayout()
                    content_ui.setSpacing(0)
                    content_ui.setContentsMargins(0, 0, 0, 0)
                    space = QWidget()
                    space.setFixedWidth(980-refente.laize-refente.dec)
                    content_ui.addWidget(space)
                    content_ui.addWidget(BobineMereUI(bobine=self.parent.plan_prod.bobine_papier_selected))
                    refente = self.parent.plan_prod.refente_selected
                    content_ui.addWidget(DecBobineRefente(dec=refente.dec))
                    content_ui.addStretch(0)
                    content_layout.addLayout(content_ui)
                else:
                    content_ui = BobineMereUI(bobine=self.parent.plan_prod.bobine_papier_selected)
                    content_layout.addWidget(content_ui)
            else:
                self.clear_bt.hide()
                content_layout.addLayout(self.get_ui_select(text="une bobine mère papier"))
            return content_layout
        if self.data_type == "poly":
            if self.parent.plan_prod.bobine_poly_selected:
                if self.parent.plan_prod.refente_selected:
                    refente = self.parent.plan_prod.refente_selected
                    content_ui = QHBoxLayout()
                    content_ui.setSpacing(0)
                    content_ui.setContentsMargins(0, 0, 0, 0)
                    space = QWidget()
                    space.setFixedWidth(980-refente.laize-refente.dec)
                    content_ui.addWidget(space)
                    content_ui.addWidget(BobineMereUI(bobine=self.parent.plan_prod.bobine_poly_selected))
                    refente = self.parent.plan_prod.refente_selected
                    content_ui.addWidget(DecBobineRefente(dec=refente.dec))
                    content_ui.addStretch(0)
                    content_layout.addLayout(content_ui)
                else:
                    content_ui = BobineMereUI(bobine=self.parent.plan_prod.bobine_poly_selected)
                    content_layout.addWidget(content_ui)
            else:
                self.clear_bt.hide()
                content_layout.addLayout(self.get_ui_select(text="une bobine mère polypro"))
            return content_layout
        if self.data_type == "refente":
            if self.parent.plan_prod.refente_selected:
                refente = self.parent.plan_prod.refente_selected
                content_ui = QHBoxLayout()
                content_ui.setSpacing(0)
                content_ui.setContentsMargins(0, 0, 0, 0)
                space = QWidget()
                space.setFixedWidth(980-refente.laize-refente.dec)
                content_ui.addWidget(space)
                content_ui.addWidget(RefenteUi(refente=refente,
                                               bobines_selected=self.parent.plan_prod.bobines_filles_selected))
                content_ui.addWidget(DecBobineRefente(dec=refente.dec))
                content_ui.addStretch(0)
                content_layout.addLayout(content_ui)
            else:
                self.clear_bt.hide()
                content_layout.addLayout(self.get_ui_select(text="une refente"))
            return content_layout
        if self.data_type == "bobine":
            content_layout.setContentsMargins(0, 0, 0, 0)
            content_layout.setSpacing(2)
            if self.parent.plan_prod.bobines_filles_selected:
                content_layout.addWidget(LegendBobineSelected())
                for value in group_bobine(bobines=self.parent.plan_prod.bobines_filles_selected).values():
                    content_layout.addWidget(LineBobineSelected(bobine=value[0], amount=value[1]))
                self.set_border(color=None)
            else:
                self.clear_bt.hide()
                content_layout.addLayout(self.get_ui_select(text="une bobine fille"))
                self.set_border(color=color_noir)
            return content_layout

    def is_selected(self):
        if self.data_type == "refente" and self.parent.plan_prod.refente_selected:
            return True
        if self.data_type == "papier" and self.parent.plan_prod.bobine_papier_selected:
            return True
        if self.data_type == "poly" and self.parent.plan_prod.bobine_poly_selected:
            return True
        if self.data_type == "perfo" and self.parent.plan_prod.perfo_selected:
            return True
        if self.data_type == "bobine" and self.parent.plan_prod.bobines_filles_selected:
            return True
        return False

    def handle_clicked_bt_delete(self):
        if self.data_type == "refente" and self.parent.plan_prod.refente_selected:
            self.parent.plan_prod.del_refente_selected()
        if self.data_type == "papier" and self.parent.plan_prod.bobine_papier_selected:
            self.parent.plan_prod.del_papier_selected()
        if self.data_type == "poly" and self.parent.plan_prod.bobine_poly_selected:
            self.parent.plan_prod.del_poly_selected()
        if self.data_type == "perfo" and self.parent.plan_prod.perfo_selected:
            self.parent.plan_prod.del_perfo_selected()
        self.parent.update()

    @staticmethod
    def get_ui_select(text):
        hbox = QHBoxLayout()
        label = QLabel("Double click pour sélectionner {}".format(text))
        label.setStyleSheet(gray_18_label_stylesheet)
        hbox.addWidget(label, alignment=Qt.AlignCenter)
        return hbox

    def mouseDoubleClickEvent(self, e):
        filter_store.set_data_type(self.data_type)
        self.callback()
        super(BlocSelected, self).mouseDoubleClickEvent(e)


