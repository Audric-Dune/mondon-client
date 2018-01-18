# !/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QPushButton, QHBoxLayout
from commun.constants.colors import color_bleu_gris

from commun.constants.dimensions import button_size
from commun.constants.stylesheets import button_stylesheet
from commun.ui.public.mondon_widget import MondonWidget


class ArretWindowFinish(MondonWidget):
    # Signal émit lorsque l'on veut ajouter une raison
    FINISH_SIGNAL = pyqtSignal()
    # _____DEFINITION CONSTANTE CLASS_____
    BUTTON_WIDTH = 200
    """
    Bloc pour fermer la fenetre apres modification
    S'active uniquement si on a séléctionné une raison
    """
    def __init__(self, parent=None):
        super(ArretWindowFinish, self).__init__(parent=parent)
        self.set_background_color(color_bleu_gris)
        # _____INITIALISATION WIDGET_____
        self.bt_finish = QPushButton("Terminer", self)
        self.bt_finish.clicked.connect(self.on_click_bt_finish)
        self.init_widget()

    def init_widget(self):
        """
        Initialise le layout et insère le bouton terminé
        """
        hbox = QHBoxLayout()
        self.bt_finish.setFixedSize(self.BUTTON_WIDTH, button_size)
        self.bt_finish.setStyleSheet(button_stylesheet)
        hbox.addWidget(self.bt_finish)

        self.setLayout(hbox)

    def on_click_bt_finish(self):
        """
        Emet un signal lorsque l'on click sur le bouton terminé
        """
        self.FINISH_SIGNAL.emit()
