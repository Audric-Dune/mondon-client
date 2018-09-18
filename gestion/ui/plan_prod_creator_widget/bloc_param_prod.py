# !/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QHBoxLayout, QLabel, QVBoxLayout
from PyQt5.QtCore import Qt

from commun.utils.timestamp import timestamp_to_hour_little
from commun.constants.colors import color_bleu_gris
from commun.ui.public.mondon_widget import MondonWidget
from commun.ui.public.text_edit import TextEdit
from commun.constants.stylesheets import line_edit_green_stylesheet, line_edit_red_stylesheet,\
    white_12_label_stylesheet, white_16_bold_label_stylesheet, red_12_bold_label_stylesheet


class BlocParamProd(MondonWidget):
    def __init__(self, plan_prod, parent=None):
        super(BlocParamProd, self).__init__(parent=parent)
        # self.setFixedHeight(50)
        self.setFocusPolicy(Qt.ClickFocus)
        self.background_color = color_bleu_gris
        self.plan_prod = plan_prod
        self.hbox_master = QHBoxLayout()
        self.text_edit_tours = TextEdit(number_only=True, number_limit=1000)
        self.text_edit_tours.setText(str(self.plan_prod.tours))
        self.text_edit_tours.setStyleSheet(line_edit_green_stylesheet)
        self.text_edit_tours.textChanged.connect(self.handle_tours_changed)
        self.label_end = QLabel("Fin production : {}".format(timestamp_to_hour_little(self.plan_prod.end)))
        import time
        text_time_reglage = time.strftime("%H:%M:%S", time.gmtime(self.plan_prod.data_reglages.time_reglage * 60))
        self.label_time_reglage = QLabel("Réglage : {}".format(text_time_reglage))
        value_time_prod = self.plan_prod.end - self.plan_prod.start - self.plan_prod.data_reglages.time_reglage*3600
        text_prod = time.strftime("%H:%M:%S", time.gmtime(value_time_prod / 60))
        self.label_time_prod = QLabel("Production : {}".format(text_prod))
        self.update_label()
        self.init_ui()

    def init_ui(self):
        label_nb_tours = QLabel("Nombre de tours : ")
        label_nb_tours.setStyleSheet(white_12_label_stylesheet)
        self.hbox_master.addWidget(label_nb_tours)
        self.text_edit_tours.setFixedWidth(40)
        self.text_edit_tours.setAlignment(Qt.AlignCenter)
        self.hbox_master.addWidget(self.text_edit_tours)
        self.hbox_master.addStretch(1)
        label_prod = QLabel("PRODUCTION")
        label_prod.setStyleSheet(white_16_bold_label_stylesheet)
        self.hbox_master.addWidget(label_prod)
        self.hbox_master.addStretch(1)
        vbox = QVBoxLayout()
        label_debut = QLabel("Début production : {}".format(timestamp_to_hour_little(self.plan_prod.start)))
        label_debut.setStyleSheet(white_12_label_stylesheet)
        label_debut.setAlignment(Qt.AlignRight)
        self.label_end.setStyleSheet(white_12_label_stylesheet)
        self.label_end.setAlignment(Qt.AlignRight)
        self.label_time_reglage.setStyleSheet(white_12_label_stylesheet)
        self.label_time_reglage.setAlignment(Qt.AlignRight)
        self.label_time_prod.setStyleSheet(white_12_label_stylesheet)
        self.label_time_prod.setAlignment(Qt.AlignRight)
        vbox.addWidget(label_debut)
        vbox.addWidget(self.label_time_reglage)
        vbox.addWidget(self.label_time_prod)
        vbox.addWidget(self.label_end)
        self.hbox_master.addLayout(vbox)
        self.setLayout(self.hbox_master)

    def update_label(self):
        if self.text_edit_tours.text() != self.plan_prod.tours:
            self.text_edit_tours.setText(str(self.plan_prod.tours))
        self.label_end.setText("Fin production : {}".format(timestamp_to_hour_little(self.plan_prod.end)))
        import time
        text_time_reglage = time.strftime("%H:%M:%S", time.gmtime(self.plan_prod.data_reglages.time_reglage*60))
        self.label_time_reglage.setText("Réglage : {}".format(text_time_reglage))
        value_time_prod = self.plan_prod.end - self.plan_prod.start - self.plan_prod.data_reglages.time_reglage*60
        if value_time_prod < 0:
            value_time_prod = 0
        text_prod = time.strftime("%H:%M:%S", time.gmtime(value_time_prod))
        self.label_time_prod.setText("Production : {}".format(text_prod))

    def handle_tours_changed(self, text_edit_value):
        if text_edit_value == "":
            self.plan_prod.set_tours(0)
            self.text_edit_tours.setStyleSheet(line_edit_red_stylesheet)
        else:
            self.text_edit_tours.setStyleSheet(line_edit_green_stylesheet)
            self.plan_prod.set_tours(int(text_edit_value))
            if self.plan_prod.is_valid_tours():
                self.label_end.setStyleSheet(white_12_label_stylesheet)
                self.text_edit_tours.setStyleSheet(line_edit_green_stylesheet)
            else:
                self.label_end.setStyleSheet(red_12_bold_label_stylesheet)
                self.text_edit_tours.setStyleSheet(line_edit_red_stylesheet)
