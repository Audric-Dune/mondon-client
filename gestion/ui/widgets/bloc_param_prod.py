# !/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QHBoxLayout, QLabel

from commun.utils.timestamp import timestamp_to_hour_little
from commun.constants.colors import color_bleu_gris
from commun.ui.public.mondon_widget import MondonWidget
from commun.ui.public.text_edit import TextEdit
from commun.constants.stylesheets import line_edit_green_stylesheet, line_edit_red_stylesheet


class BlocParamProd(MondonWidget):
    def __init__(self, plan_prod, parent=None):
        super(BlocParamProd, self).__init__(parent=parent)
        self.background_color = color_bleu_gris
        self.plan_prod = plan_prod
        self.hbox = QHBoxLayout()
        self.text_edit_tours = TextEdit(number_only=True, number_limit=1000)
        self.text_edit_tours.setText(str(self.plan_prod.tours))
        self.text_edit_tours.setStyleSheet(line_edit_green_stylesheet)
        self.text_edit_tours.textChanged.connect(self.handle_tours_changed)
        self.label_end = QLabel("")
        self.update_label()
        self.init_ui()

    def init_ui(self):
        self.hbox.setSpacing(0)
        self.hbox.addWidget(QLabel("Nombre de tours : "))
        self.hbox.addWidget(self.text_edit_tours)
        self.hbox.addWidget(QLabel("PRODUCTION"))
        self.hbox.addWidget(QLabel("Début production : "))
        self.hbox.addWidget(QLabel(timestamp_to_hour_little(self.plan_prod.start)))
        self.hbox.addWidget(QLabel(" - Fin production : "))
        self.hbox.addWidget(self.label_end)
        self.setLayout(self.hbox)

    def update_label(self):
        if self.text_edit_tours.text() != self.plan_prod.tours:
            self.text_edit_tours.setText(str(self.plan_prod.tours))
        self.label_end.setText(timestamp_to_hour_little(self.plan_prod.end))

    def handle_tours_changed(self, text_edit_value):
        if text_edit_value == "":
            self.plan_prod.set_tours(0)
            self.text_edit_tours.setStyleSheet(line_edit_red_stylesheet)
        else:
            self.text_edit_tours.setStyleSheet(line_edit_green_stylesheet)
            self.plan_prod.set_tours(int(text_edit_value))
            if self.plan_prod.is_valid_tours():
                self.text_edit_tours.setStyleSheet(line_edit_green_stylesheet)
            else:
                self.text_edit_tours.setStyleSheet(line_edit_red_stylesheet)
