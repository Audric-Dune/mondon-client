# !/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QHBoxLayout, QLineEdit, QLabel

from commun.constants.colors import color_bleu_gris
from commun.constants.stylesheets import line_edit_stylesheet, white_title_label_stylesheet
from commun.ui.public.mondon_widget import MondonWidget


class ArretWindowAjoutCommentaire(MondonWidget):
    HEIGHT_TEXT_EDIT = 24
    """
    Bloc d'ajout commentaire
    """
    def __init__(self, parent=None):
        super(ArretWindowAjoutCommentaire, self).__init__(parent=parent)
        self.set_background_color(color_bleu_gris)
        # _____INITIALISATION WIDGET_____
        self.line_edit = QLineEdit()
        self.init_widget()

    def init_widget(self):
        """
        Initialise le layout et insère le bouton validation
        """
        hbox = QHBoxLayout()
        label = QLabel('Commentaire')
        label.setFixedHeight(self.HEIGHT_TEXT_EDIT)
        label.setStyleSheet(white_title_label_stylesheet)
        hbox.addWidget(label)
        self.line_edit.setFixedHeight(self.HEIGHT_TEXT_EDIT)
        self.line_edit.setPlaceholderText("Entrer un commentaire si besoin")
        self.line_edit.setStyleSheet(line_edit_stylesheet)
        hbox.addWidget(self.line_edit)
        self.setLayout(hbox)
