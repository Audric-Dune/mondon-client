# !/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QVBoxLayout, QPushButton
from PyQt5.QtCore import pyqtSignal, QSize, QMargins
from PyQt5.QtGui import QPainter, QIcon, QPixmap

from constants.colors import color_bleu_gris
from constants.stylesheets import white_label_stylesheet,\
    button_little_stylesheet

from ui.utils.drawing import draw_rectangle


class PopupCloseNoRaison(QWidget):
    # Signal émit lorsque on sélectionne une réponse
    # Retourne la réponse de l'utilisateur
    POPUP_CLOSE_NO_RAISON_SIGNAL = pyqtSignal(bool)
    # _____DEFINITION CONSTANTE CLASS_____
    SIZE = QSize(40, 40)
    WIDTH_BUTTON_OK = 60
    HEIGHT_BUTTON_OK = 24
    MARGIN_VBOX_PRINCIPALE = QMargins(15, 15, 15, 15)

    """
    Popup d'avertissement pas de raison sélectionnée
    """

    def __init__(self, onclose, parent=None):
        super(PopupCloseNoRaison, self).__init__(parent=parent)
        self.onclose = onclose
        self.setWindowTitle("Impossible de fermer la fenêtre")
        self.setWindowIcon(QIcon())
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
        # On crée un bouton OK
        bt_ok = QPushButton("OK")
        bt_ok.setStyleSheet(button_little_stylesheet)
        # On connecte le bouton
        bt_ok.clicked.connect(lambda: self.onclick_button(False))
        bt_ok.setFixedSize(self.WIDTH_BUTTON_OK, self.HEIGHT_BUTTON_OK)
        # On ajoute l'item au layout vertical
        hbox.addWidget(bt_ok)
        hbox.addStretch(1)
        hbox.setContentsMargins(0, 0, 0, 0)
        return hbox

    def create_icone(self):
        icone_container = QLabel()
        img = QPixmap("assets/images/icone_error.png")
        icone_container.setPixmap(img)
        icone_container.setFixedSize(self.SIZE)
        icone_container.setScaledContents(True)
        return icone_container

    @staticmethod
    def create_message():
        vbox = QVBoxLayout()
        label1 = QLabel("Aucune raison sélectionnée.")
        label1.setStyleSheet(white_label_stylesheet)
        vbox.addWidget(label1)
        label2 = QLabel("Veuillez en ajouter au moins une.")
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
        self.POPUP_CLOSE_NO_RAISON_SIGNAL.emit(bool)

    def draw_fond(self, p):
        """
        Dessine un rectangle de la taille du bloc
        :param p: parametre de dessin
        """
        draw_rectangle(p, 5, 5, self.width()-10, self.height()-10, color_bleu_gris)

    def paintEvent(self, event):
        p = QPainter()
        p.begin(self)
        self.draw(p)
        p.end()

    def draw(self, p):
        self.draw_fond(p)

    def closeEvent(self, event):
        self.onclose()
