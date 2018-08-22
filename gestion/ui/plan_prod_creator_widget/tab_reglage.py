# !/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout
from PyQt5.QtGui import QPen, QPainter, QColor

from commun.constants.colors import color_noir, color_blanc
from commun.stores.reglage_store import reglage_store
from commun.ui.public.checkbox_button import CheckboxButton
from commun.utils.layout import clear_layout

from gestion.stores.plan_prod_store import plan_prod_store


class TabReglage(QWidget):

    def __init__(self, parent=None, plan_prod=None):
        super(TabReglage, self).__init__(parent=parent)
        self.plan_prod = plan_prod
        self.time_aide = 0
        self.time_conducteur = 0
        self.vbox = QVBoxLayout()
        self.init_ui()
        self.update_widget()

    def init_ui(self):
        self.setLayout(self.vbox)

    def update_widget(self):
        clear_layout(self.vbox)
        for reglage in reglage_store.reglages:
            if reglage.is_active(p=self.plan_prod, last_p=self.plan_prod.last_plan_prod) and not reglage.optionnel:
                self.vbox.addWidget(LineReglage(parent=self, reglage=reglage))
        self.vbox.addStretch(0)


class LineReglage(QWidget):

    def __init__(self, parent=None, reglage=None):
        super(LineReglage, self).__init__(parent=parent)
        self.reglage = reglage
        self.id = reglage.id
        self.init_ui()

    def init_ui(self):
        hbox = QHBoxLayout()
        hbox.setContentsMargins(0, 0, 0, 0)
        label_des = QLabel(self.reglage.des)
        label_des.setFixedWidth(350)
        hbox.addWidget(label_des)
        qty = self.reglage.qty if self.reglage.qty else 1
        label_qty = QLabel("x{}".format(qty))
        hbox.addWidget(label_qty)
        check_box_conducteur = CheckboxButton(parent=self)
        check_box_conducteur.setFixedSize(20, 20)
        hbox.addWidget(check_box_conducteur)
        check_box_aide = CheckboxButton(parent=self)
        check_box_aide.setFixedSize(20, 20)
        hbox.addWidget(check_box_aide)
        label_time = QLabel("{} min".format(self.reglage.time))
        label_time.setFixedWidth(50)
        hbox.addWidget(label_time)
        self.setLayout(hbox)

    def paintEvent(self, e):
        p = QPainter(self)
        color = color_noir.rgb_components
        qcolor = QColor(color[0], color[1], color[2])
        pen = QPen()
        pen.setColor(qcolor)
        p.setPen(pen)
        color = color_blanc.rgb_components
        qcolor = QColor(color[0], color[1], color[2])
        p.fillRect(0, 0, self.width(), self.height(), qcolor)
        p.drawRect(0, 0, self.width(), self.height())
