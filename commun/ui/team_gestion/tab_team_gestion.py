# !/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtCore import Qt, QEvent
from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QWidget, QLabel, QLineEdit

from commun.constants.colors import color_bleu_gris, color_blanc
from commun.constants.param import LIMIT_JOURS_GESTION_EQUIPE
from commun.constants.stylesheets import (
    green_maj_label_stylesheet,
    white_16_bold_label_stylesheet,
    white_16_label_stylesheet,
    line_edit_stylesheet)
from commun.lib.base_de_donnee import Database
from production.stores.settings_team_gestion_store import settings_team_gestion_store
from commun.ui.public.mondon_widget import MondonWidget
from commun.ui.public.checkbox_button import CheckboxButton
from commun.ui.public.text_edit import TextEdit
from commun.utils.layout import clear_layout
from commun.utils.timestamp import timestamp_to_name_number_day_month, timestamp_at_week_ago


class TabTeamGestion(MondonWidget):
    def __init__(self, parent=None):
        super(TabTeamGestion, self).__init__(parent)
        self.installEventFilter(self)
        self.set_background_color(color_bleu_gris)
        self.hbox = QHBoxLayout()
        self.array_text_edit = []
        self.content_tab = QVBoxLayout()
        self.current_data = None
        self.init_widget()

    def on_settings_team_gestion_changed(self):
        self.init_widget()

    def add_data(self):
        self.current_data = []
        all_data = Database.get_team_gestion()
        for data in all_data:
            start_day = data[0]
            start_week = timestamp_at_week_ago(settings_team_gestion_store.week_ago)
            start_next_week = timestamp_at_week_ago(settings_team_gestion_store.week_ago - 1)
            if start_week <= start_day < start_next_week:
                self.current_data.append(data)
        print(self.current_data)

    def init_widget(self):
        self.add_data()
        self.create_tab()
        self.setLayout(self.content_tab)
    #     clear_layout(self.hbox)
    #     widget = QWidget(parent=self)
    #     widget.setLayout(self.create_tab())
    #     widget.setStyleSheet("background-color:white;")
    #     self.hbox.addWidget(widget)
    #     self.setLayout(self.hbox)

    def create_tab(self):
        clear_layout(self.content_tab)
        self.array_text_edit = []
        for values in self.current_data:
            self.content_tab.addLayout(self.create_line(values))
            print(values)

    def create_line(self, data):
        line = QHBoxLayout()
        line.addWidget(self.create_label(timestamp_to_name_number_day_month(data[0]), align=Qt.AlignCenter))
        line.addWidget(self.create_text_edit(data[1]))
        line.addWidget(self.create_checkbox(data[2]))
        return line

    def create_text_edit(self, value):
        """
        S'occupe de créer un champs éditable
        """
        # On crée le champs éditable
        text_edit = TextEdit()
        text_edit.setText(str(value))
        text_edit.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        text_edit.setStyleSheet(line_edit_stylesheet)
        text_edit.setAttribute(Qt.WA_MacShowFocusRect, 0)
        text_edit.setFixedSize(20, 20)
        text_edit.setValidator(QIntValidator(0, 24))
        text_edit.returnPressed.connect(lambda: self.editable_item_change(text_edit.text(), text_edit, clear_focus=True))
        text_edit.textChanged.connect(lambda: self.editable_item_change(text_edit.text(), text_edit))
        self.array_text_edit.append(text_edit)
        return text_edit

    @staticmethod
    def editable_item_change(text, text_edit, clear_focus=False):
        if text == "":
            text_edit.setText("0")
        if clear_focus:
            text_edit.clearFocus()
        print(text)

    def create_checkbox(self, state):
        state = False if state == 1 else True
        checkbox = CheckboxButton(parent=self, is_check=state)
        checkbox.setFixedSize(20, 20)
        return checkbox
    #
    # @staticmethod
    # def create_label_tittle(text, align):
    #     """
    #     Crée un label titre
    #     :param text: Le texte du label
    #     :param align: L'alignement du label
    #     :return: Le label
    #     """
    #     label = QLabel(text)
    #     label.setStyleSheet(green_maj_label_stylesheet)
    #     label.setAlignment(align)
    #     label.setFixedHeight(40)
    #     return label

    @staticmethod
    def create_label(text, align, bold=False):
        """
        Crée un label standard (avec la possibilité de le mettre en gras)
        :param text: Le texte du label
        :param align: L'alignement du label
        :param bold: Mise en gras ou non
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

    def eventFilter(self, object, event):
        if event.type() == QEvent.MouseButtonPress:
            for text_edit in self.array_text_edit:
                text_edit.clearFocus()
            return True
        return False
