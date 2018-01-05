# !/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QPushButton, QHBoxLayout

from constants.colors import color_bleu_gris
from constants.dimensions import button_size
from constants.stylesheets import button_stylesheet, button_stylesheet_unselected
from ui.widgets.public.mondon_widget import MondonWidget


class ArretWindowSelectType(MondonWidget):
    # _____DEFINITION CONSTANTE CLASS_____
    BUTTON_WIDTH = 200
    """
    Bloc sélection du type d'arret
    Affiche et met a jour le style des boutons "Prévu" et "Imprévu"
    """
    def __init__(self, arret, parent=None):
        super(ArretWindowSelectType, self).__init__(parent=parent)
        self.set_background_color(color_bleu_gris)
        self.arret = arret
        self.type_selected = None
        # _____INITIALISATION WIDGET_____
        self.bt_prevu = QPushButton("Raison prévue", self)
        self.bt_prevu.clicked.connect(self.on_click_bt_prevu)
        self.bt_imprevu = QPushButton("Raison imprévue", self)
        self.bt_imprevu.clicked.connect(self.on_click_bt_imprevu)
        self.bt_entretien = QPushButton("Nettoyage", self)
        self.bt_entretien.clicked.connect(self.on_click_bt_entretien)
        self.init_widget()

    def init_widget(self):
        """
        Initialise le layout et insère les boutons
        """
        hbox = QHBoxLayout()
        self.bt_prevu.setFixedSize(self.BUTTON_WIDTH, button_size)
        self.bt_prevu.setStyleSheet(button_stylesheet)
        hbox.addWidget(self.bt_prevu)
        self.bt_imprevu.setFixedSize(self.BUTTON_WIDTH, button_size)
        self.bt_imprevu.setStyleSheet(button_stylesheet)
        hbox.addWidget(self.bt_imprevu)
        self.bt_entretien.setFixedSize(self.BUTTON_WIDTH, button_size)
        self.bt_entretien.setStyleSheet(button_stylesheet)
        hbox.addWidget(self.bt_entretien)

        self.setLayout(hbox)

    def on_data_changed(self):
        """
        Fonction héritée de mondon_widget
        Est appelé automatiquement après modification des data
        """
        self.update()

    def on_click_bt_prevu(self):
        """
        Fonction appelé après un click sur le bouton "Prévu"
        Met à jour les styles des boutons
        Met a jour la variable mémoire de séléction d'un type dans l'object Arret
        """
        # De base met le style select sur le bouton "Prévu"
        # De base met le style unselect sur le bouton "Imprévu"
        self.bt_prevu.setStyleSheet(button_stylesheet)
        self.bt_imprevu.setStyleSheet(button_stylesheet_unselected)
        self.bt_entretien.setStyleSheet(button_stylesheet_unselected)

        # Si la variable mémoire de séléction d'un type dans l'object Arret est "Prévu",
        # on a déja sélectionner le bouton "Prévu"
        if self.arret.type_cache == "Prévu":
            # Dans se cas on met le style select sur le bouton "Imprévu"
            self.bt_imprevu.setStyleSheet(button_stylesheet)
            self.bt_entretien.setStyleSheet(button_stylesheet)
        # On met a jour la variable mémoire de séléction d'un type dans l'object Arret
        self.arret.add_type_cache("Prévu")

    def on_click_bt_imprevu(self):
        """
        Fonction appelé après un click sur le bouton "Imprévu"
        Met à jour les styles des boutons
        Met a jour la variable mémoire de séléction d'un type dans l'object Arret
        """
        # De base met le style select sur le bouton "Imprévu"
        # De base met le style unselect sur le bouton "Prévu"
        # De base met le style unselect sur le bouton "Nettoyage"
        self.bt_prevu.setStyleSheet(button_stylesheet_unselected)
        self.bt_imprevu.setStyleSheet(button_stylesheet)
        self.bt_entretien.setStyleSheet(button_stylesheet_unselected)
        # Si la variable mémoire de séléction d'un type dans l'object Arret est "Imprévu",
        # on a déja sélectionner le bouton "Imprévu"
        if self.arret.type_cache == "Imprévu":
            # Dans se cas on met le style select sur le bouton "Prévu"
            self.bt_prevu.setStyleSheet(button_stylesheet)
            self.bt_entretien.setStyleSheet(button_stylesheet)
        # On met a jour la variable mémoire de séléction d'un type dans l'object Arret
        self.arret.add_type_cache("Imprévu")

    def on_click_bt_entretien(self):
        """
        Fonction appelé après un click sur le bouton "Nettoyage"
        Met à jour les styles des boutons
        Met a jour la variable mémoire de séléction d'un type dans l'object Arret
        """
        # De base met le style select sur le bouton "Imprévu"
        # De base met le style unselect sur le bouton "Prévu"
        self.bt_prevu.setStyleSheet(button_stylesheet_unselected)
        self.bt_entretien.setStyleSheet(button_stylesheet)
        self.bt_imprevu.setStyleSheet(button_stylesheet_unselected)
        # Si la variable mémoire de séléction d'un type dans l'object Arret est "Prévu",
        # on a déja sélectionner le bouton "Prévu"
        if self.arret.type_cache == "Nettoyage":
            # Dans se cas on met le style select sur le bouton "Prévu"
            self.bt_prevu.setStyleSheet(button_stylesheet)
            self.bt_imprevu.setStyleSheet(button_stylesheet)
        # On met a jour la variable mémoire de séléction d'un type dans l'object Arret
        self.arret.add_type_cache("Nettoyage")

    def remove_type(self):
        """
        Réintialise les boutons
        """
        self.bt_prevu.setStyleSheet(button_stylesheet)
        self.bt_imprevu.setStyleSheet(button_stylesheet)
        self.bt_entretien.setStyleSheet(button_stylesheet)
