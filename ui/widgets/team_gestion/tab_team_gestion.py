# !/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QWidget, QScrollArea, QLabel, QLineEdit
from PyQt5.QtCore import Qt

from constants.colors import color_bleu_gris
from constants.stylesheets import scroll_bar_stylesheet,\
    green_maj_label_stylesheet,\
    white_16_bold_label_stylesheet,\
    white_16_label_stylesheet,\
    line_edit_stylesheet
from ui.utils.timestamp import timestamp_to_name_number_day_month
from lib.base_de_donnee import Database
from ui.widgets.public.mondon_widget import MondonWidget


class TabTeamGestion(MondonWidget):
    def __init__(self, parent=None):
        super(TabTeamGestion, self).__init__(parent)
        self.set_background_color(color_bleu_gris)
        self.init_widget()

    def init_widget(self):
        hbox = QHBoxLayout()
        widget = QWidget(parent=self)
        widget.setLayout(self.create_tab())
        widget.setStyleSheet("background-color:white;")
        scroll_bar = QScrollArea()
        scroll_bar.setWidget(widget)
        scroll_bar.setStyleSheet(scroll_bar_stylesheet)
        scroll_bar.setAlignment(Qt.AlignCenter)
        hbox.addWidget(scroll_bar)
        self.setLayout(hbox)

    def create_tab(self):
        data = Database.get_team_gestion()
        content_scroll = QVBoxLayout()
        for values in data:
            content_scroll.addWidget(self.create_line(values))
        return content_scroll

    def create_line(self, values):
        background = MondonWidget(parent=self)
        background.set_background_color(color_bleu_gris)
        hbox = QHBoxLayout(background)
        hbox.addWidget(self.create_label(timestamp_to_name_number_day_month(values[0]), align=Qt.AlignCenter))
        hbox.addWidget(self.create_text_edit(values[1]))
        hbox.addWidget(self.create_text_edit(values[2]))
        hbox.addWidget(self.create_text_edit(values[3]))
        hbox.addWidget(self.create_text_edit(values[4]))
        return background

    def create_text_edit(self, placeholder):
        """
        S'occupe de créer un champs éditable
        :param data_text_edit: Donnée du champs
        :param index: L'index du champs éditable
        """
        # On crée le champs éditable
        text_edit = QLineEdit()
        # On crée son placeholder
        text_edit.setPlaceholderText(str(placeholder))
        text_edit.setStyleSheet(line_edit_stylesheet)
        text_edit.setAttribute(Qt.WA_MacShowFocusRect, 0)
        # text_edit.textChanged.connect(lambda: self.editable_item_change(text_edit.text(), index))
        return text_edit

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
