# !/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtCore import QSize, pyqtSignal
from PyQt5.QtGui import QPainter, QIcon
from PyQt5.QtWidgets import QPushButton, QLabel, QHBoxLayout, QVBoxLayout, QTextEdit

from constants.colors import color_bleu_gris
from constants.param import LIST_CHOIX_RAISON_PREVU, LIST_CHOIX_RAISON_IMPREVU
from constants.stylesheets import \
    check_box_off_stylesheet, \
    check_box_on_stylesheet, \
    white_title_label_stylesheet
from ui.utils.drawing import draw_rectangle
from ui.widgets.public.dropdown import Dropdown
from ui.widgets.public.mondon_widget import MondonWidget


class ArretWindowSelectRaison(MondonWidget):
    # Création du signal qui indique que les conditions pour valider la sélection on changé
    VALIDATION_CONDITION_SIGNAL = pyqtSignal(bool)
    # _____DEFINITION CONSTANTE CLASS_____
    SIZE = QSize(24, 24)
    HEIGHT_TEXT_EDIT = 24
    """
    Bloc sélection raison de la window arret
    Affiche le temps de l'arret, l'heure de début et le jour
    """
    def __init__(self, arret, parent=None):
        super(ArretWindowSelectRaison, self).__init__(parent=parent)
        arret.ARRET_RAISON_CHANGED_SIGNAL.connect(self.update_widget)
        self.arret = arret
        self.list_choix = LIST_CHOIX_RAISON_PREVU if self.arret.type_cache == "Prévu" else LIST_CHOIX_RAISON_IMPREVU
        self.items = []
        self.buttons = []
        self.validation_condition = False
        self.raison_index_selected = []
        # _____INITIALISATION WIDGET_____
        self.vbox = QVBoxLayout()
        self.init_widget()

    def init_widget(self):
        """
        Initialise les layouts et insère les labels et dropdown définit dans les params du programme
        """
        index = 0
        # On parcour la liste de choix définit dans les params du programme
        for tupple in self.list_choix:
            # La première valeur correspond au format
            format = tupple[0]
            # La 2e valeur correspond au donnée
            value = tupple[1]
            # On initialise un layout horisontal et on ajoute le boutton
            hbox = QHBoxLayout()
            # On crée la checkbox liée a l'item
            self.buttons.append(self.create_check_button(index))
            # On ajoute la check box au layout
            hbox.addWidget(self.buttons[index])
            # On crée un item qui correspond au format
            if format == "label":
                self.items.append((format, self.create_label(value)))
            elif format == "dropdown":
                self.items.append((format, self.create_dropdown(value, index)))
                # On ajoute un label titre au layout
                label_dropdown = QLabel(value["titre"])
                label_dropdown.setStyleSheet(white_title_label_stylesheet)
                hbox.addWidget(label_dropdown)
            elif format == "text_edit":
                self.items.append((format, self.create_text_edit(value, index)))
                # On ajoute un label titre au layout
                label_dropdown = QLabel(value["titre"])
                label_dropdown.setStyleSheet(white_title_label_stylesheet)
                hbox.addWidget(label_dropdown)
            hbox.addWidget(self.items[index][1])
            hbox.addStretch(1)
            # On ajout le layout horisontal au layout principal vertical
            self.vbox.addLayout(hbox)
            index += 1
        # On ajout set le layout vertical
        self.setLayout(self.vbox)

    def update_widget(self):
        """
        Met a jour les styles des widgets
        """
        index = 0
        # On parcour l'ensemble des checkboxs
        while index < len(self.buttons):
            # Si le boutton est sélectionné
            if self.is_selected(index):
                # On active la ligne boutton
                self.activate_line(button=self.buttons[index], item=self.items[index])
            # Sinon on initialise la ligne
            else:
                # On désactive la ligne boutton
                self.initialise_line(button=self.buttons[index], item=self.items[index])
            index += 1

    @staticmethod
    def initialise_line(button, item):
        """
        S'occupe d'initialiser une ligne
        :param button: le boutton de la ligne
        :param item: l'item de la ligne
        """
        format = item[0]
        object = item[1]
        # On met le style check box sur off
        button.setStyleSheet(check_box_off_stylesheet)
        # On remove l'icon au cas ou
        button.setIcon(QIcon())
        # Si l'item est un label on le passe en blanc
        if format == "label":
            object.setStyleSheet(white_title_label_stylesheet)
        # Si l'item est une dropdown on la cache
        if format == "dropdown":
            object.hide()

    def activate_line(self, button, item):
        """
        S'occupe d'activer une ligne
        :param button: le boutton de la ligne
        :param item: l'item de la ligne
        """
        format = item[0]
        object = item[1]
        # On met le style check box sur on
        button.setStyleSheet(check_box_on_stylesheet)
        # On met l'icon check
        self.set_icon_check_on_checkbox(button)
        # Si l'item est une dropdown on l'affiche
        if format == "dropdown" or format == "text_edit":
            object.show()

    def onclick_button(self, index):
        """
        S'occupe de gérer le click sur une checkbox
        :param index: l'index du boutton clické
        """
        # Si on click sur une checkbox déja sélectionnée
        if self.is_selected(index):
            # On supprime l'index du bouton de la liste des indexs sélectionnés
            self.raison_index_selected.remove(index)
            # On met a jour la variable mémoire de séléction des raisons dans l'object Arret
            self.arret.remove_raison_cache(index)
            # On test si il reste des indexs dans la liste des indexs sélectionnés
            self.check_valid_condition()
            self.update_widget()
        else:
            # On ajoute l'index du bouton de la liste des indexs sélectionnés
            self.raison_index_selected.append(index)
            # On met a jour la variable mémoire de séléction des raisons dans l'object Arret
            self.arret.add_raison_cache(index, None)
            self.check_valid_condition()

    def style_choice(self, text, index):
        """
        S'occupe de gérer la sélection dans une dropdown
        :param text: Le texte sélectionné
        :param index: L'index de la drop_down sélectionné
        """
        # On met a jour la variable mémoire de séléction d'une raison dans l'object Arret
        self.arret.add_raison_cache(index, text)
        self.check_valid_condition()

    def is_selected(self, index_research):
        if self.raison_index_selected:
            for index in self.raison_index_selected:
                if index == index_research:
                    return True
        return False

    def connect_button(self, button, index):
        """
        S'occupe de créer une connection entre la fonction onclick_button et un boutton
        :param button: Le boutton a connecter
        :param index: L'index du boutton a connecter
        """
        button.clicked.connect(lambda: self.onclick_button(index))

    def create_check_button(self, index):
        """
        S'occupe de créer une chexbox
        :param index: index du boutton
        :return: Le boutton initialisé
        """
        # On crée un boutton vide
        button = QPushButton("")
        # On set sa taille
        button.setFixedSize(self.SIZE)
        # On met le style a off
        button.setStyleSheet(check_box_off_stylesheet)
        # On appel la fonction de connection
        self.connect_button(button, index)
        return button

    def set_icon_check_on_checkbox(self,button):
        """
        S'occupe de check une checkbox
        :param button: Le boutton a checker
        """
        # On importe l'image de check
        img = QIcon("assets/images/white_cross.png")
        # On set l'image de check au bouton
        button.setIcon(img)
        # On initialise la taille de l'image
        button.setIconSize(self.SIZE)

    @staticmethod
    def create_label(text):
        """
        S'occupe de créer un label
        :param text: Texte du label
        :return: Le texte initialisé
        """
        # On crée un label avec son texte
        label = QLabel(text)
        # On met la couleur du texte en blanc
        label.setStyleSheet(white_title_label_stylesheet)
        return label

    def create_dropdown(self, data_dropdown, index):
        """
        S'occupe de créer une dropdown
        :param data_dropdown: Les données de la dropdown
        :param index: L'index de la dropdown
        :return: La dropdown initialisée
        """
        # On crée l'object Dropdown
        dropdown = Dropdown(index)
        # On crée son placeholder
        dropdown.set_placeholder(data_dropdown["placeholder"])
        # On parcour les valeurs a insérer dans la dropdown
        for value in data_dropdown["values"]:
            # On ajoute la valeur a la dropdown
            dropdown.add_item(value)
        # On connect la dropdown a la fonction style_choice
        dropdown.VALUE_SELECTED_SIGNAL.connect(self.style_choice)
        # On cache la dropdown
        dropdown.hide()
        return dropdown

    def create_text_edit(self, data_text_edit, index):
        """
        S'occupe de créer un champs éditable
        :param data_text_edit: Donnée du champs
        :param index: L'index du champs éditable
        """
        # On crée le champs éditable
        text_edit = QTextEdit()
        # On crée son placeholder
        text_edit.setPlaceholderText(data_text_edit["placeholder"])
        # On cache le champs éditable
        text_edit.hide()
        text_edit.setFixedHeight(self.HEIGHT_TEXT_EDIT)
        return text_edit

    def check_valid_condition(self):
        check = True
        if not self.raison_index_selected:
            check = False
        else:
            for index in self.raison_index_selected:
                if self.items[index][0] == "label":
                    pass
                elif self.items[index][0] == "dropdown":
                    if self.items[index][1].selected:
                        pass
                    else:
                        check = False
                        break
        if check:
            self.validation_condition = True
            self.VALIDATION_CONDITION_SIGNAL.emit(True)
        else:
            self.validation_condition = False
            self.VALIDATION_CONDITION_SIGNAL.emit(False)

    def draw_fond(self, p):
        """
        Dessine un rectangle de la taille du bloc
        :param p: parametre de dessin
        """
        draw_rectangle(p, 0, 0, self.width(), self.height(), color_bleu_gris)

    def paintEvent(self, event):
        p = QPainter()
        p.begin(self)
        self.draw(p)
        p.end()

    def draw(self, p):
        self.draw_fond(p)
