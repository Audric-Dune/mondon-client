# !/usr/bin/env python
# -*- coding: utf-8 -*-


from PyQt5.QtWidgets import QWidget, QHBoxLayout, QPushButton
from PyQt5.QtGui import QPen, QPainter, QColor

from commun.constants.stylesheets import button_little_stylesheet, button_little_red_stylesheet
from commun.constants.colors import color_bleu_gris


class BlocBt(QWidget):

    def __init__(self, parent, plan_prod, callback):
        super(BlocBt, self).__init__(parent=parent)
        self.plan_prod = plan_prod
        self.callback = callback
        self.bt_valid = QPushButton("Validé")
        self.plan_prod.ON_CHANGED_SIGNAL.connect(self.update_bt)
        self.init_ui()
        self.update_bt()

    def init_ui(self):
        vbox = QHBoxLayout()
        vbox.setContentsMargins(5, 5, 20, 5)
        vbox.setSpacing(20)
        vbox.addStretch()
        self.bt_valid.setStyleSheet(button_little_stylesheet)
        self.bt_valid.setFixedSize(80, 25)
        self.bt_valid.clicked.connect(lambda: self.handle_bt_click(bt_name="valid"))
        bt_cancel = QPushButton("Annuler")
        bt_cancel.clicked.connect(lambda: self.handle_bt_click(bt_name="cancel"))
        bt_cancel.setStyleSheet(button_little_red_stylesheet)
        bt_cancel.setFixedSize(80, 25)
        vbox.addWidget(self.bt_valid)
        vbox.addWidget(bt_cancel)
        self.setLayout(vbox)

    def update_bt(self):
        if self.plan_prod.is_valid():
            self.bt_valid.setDisabled(False)
        else:
            self.bt_valid.setDisabled(True)

    def paintEvent(self, e):
        p = QPainter(self)
        color = color_bleu_gris.rgb_components
        qcolor = QColor(color[0], color[1], color[2])
        pen = QPen()
        pen.setColor(qcolor)
        p.setPen(pen)
        p.drawRect(0, 0, self.width()-1, self.height()-1)
        super(BlocBt, self).paintEvent(e)

    def handle_bt_click(self, bt_name):
        self.callback(bt_name)
