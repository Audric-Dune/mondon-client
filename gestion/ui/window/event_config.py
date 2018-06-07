# !/usr/bin/env python
# -*- coding: utf-8 -*-


from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QVBoxLayout, QPushButton
from PyQt5.QtCore import Qt

from commun.constants.stylesheets import white_16_bold_label_stylesheet, \
    white_14_label_no_background_stylesheet, \
    button_little_stylesheet,\
    button_little_red_stylesheet
from commun.ui.public.text_edit import TextEdit
from commun.constants.colors import color_bleu_gris


class EventConfig(QWidget):
    WIDTH_TEXT_EDIT = 30

    def __init__(self, type_event):
        super(EventConfig, self).__init__(None)
        self.setWindowFlags(Qt.Dialog)
        self.type_event = type_event
        self.start = None
        self.start_hour = TextEdit(number_only=True, number_min=6,
                                   number_max=22, width=self.WIDTH_TEXT_EDIT, alignement="center", init_value="")
        self.start_min = TextEdit(number_only=True, number_min=0,
                                  number_max=59, init_value=0, width=self.WIDTH_TEXT_EDIT, alignement="center")
        self.duration = None
        self.duration_hour = TextEdit(number_only=True, number_min=0,
                                      number_max=16, width=self.WIDTH_TEXT_EDIT, alignement="center", init_value="-")
        self.duration_min = TextEdit(number_only=True, number_min=0,
                                     number_max=59, init_value="-", width=self.WIDTH_TEXT_EDIT, alignement="center")
        self.end = None
        self.end_hour = TextEdit(number_only=True, number_min=6,
                                 number_max=22, width=self.WIDTH_TEXT_EDIT, alignement="center", init_value="-")
        self.end_min = TextEdit(number_only=True, number_min=0,
                                number_max=59, init_value=0, width=self.WIDTH_TEXT_EDIT, alignement="center")
        self.ensemble = None
        self.info = None
        self.init_widget()
        self.show()

    def is_valid_event(self):
        if self.start and self.end:
            return True
        return False

    def init_widget(self):
        vbox = QVBoxLayout()
        vbox.setContentsMargins(5, 5, 5, 5)
        vbox.addWidget(self.get_bloc_title())
        vbox.addWidget(self.get_bloc_settings())
        vbox.addWidget(self.get_bloc_bt())
        self.setLayout(vbox)

    def get_bloc_title(self):
        title_contain = QWidget(parent=self)
        self.set_background_color(title_contain)
        title_label = QLabel(self.get_title())
        title_label.setStyleSheet(white_16_bold_label_stylesheet)
        title_contain_hbox = QHBoxLayout()
        title_contain_hbox.addWidget(title_label)
        title_contain.setLayout(title_contain_hbox)
        return title_contain

    def get_bloc_settings(self):
        settings_contain = QWidget(parent=self)
        self.set_background_color(settings_contain)
        settings_contain_vbox = QVBoxLayout()
        settings_contain_vbox.addLayout(self.get_line_setting("Début :", self.start_hour, self.start_min))
        settings_contain_vbox.addLayout(self.get_line_setting("Durée :", self.duration_hour, self.duration_min))
        settings_contain_vbox.addLayout(self.get_line_setting("Fin :", self.end_hour, self.end_min))
        settings_contain.setLayout(settings_contain_vbox)
        return settings_contain

    @staticmethod
    def get_line_setting(text, text_edit_hour, text_edit_min):
        hbox = QHBoxLayout()
        hbox.setSpacing(0)
        label = QLabel(text)
        label.setStyleSheet(white_14_label_no_background_stylesheet)
        hbox.addWidget(label)
        hbox.addStretch()
        hbox.addWidget(text_edit_hour)
        double_point_label = QLabel("h :")
        double_point_label.setStyleSheet(white_14_label_no_background_stylesheet)
        hbox.addWidget(double_point_label)
        hbox.addWidget(text_edit_min)
        min_label = QLabel("min")
        min_label.setStyleSheet(white_14_label_no_background_stylesheet)
        hbox.addWidget(min_label)
        return hbox

    def get_bloc_bt(self):
        bt_contain = QWidget(parent=self)
        self.set_background_color(bt_contain)
        bt_contain_hbox = QHBoxLayout()
        bt_valid = QPushButton("Validé")
        bt_valid.setStyleSheet(button_little_stylesheet)
        bt_valid.setFixedSize(80, 25)
        bt_cancel = QPushButton("Annulé")
        bt_cancel.clicked.connect(self.close)
        bt_cancel.setStyleSheet(button_little_red_stylesheet)
        bt_cancel.setFixedSize(80, 25)
        bt_contain_hbox.addWidget(bt_valid)
        bt_contain_hbox.addWidget(bt_cancel)
        bt_contain.setLayout(bt_contain_hbox)
        return bt_contain

    def get_title(self):
        if self.type_event == "clean":
            return "Ajouter un nettoyage machine"

    @staticmethod
    def set_background_color(widget):
        widget.setStyleSheet(
            "background-color:{color_bleu_gris};".format(color_bleu_gris=color_bleu_gris.hex_string)
        )
