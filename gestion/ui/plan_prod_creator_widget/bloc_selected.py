# !/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.Qt import Qt
from PyQt5.QtGui import QColor, QPainter, QPen
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel, QWidget
from commun.constants.colors import color_blanc, color_gris_noir
from commun.constants.stylesheets import gray_18_label_stylesheet
from commun.ui.public.mondon_widget import MondonWidget
from commun.ui.public.bobine_mere_ui import BobineMereUI
from commun.ui.public.refente_ui import RefenteUi
from commun.ui.public.perfo_ui import PerfoUi
from commun.ui.public.dec_bobine_refente import DecBobineRefente
from commun.utils.layout import clear_layout
from gestion.stores.filter_store import filter_store


class BlocSelected(MondonWidget):

    def __init__(self, data_type, callback,  parent=None):
        super(BlocSelected, self).__init__(parent=parent)
        self.background_color = color_blanc
        self.data_type = data_type
        self.parent = parent
        self.callback = callback
        self.master_hbox = QVBoxLayout()
        self.init_ui()

    def init_ui(self):
        self.master_hbox.addLayout(self.get_content())
        self.setLayout(self.master_hbox)

    def update_widget(self):
        clear_layout(self.master_hbox)
        self.master_hbox.addLayout(self.get_content())
        self.update()

    def get_content(self):
        content_layout = QVBoxLayout()
        content_layout.setContentsMargins(0, 0, 0, 0)
        if self.data_type == "perfo":
            if self.parent.plan_prod.perfo_selected:
                content_ui = PerfoUi(perfo=self.parent.plan_prod.perfo_selected)
                content_layout.addWidget(content_ui)
                return content_layout
            else:
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
                    content_layout.addLayout(content_ui)
                else:
                    content_ui = BobineMereUI(bobine=self.parent.plan_prod.bobine_papier_selected)
                    content_layout.addWidget(content_ui)
                return content_layout
            else:
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
                    content_layout.addLayout(content_ui)
                else:
                    content_ui = BobineMereUI(bobine=self.parent.plan_prod.bobine_poly_selected)
                    content_layout.addWidget(content_ui)
                return content_layout
            else:
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
                content_layout.addLayout(content_ui)
                return content_layout
            else:
                content_layout.addLayout(self.get_ui_select(text="une refente"))
                return content_layout
        content_layout.addLayout(self.get_ui_select(text="En cours"))
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
        return False

    def paintEvent(self, e):
        if not self.is_selected():
            p = QPainter(self)
            color = color_gris_noir.rgb_components
            qcolor_gris_noir = QColor(color[0], color[1], color[2])
            pen = QPen()
            pen.setStyle(Qt.CustomDashLine)
            pen.setDashPattern([10, 3])
            pen.setColor(qcolor_gris_noir)
            p.setPen(pen)
            p.drawRect(0, 0, self.width()-1, self.height()-1)

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
