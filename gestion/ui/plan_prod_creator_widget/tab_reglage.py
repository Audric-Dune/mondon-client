# !/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout
from PyQt5.QtGui import QPen, QPainter, QColor

from commun.constants.colors import color_noir, color_blanc
from commun.stores.reglage_store import reglage_store
from commun.ui.public.checkbox_button import CheckboxButton
from commun.utils.layout import clear_layout


class TabReglage(QWidget):

    def __init__(self, parent=None, plan_prod=None):
        super(TabReglage, self).__init__(parent=parent)
        self.plan_prod = plan_prod
        self.vbox = QVBoxLayout()
        self.init_ui()
        self.update_widget()

    def init_ui(self):
        self.setLayout(self.vbox)

    def update_widget(self):
        self.plan_prod.data_reglages.update_reglage()
        clear_layout(self.vbox)
        for data_reglage in self.plan_prod.data_reglages.data_reglages:
            if not data_reglage.reglage.is_optionnel() and data_reglage.reglage.cat != "CHAUFFE":
                self.vbox.addWidget(LineReglage(parent=self, data_reglage=data_reglage))
        self.vbox.addSpacing(50)
        for data_reglage in self.plan_prod.data_reglages.data_reglages:
            if data_reglage.reglage.is_optionnel():
                self.vbox.addWidget(LineReglage(parent=self, data_reglage=data_reglage))
        self.vbox.addStretch(0)


class LineReglage(QWidget):

    def __init__(self, parent=None, data_reglage=None, reglage=None):
        super(LineReglage, self).__init__(parent=parent)
        self.data_reglage = data_reglage
        self.reglage = data_reglage.reglage if data_reglage else reglage
        self.init_ui()

    def init_ui(self):
        hbox = QHBoxLayout()
        hbox.setContentsMargins(0, 0, 0, 0)
        label_des = QLabel(self.reglage.des)
        label_des.setFixedWidth(350)
        hbox.addWidget(label_des)
        qty = self.reglage.qty
        label_qty = QLabel("x{}".format(qty))
        hbox.addWidget(label_qty)
        check_box_conducteur = CheckboxButton(parent=self, is_check=not self.data_reglage.check_box_conducteur)
        check_box_conducteur.ON_CLICK_SIGNAL.connect(lambda: self.data_reglage.flip_check_box("conducteur"))
        check_box_conducteur.setFixedSize(20, 20)
        hbox.addWidget(check_box_conducteur)
        check_box_aide = CheckboxButton(parent=self, is_check=not self.data_reglage.check_box_aide)
        check_box_aide.ON_CLICK_SIGNAL.connect(lambda: self.data_reglage.flip_check_box("aide"))
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
