# !/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtCore import QSize, pyqtSignal
from PyQt5.QtGui import QPainter, QIcon
from PyQt5.QtWidgets import QPushButton, QLabel, QHBoxLayout, QVBoxLayout

from constants.colors import color_bleu_gris
from constants.param import LIST_CHOIX_RAISON_PREVU, LIST_CHOIX_RAISON_IMPREVU
from constants.stylesheets import \
    check_box_off_stylesheet, \
    check_box_on_stylesheet, \
    check_box_unselected_stylesheet, \
    white_title_label_stylesheet, \
    disable_16_label_stylesheet
from ui.utils.drawing import draw_rectangle
from ui.widgets.public.dropdown import Dropdown
from ui.widgets.public.mondon_widget import MondonWidget


class ArretWindowListRaison(MondonWidget):

    """
    Bloc de visualisation des raison de la window arret
    Affiche la liste des raisons ajouter a l'arret
    """
    def __init__(self, arret, parent=None):
        super(ArretWindowListRaison, self).__init__(parent=parent)
        self.arret = arret
        self.list_layout_raison = {}
        # _____INITIALISATION WIDGET_____
        self.vbox = QVBoxLayout(self)
        self.initial_line = self.create_initial_line()
        self.init_widget()

    def init_widget(self):
        """
        Initialise les layouts et insère les raisons
        """
        # On récupère la liste des raisons sotcké dans l'object Arret
        list_raison = self.arret.raisons
        # Si la liste de raison est vide
        if len(list_raison) == 0:
            # On ajout la ligne pas de raison sélectionné
            self.vbox.addLayout(self.initial_line)
        else:
            # On parcour la liste des raisons
            index = 0
            for raison in list_raison:
                # On crée la nouvelle ligne
                line_raison = self.create_line_raison(raison)
                # On ajoute la ligne a la liste des layouts
                self.list_layout_raison[index] = line_raison
                # On ajoute la ligne au layout
                self.vbox.addLayout(line_raison)
                index += 1
        self.setLayout(self.vbox)

    def update_widget(self):
        # On récupère la liste des raisons sotcké dans l'object Arret
        list_raison = self.arret.raisons
        # On regarde si il ya plus de raison dans l'object Arret que dans le layout
        if len(list_raison) > len(self.list_layout_raison):
            # Si il n'y a pas de ligne, on supprime la ligne initiale
            if len(self.list_layout_raison) == 0:
                item_layout = self.vbox.itemAt(0)
                self.vbox.removeItem(item_layout)
                self.clear_layout(self.initial_line)
            # La longeur de la liste des layouts correspond a l'index de la raison
            # dans list_raison que l'on veux insérer
            index = len(self.list_layout_raison)
            # On sélectionne la raison à ajouter
            raison = list_raison[index]
            # On crée la nouvelle ligne
            line_raison = self.create_line_raison(raison)
            # On ajoute la ligne a la liste des layouts
            self.list_layout_raison[index] = line_raison
            # On ajoute la ligne au layout
            self.vbox.addLayout(line_raison)

    @staticmethod
    def create_initial_line():
        """
        S'occupe de créer une ligne si l'arret contient aucune raison
        :return: Le layout de la line
        """
        # Création widget horizontal
        hbox = QHBoxLayout()
        # Création du label
        initial_label = QLabel("Aucune raison renseignée pour cette arrêt")
        # On met le label en blanc
        initial_label.setStyleSheet(white_title_label_stylesheet)
        # On ajoute le label au layout
        hbox.addWidget(initial_label)
        return hbox

    @staticmethod
    def create_line_raison(raison):
        """
        S'occupe de créer une ligne si l'arret contient aucune raison
        :return: Le layout de la line
        """
        # Création widget horizontal
        hbox = QHBoxLayout()
        # Création du label type
        type_label = QLabel(raison.type)
        # On met le label en blanc
        type_label.setStyleSheet(white_title_label_stylesheet)
        # On ajoute le label au layout
        hbox.addWidget(type_label)
        # Création du label raison
        raison_label = QLabel(raison.raison)
        # On met le label en blanc
        raison_label.setStyleSheet(white_title_label_stylesheet)
        # On ajoute le label au layout
        hbox.addWidget(raison_label)
        hbox.addStretch(1)
        return hbox

    @staticmethod
    def clear_layout(layout):
        """
        Supprime tous les enfant d'un layout
        :param layout: Le layout a clear
        :return:
        """
        # On boucle jusqu'a se que le layout soit vide
        while layout.count():
            # On sélectionne le premiere enfant
            child = layout.takeAt(0)
            # Si c'est un widget on le supprime
            if child.widget():
                child.widget().deleteLater()

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
