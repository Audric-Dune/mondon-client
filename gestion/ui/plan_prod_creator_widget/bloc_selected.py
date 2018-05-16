# !/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.Qt import Qt
from PyQt5.QtGui import QColor, QPainter, QPen
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel
from gestion.ui.line_in_selector.line_bobine_poly import LineBobinePoly
from gestion.ui.line_in_selector.line_perfo import LinePerfo
from gestion.ui.line_in_selector.line_refente import LineRefente

from commun.constants.colors import color_blanc, color_gris_noir
from commun.constants.stylesheets import gray_18_label_stylesheet
from commun.ui.public.mondon_widget import MondonWidget
from commun.utils.layout import clear_layout
from gestion.stores.filter_store import filter_store
from gestion.ui.line_in_selector.line_bobine_papier import LineBobinePapier


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
                content_ui = LinePerfo(perfo=self.parent.plan_prod.perfo_selected)
                content_layout.addWidget(content_ui)
                return content_layout
            else:
                content_layout.addLayout(self.get_ui_select(text="une campagne de perforation"))
                return content_layout
        if self.data_type == "papier":
            if self.parent.plan_prod.bobine_papier_selected:
                content_ui = LineBobinePapier(bobine=self.parent.plan_prod.bobine_papier_selected)
                content_layout.addWidget(content_ui)
                return content_layout
            else:
                content_layout.addLayout(self.get_ui_select(text="une bobine mère papier"))
                return content_layout
        if self.data_type == "poly":
            if self.parent.plan_prod.bobine_poly_selected:
                content_ui = LineBobinePoly(bobine=self.parent.plan_prod.bobine_poly_selected)
                content_layout.addWidget(content_ui)
                return content_layout
            else:
                content_layout.addLayout(self.get_ui_select(text="une bobine mère polypro"))
                return content_layout
        if self.data_type == "refente":
            if self.parent.plan_prod.refente_selected:
                content_ui = LineRefente(refente=self.parent.plan_prod.refente_selected)
                content_layout.addWidget(content_ui)
                return content_layout
            else:
                content_layout.addLayout(self.get_ui_select(text="une refente"))
                return content_layout
        content_layout.addLayout(self.get_ui_select(text="En cours"))
        return content_layout

    def paintEvent(self, e):
        p = QPainter(self)
        color = color_gris_noir.rgb_components
        qcolor_gris_noir = QColor(color[0], color[1], color[2])
        pen = QPen()
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
