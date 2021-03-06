# !/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QPushButton, QHBoxLayout

from commun.constants.colors import color_bleu_gris
from commun.constants.dimensions import button_size
from commun.constants.stylesheets import button_stylesheet
from commun.ui.public.mondon_widget import MondonWidget


class ArretWindowAjoutRaison(MondonWidget):
    # Signal émit lorsque l'on veut ajouter une raison
    ADD_RAISON_SIGNAL = pyqtSignal()
    # _____DEFINITION CONSTANTE CLASS_____
    BUTTON_WIDTH = 200
    """
    Bloc de validation d'une raison d'arret
    S'active uniquement si on a séléctionné une raison
    """
    def __init__(self, parent=None):
        super(ArretWindowAjoutRaison, self).__init__(parent=parent)
        self.set_background_color(color_bleu_gris)
        # _____INITIALISATION WIDGET_____
        self.bt_add = QPushButton("Ajouter", self)
        self.bt_add.clicked.connect(self.on_click_bt_add)
        self.init_widget()

    def init_widget(self):
        """
        Initialise le layout et insère le bouton validation
        """
        hbox = QHBoxLayout()
        self.bt_add.setFixedSize(self.BUTTON_WIDTH, button_size)
        self.bt_add.setStyleSheet(button_stylesheet)
        hbox.addWidget(self.bt_add)

        self.setLayout(hbox)

    def on_click_bt_add(self):
        """
        Emet un signal lorsque l'on click sur le bouton ajouter
        """
        self.ADD_RAISON_SIGNAL.emit()