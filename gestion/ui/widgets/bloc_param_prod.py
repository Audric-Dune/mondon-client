# !/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QHBoxLayout, QLabel

from commun.utils.timestamp import timestamp_to_hour_little
from commun.constants.colors import color_bleu_gris
from commun.ui.public.mondon_widget import MondonWidget
from commun.ui.public.text_edit import TextEdit
from commun.constants.stylesheets import white_text_edit_stylesheet


class BlocParamProd(MondonWidget):
    def __init__(self, plan_prod, parent=None):
        super(BlocParamProd, self).__init__(parent=parent)
        self.background_color = color_bleu_gris
        self.plan_prod = plan_prod
        self.hbox = QHBoxLayout()
        self.text_edit_tours = TextEdit()
        self.text_edit_tours.setText(str(self.plan_prod.tours))
        self.text_edit_tours.setStyleSheet(white_text_edit_stylesheet)
        self.text_edit_tours.textChanged.connect(self.handle_tours_changed)
        self.init_ui()

    def init_ui(self):
        self.hbox.addWidget(QLabel("Nombre de tours :"))
        self.hbox.addWidget(self.text_edit_tours)
        self.hbox.addWidget(QLabel("PRODUCTION"))
        self.hbox.addWidget(QLabel("Début production :"))
        self.hbox.addWidget(QLabel(timestamp_to_hour_little(self.plan_prod.start)))
        self.hbox.addWidget(QLabel(" - Fin production :"))
        self.setLayout(self.hbox)

    def handle_tours_changed(self, text_edit_value):
        self.plan_prod.tours = int(text_edit_value)
