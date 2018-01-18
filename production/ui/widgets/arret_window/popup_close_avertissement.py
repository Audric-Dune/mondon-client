# !/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtCore import pyqtSignal, QSize, QMargins
from PyQt5.QtGui import QPainter, QPixmap
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QVBoxLayout, QPushButton

from commun.constants.colors import color_bleu_gris
from commun.constants.stylesheets import white_label_stylesheet, button_little_stylesheet
from commun.utils.drawing import draw_rectangle


class PopupCloseAvertissement(QWidget):
    # Signal émit lorsque on sélectionne une réponse
    # Retourne la réponse de l'utilisateur
    POPUP_CLOSE_AVERTISSEMENT_SIGNAL = pyqtSignal(bool)
    # _____DEFINITION CONSTANTE CLASS_____
    SIZE = QSize(40, 40)
    WIDTH_BUTTON_OK = 60
    HEIGHT_BUTTON_OK = 24
    MARGIN_VBOX_PRINCIPALE = QMargins(15, 15, 15, 15)

    """
    Popup d'avertissement modification en cours
    """

    def __init__(self, onclose, parent=None):
        super(PopupCloseAvertissement, self).__init__(parent=parent)
        self.onclose = onclose
        self.setWindowTitle("Attention")
        # _____INITIALISATION WIDGET_____
        self.vbox = QVBoxLayout(self)
        self.init_widget()
        self.show()
        self.setFixedSize(self.width(), self.height())

    def init_widget(self):
        hbox = QHBoxLayout()
        hbox.addWidget(self.create_icone())
        hbox.addLayout(self.create_message())
        hbox.setSpacing(10)
        hbox.setContentsMargins(0, 0, 0, 0)
        self.vbox.addLayout(hbox)
        self.vbox.addLayout(self.create_button())
        self.vbox.setContentsMargins(self.MARGIN_VBOX_PRINCIPALE)
        self.vbox.setSpacing(10)
        self.setLayout(self.vbox)

    def create_button(self):
        hbox = QHBoxLayout()
        hbox.addStretch(1)
        # On crée un bouton OUI
        bt_oui = QPushButton("Oui")
        bt_oui.setStyleSheet(button_little_stylesheet)
        # On connecte le bouton
        bt_oui.clicked.connect(lambda: self.onclick_button(True))
        bt_oui.setFixedSize(self.WIDTH_BUTTON_OK, self.HEIGHT_BUTTON_OK)
        # On ajoute l'item au layout vertical
        hbox.addWidget(bt_oui)
        # On crée un bouton NON
        bt_non = QPushButton("Non")
        bt_non.setStyleSheet(button_little_stylesheet)
        # On connecte le bouton
        bt_non.clicked.connect(lambda: self.onclick_button(False))
        bt_non.setFixedSize(self.WIDTH_BUTTON_OK, self.HEIGHT_BUTTON_OK)
        # On ajoute l'item au layout vertical
        hbox.addWidget(bt_non)
        hbox.addStretch(1)
        hbox.setContentsMargins(0, 0, 0, 0)
        hbox.setSpacing(20)
        return hbox

    def create_icone(self):
        icone_container = QLabel()
        img = QPixmap("commun/assets/images/icone_information.png")
        icone_container.setPixmap(img)
        icone_container.setFixedSize(self.SIZE)
        icone_container.setScaledContents(True)
        return icone_container

    @staticmethod
    def create_message():
        vbox = QVBoxLayout()
        label1 = QLabel("Des modifications sont en cours. Si vous fermez la fenêtre elles ne seront pas enregistrées.")
        label1.setWordWrap(True)
        label1.setStyleSheet(white_label_stylesheet)
        vbox.addWidget(label1)
        label2 = QLabel("Etes-vous sûr de vouloir quitter la fenêtre ?")
        label2.setStyleSheet(white_label_stylesheet)
        vbox.addWidget(label2)
        vbox.setSpacing(0)
        vbox.setContentsMargins(0, 0, 0, 0)
        return vbox

    def onclick_button(self, bool):
        """
        On émet un signal pour donner la reponse de l'utilisateur
        :param text: Texte de l'item clické
        """
        self.POPUP_CLOSE_AVERTISSEMENT_SIGNAL.emit(bool)

    def draw_fond(self, p):
        """
        Dessine un rectangle de la taille du bloc
        :param p: parametre de dessin
        """
        draw_rectangle(p, 5, 5, self.width() - 10, self.height() - 10, color_bleu_gris)

    def paintEvent(self, event):
        p = QPainter()
        p.begin(self)
        self.draw(p)
        p.end()

    def draw(self, p):
        self.draw_fond(p)

    def closeEvent(self, event):
        self.onclose()
