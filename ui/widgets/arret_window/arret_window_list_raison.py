# !/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtGui import QPainter, QIcon
from PyQt5.Qt import Qt
from PyQt5.QtWidgets import QLabel, QHBoxLayout, QVBoxLayout, QPushButton
from PyQt5.QtCore import QSize, QMargins, pyqtSignal

from constants.colors import color_bleu_gris
from constants.stylesheets import \
    gray_title_label_stylesheet, \
    red_title_label_stylesheet, \
    button_gray_cross_stylesheet,\
    button_red_cross_stylesheet
from ui.utils.drawing import draw_rectangle
from ui.utils.layout import clear_layout
from ui.widgets.public.pixmap_button import PixmapButton
from ui.widgets.public.mondon_widget import MondonWidget


class ArretWindowListRaison(MondonWidget):
    DELETE_RAISON_SIGNAL = pyqtSignal()
    # _____DEFINITION CONSTANTE CLASS_____
    WIDTH_TYPE = 120
    HEIGHT_LINE = 24
    SIZE = QSize(24, 24)
    VBOX_SPACING = 5
    VBOX_MARGIN = QMargins(10, 10, 10, 10)
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
        self.vbox.setContentsMargins(self.VBOX_MARGIN)
        self.vbox.setSpacing(self.VBOX_SPACING)
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
            self.initial_line = self.create_initial_line()
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
        # On regarde si il y a plus de raison dans l'object Arret que dans le layout
        if len(list_raison) > len(self.list_layout_raison):
            # Si il n'y a pas de ligne, on supprime la ligne initiale
            if len(self.list_layout_raison) == 0:
                item_layout = self.vbox.itemAt(0)
                self.vbox.removeItem(item_layout)
                self.initial_line = clear_layout(self.initial_line)
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
            self.update_widget()

    def create_initial_line(self):
        """
        S'occupe de créer une ligne si l'arret contient aucune raison
        :return: Le layout de la ligne
        """
        # Création widget horizontal
        hbox = QHBoxLayout()
        # Création du label
        initial_label = QLabel("Aucune raison renseignée pour cette arrêt")
        initial_label.setFixedHeight(self.HEIGHT_LINE)
        initial_label.setAlignment(Qt.AlignCenter)
        # On met le label en rouge
        initial_label.setStyleSheet(red_title_label_stylesheet)
        # On ajoute le label au layout
        hbox.addWidget(initial_label)
        return hbox

    def create_line_raison(self, raison):
        """
        S'occupe de créer une ligne associé a une raison
        :return: Le layout de la ligne
        """
        # Création widget horizontal
        hbox = QHBoxLayout()
        # Création du label type
        type_label = QLabel(raison.type)
        # On met le label en couleur en fonction du type et on définit la largeur
        label_stylesheet = gray_title_label_stylesheet if raison.type == "Prévu" else red_title_label_stylesheet
        type_label.setStyleSheet(label_stylesheet)
        type_label.setAlignment(Qt.AlignCenter)
        type_label.setFixedWidth(self.WIDTH_TYPE)
        type_label.setFixedHeight(self.HEIGHT_LINE)
        # On ajoute le label au layout
        hbox.addWidget(type_label)
        # Création du label raison
        raison_label = QLabel(raison.raison)
        # On met le label en couleur en fonction du type et on définit la largeur
        raison_label.setStyleSheet(label_stylesheet)
        # On ajoute le label au layout
        hbox.addWidget(raison_label)
        # On crée un bouton pour supprimer la ligne
        bt_cross = PixmapButton(parent=self)
        bt_cross.setFixedSize(self.HEIGHT_LINE, self.HEIGHT_LINE)
        bt_cross.set_image("assets/images/white_cross.png")
        bt_cross_stylesheet = button_gray_cross_stylesheet if raison.type == "Prévu" else button_red_cross_stylesheet
        bt_cross.setStyleSheet(bt_cross_stylesheet)
        bt_cross.clicked.connect(lambda: self.delete_line_raison(raison.raison))
        # On ajoute le bouton au layout
        hbox.addWidget(bt_cross)
        hbox.setSpacing(0)
        return hbox

    def delete_line_raison(self, raison):
        """
        S'occupe de supprimer une ligne raison
        :param raison: La raison a supprimer
        """
        # Supprime l'object Raison dans l'object Arret
        self.arret.remove_raison(raison)
        # Réinitialise la liste des layout raison
        self.list_layout_raison = {}
        self.vbox = clear_layout(self.vbox)
        self.init_widget()
        self.DELETE_RAISON_SIGNAL.emit()

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
