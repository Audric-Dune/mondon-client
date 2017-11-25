# !/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QPushButton, QHBoxLayout
from PyQt5.QtCore import pyqtSignal

from constants.colors import color_bleu_gris
from constants.dimensions import button_size
from constants.stylesheets import button_stylesheet
from ui.utils.drawing import draw_rectangle
from ui.widgets.public.mondon_widget import MondonWidget


class ArretWindowAjoutRaison(MondonWidget):
    # Signal émit lorsque l'on veut ajouter une raison
    ADD_RAISON_SIGNAL = pyqtSignal()

    """
    Bloc de validation d'une raison d'arret
    S'active uniquement si on a séléctionné une raison
    """
    def __init__(self, parent=None):
        super(ArretWindowAjoutRaison, self).__init__(parent=parent)
        # _____INITIALISATION WIDGET_____
        self.bt_add = QPushButton("Ajouter", self)
        self.bt_add.clicked.connect(self.on_click_bt_add)
        self.init_widget()

    def init_widget(self):
        """
        Initialise le layout et insère le bouton validation
        """
        hbox = QHBoxLayout()
        self.bt_add.setFixedSize(200, button_size)
        self.bt_add.setStyleSheet(button_stylesheet)
        hbox.addWidget(self.bt_add)

        self.setLayout(hbox)

    def on_click_bt_add(self):
        """
        Emet un signal lorsque l'on click sur le bouton ajouter
        """
        self.ADD_RAISON_SIGNAL.emit()

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
