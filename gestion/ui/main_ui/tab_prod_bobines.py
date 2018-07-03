# !/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QPainter, QPen

from commun.constants.stylesheets import black_14_label_stylesheet
from commun.constants.colors import color_blanc, color_noir
from commun.utils.timestamp import timestamp_at_day_ago
from commun.utils.layout import clear_layout
from commun.stores.bobine_fille_store import bobine_fille_store

from gestion.stores.settings_store import settings_store_gestion


class TabProdBobine(QWidget):

    def __init__(self, parent=None):
        super(TabProdBobine, self).__init__(parent=parent)
        self.dict_bobines = {}
        self.vbox = QVBoxLayout()
        self.init_ui()
        settings_store_gestion.SETTINGS_CHANGED_SIGNAL.connect(self.update_widget)

    def init_ui(self):
        self.update_widget()
        self.vbox.setSpacing(0)
        self.vbox.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.vbox)

    def paintEvent(self, e):
        p = QPainter(self)
        color = color_blanc.rgb_components
        qcolor = QColor(color[0], color[1], color[2])
        p.fillRect(0, 0, self.width(), self.height(), qcolor)
        color = color_noir.rgb_components
        qcolor = QColor(color[0], color[1], color[2])
        pen = QPen()
        pen.setColor(qcolor)
        p.setPen(pen)
        p.drawRect(0, 0, self.width()-1, self.height()-1)

    def update_widget(self):
        self.get_bobines()
        clear_layout(self.vbox)
        self.vbox.addWidget(LineLegend(parent=self))
        for key, value in self.dict_bobines.items():
            bobine = bobine_fille_store.get_bobine(code=key)
            self.vbox.addWidget(LineBobine(parent=self, bobine=bobine, quantity=value))

    def get_bobines(self):
        self.dict_bobines.clear()
        from gestion.stores.plan_prod_store import plan_prod_store
        day_ago = settings_store_gestion.day_ago
        start = timestamp_at_day_ago(day_ago)
        end = timestamp_at_day_ago(settings_store_gestion.day_ago - 1)
        for prod in plan_prod_store.plans_prods:
            if start <= prod.start < end:
                self.dict_bobines = self.add_bobines_from_prod(prod=prod, p_dict=self.dict_bobines)

    @staticmethod
    def add_bobines_from_prod(prod, p_dict):
        tours = prod.tours
        for bobine in prod.bobines_filles_selected:
            pose = bobine.pose if bobine.pose else 1
            if p_dict.get(bobine.code, False):
                p_dict[bobine.code] += tours * pose
            else:
                p_dict[bobine.code] = tours * pose
        return p_dict


class LineBobine(QWidget):

    def __init__(self, bobine, quantity, parent=None):
        super(LineBobine, self).__init__(parent=parent)
        self.bobine = bobine
        self.quantity = quantity
        self.setFixedHeight(30)
        self.init_widget()

    def init_widget(self):
        hbox = QHBoxLayout()
        hbox.setContentsMargins(0, 0, 0, 0)
        add_collum(layout=hbox, text=self.bobine.code, aligment=Qt.AlignVCenter | Qt.AlignLeft, size=200)
        add_collum(layout=hbox, text=str(int(self.bobine.laize)))
        add_collum(layout=hbox, text=str(self.bobine.color))
        add_collum(layout=hbox, text=str(int(self.bobine.stock)))
        add_collum(layout=hbox, text=str(int(self.bobine.stock_therme)))
        add_collum(layout=hbox, text="+{}".format(int(self.quantity)))
        add_collum(layout=hbox, text=str(int(self.bobine.stock_therme + self.quantity)))
        self.setLayout(hbox)


class LineLegend(QWidget):

    def __init__(self, parent):
        super(LineLegend, self).__init__(parent=parent)
        self.setFixedHeight(30)
        self.init_widget()

    def paintEvent(self, e):
        p = QPainter(self)
        color = color_noir.rgb_components
        qcolor = QColor(color[0], color[1], color[2])
        pen = QPen()
        pen.setColor(qcolor)
        p.setPen(pen)
        p.drawLine(0, self.height()-1, self.width()-1, self.height()-1)

    def init_widget(self):
        hbox = QHBoxLayout()
        hbox.setContentsMargins(0, 0, 0, 0)
        add_collum(layout=hbox, text="Code", aligment=Qt.AlignVCenter | Qt.AlignLeft, size=200)
        add_collum(layout=hbox, text="Laize")
        add_collum(layout=hbox, text="Couleur")
        add_collum(layout=hbox, text="Stock")
        add_collum(layout=hbox, text="Stock à therme")
        add_collum(layout=hbox, text="Production")
        add_collum(layout=hbox, text="Stock prév.")
        self.setLayout(hbox)


def add_collum(layout, text, stylesheet=None, aligment=None, size=None):
    label = QLabel(text)
    if size:
        label.setFixedWidth(size)
    label.setStyleSheet(stylesheet if stylesheet else black_14_label_stylesheet)
    label.setAlignment(aligment if aligment else Qt.AlignVCenter | Qt.AlignCenter)
    layout.addWidget(label)

