# !/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QWidget, QLabel, QLineEdit

from commun.constants.colors import color_bleu_gris
from commun.constants.param import LIMIT_JOURS_GESTION_EQUIPE
from commun.constants.stylesheets import (
    green_maj_label_stylesheet,
    white_16_bold_label_stylesheet,
    white_16_label_stylesheet,
    line_edit_stylesheet, )
from commun.lib.base_de_donnee import Database
from production.stores.settings_team_gestion_store import settings_team_gestion_store
from commun.ui.public.mondon_widget import MondonWidget
from commun.ui.public.checkbox_button import CheckboxButton
from commun.utils.layout import clear_layout
from commun.utils.timestamp import timestamp_to_name_number_day_month,\
    timestamp_after_day_ago,\
    timestamp_now,\
    timestamp_to_day,\
    timestamp_at_week_ago


class TabTeamGestion(MondonWidget):
    def __init__(self, parent=None):
        super(TabTeamGestion, self).__init__(parent)
        self.set_background_color(color_bleu_gris)
        self.hbox = QHBoxLayout()
        self.add_defaut_day()
        Database.add_defaut_day(1519081200)
        self.init_widget()

    def on_settings_team_gestion_changed(self):
        self.init_widget()

    def init_widget(self):
        clear_layout(self.hbox)
        widget = QWidget(parent=self)
        widget.setLayout(self.create_tab())
        widget.setStyleSheet("background-color:white;")
        self.hbox.addWidget(widget)
        self.setLayout(self.hbox)

    @staticmethod
    def is_weekend(ts_day):
        """
        Test si un ts correspond à un jour du weekend (samedi ou dimanche)
        :return: True si le ts correspond a un samedi ou dimanche sinon False
        """
        day = timestamp_to_day(ts_day)
        return day == "samedi" or day == "dimanche"

    def add_defaut_day(self):
        start_data = 1508709600
        limit_day = timestamp_after_day_ago(timestamp_now(), LIMIT_JOURS_GESTION_EQUIPE)
        ts_day_ago = start_data
        while ts_day_ago <= limit_day:
            if self.is_weekend(ts_day_ago):
                pass
            else:
                Database.add_defaut_day(ts_day_ago)
            ts_day_ago += 86400

    def create_tab(self):
        data = Database.get_team_gestion()
        content = QVBoxLayout()
        for values in data:
            start_day = values[0]
            start_week = timestamp_at_week_ago(settings_team_gestion_store.week_ago)
            start_next_week = timestamp_at_week_ago(settings_team_gestion_store.week_ago - 1)
            if start_week < start_day < start_next_week:
                content.addWidget(self.create_line(values))
        return content

    def create_line(self, values):
        background = MondonWidget(parent=self)
        background.set_background_color(color_bleu_gris)
        hbox = QHBoxLayout(background)
        hbox.addWidget(self.create_label(timestamp_to_name_number_day_month(values[0]), align=Qt.AlignCenter))
        hbox.addWidget(self.create_text_edit(values[1]))
        hbox.addWidget(self.create_text_edit(values[2]))
        hbox.addWidget(self.create_text_edit(values[3]))
        hbox.addWidget(self.create_checkbox())
        return background

    @staticmethod
    def create_text_edit(value):
        """
        S'occupe de créer un champs éditable
        """
        # On crée le champs éditable
        text_edit = QLineEdit()
        # On crée son placeholder
        text_edit.setText(str(value))
        text_edit.setStyleSheet(line_edit_stylesheet)
        text_edit.setAttribute(Qt.WA_MacShowFocusRect, 0)
        # text_edit.textChanged.connect(lambda: self.editable_item_change(text_edit.text(), index))
        return text_edit

    def create_checkbox(self):
        checkbox = CheckboxButton(parent=self)
        checkbox.setFixedSize(200, 200)
        return checkbox

    @staticmethod
    def create_label_tittle(text, align):
        """
        Crée un label titre
        :param text: Le texte du label
        :param align: L'alignement du label
        :return: Le label
        """
        label = QLabel(text)
        label.setStyleSheet(green_maj_label_stylesheet)
        label.setAlignment(align)
        label.setFixedHeight(40)
        return label

    @staticmethod
    def create_label(text, align, bold=False):
        """
        Crée un label standard (avec la possibilité de le mettre ne gras)
        :param text: Le texte du label
        :param align: L'alignement du label
        :return: Le label
        """
        text = str(text)
        label = QLabel(text.capitalize())
        if bold:
            label.setStyleSheet(white_16_bold_label_stylesheet)
        else:
            label.setStyleSheet(white_16_label_stylesheet)
        label.setAlignment(align)
        label.setFixedHeight(40)
        return label
