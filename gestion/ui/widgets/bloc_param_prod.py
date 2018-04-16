# !/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QHBoxLayout, QLabel

from commun.utils.timestamp import timestamp_to_hour_little,\
    timestamp_at_time,\
    get_hour_in_timestamp,\
    get_min_in_timestamp
from commun.constants.colors import color_bleu_gris
from commun.ui.public.mondon_widget import MondonWidget
from commun.ui.public.text_edit import TextEdit
from commun.constants.stylesheets import white_text_edit_stylesheet, red_text_edit_stylesheet


class BlocParamProd(MondonWidget):
    def __init__(self, plan_prod, parent=None):
        super(BlocParamProd, self).__init__(parent=parent)
        self.background_color = color_bleu_gris
        self.plan_prod = plan_prod
        self.hbox = QHBoxLayout()
        self.text_edit_tours = TextEdit(number_only=True)
        self.text_edit_tours.setText(str(self.plan_prod.tours))
        self.text_edit_tours.setStyleSheet(white_text_edit_stylesheet)
        self.text_edit_tours.textChanged.connect(self.handle_tours_changed)
        self.text_edit_hour_end = TextEdit(number_only=True)
        self.text_edit_hour_end.setStyleSheet(white_text_edit_stylesheet)
        self.text_edit_min_end = TextEdit(number_only=True)
        self.text_edit_min_end.setStyleSheet(white_text_edit_stylesheet)
        self.update_label()
        self.text_edit_hour_end.textChanged.connect(self.handle_hour_changed)
        self.text_edit_min_end.textChanged.connect(self.handle_min_changed)
        self.init_ui()

    def init_ui(self):
        self.hbox.setSpacing(0)
        self.hbox.addWidget(QLabel("Nombre de tours : "))
        self.hbox.addWidget(self.text_edit_tours)
        self.hbox.addWidget(QLabel("PRODUCTION"))
        self.hbox.addWidget(QLabel("Début production : "))
        self.hbox.addWidget(QLabel(timestamp_to_hour_little(self.plan_prod.start)))
        self.hbox.addWidget(QLabel(" - Fin production : "))
        self.hbox.addWidget(self.text_edit_hour_end)
        self.hbox.addWidget(QLabel(" : "))
        self.hbox.addWidget(self.text_edit_min_end)
        self.setLayout(self.hbox)

    def update_label(self):
        pass
        # self.text_edit_hour_end.setText(str(get_hour_in_timestamp(self.plan_prod.end)))
        # self.text_edit_min_end.setText(str(get_min_in_timestamp(self.plan_prod.end)))

    def handle_tours_changed(self, text_edit_value):
        self.plan_prod.tours = int(text_edit_value)

    def handle_hour_changed(self, text_edit_hour):
        if text_edit_hour > 23:
            self.text_edit_hour_end.setStyleSheet(red_text_edit_stylesheet)
        else:
            if self.text_edit_min_end.text() == "??":
                self.text_edit_min_end.setText("00")
            new_end = timestamp_at_time(ts=self.plan_prod.start,
                                        hours=int(text_edit_hour),
                                        min=int(self.text_edit_min_end.text()))
            if self.plan_prod.start > new_end:
                self.text_edit_hour_end.setStyleSheet(red_text_edit_stylesheet)

    def handle_min_changed(self, text_edit_min):
        pass
