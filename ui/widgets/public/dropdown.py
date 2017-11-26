# !/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QVBoxLayout, QPushButton
from PyQt5.QtCore import QEvent, QPoint, pyqtSignal
from PyQt5.QtGui import QPainter, QIcon
from PyQt5.Qt import Qt

from constants.colors import color_vert_fonce, color_blanc
from constants.stylesheets import black_16_label_stylesheet,\
    white_16_label_stylesheet,\
    button_arrow_stylesheet,\
    button_dropdown_stylesheet

from ui.utils.drawing import draw_rectangle


class Dropdown(QWidget):
    # Signal émit lorsque l'on sélectionne un item dans la liste déroulante
    # Retourne le string de l'item
    VALUE_SELECTED_SIGNAL = pyqtSignal(str, int)

    """
    Object générique dropdown
    """
    def __init__(self, index, parent=None):
        super(Dropdown, self).__init__(parent=parent)
        self.index = index
        self.placeholder = None
        self.selected = None
        # _____INITIALISATION WIDGET_____
        self.bt_dropdown = QPushButton(self)
        self.bt_dropdown.setStyleSheet(button_dropdown_stylesheet)
        self.bt_dropdown.clicked.connect(self.display_popup)
        self.bt_arrow_dropdown = QPushButton(self)
        self.bt_arrow_dropdown.setStyleSheet(button_arrow_stylesheet)
        self.bt_arrow_dropdown.clicked.connect(self.display_popup)
        img = QIcon("assets/images/arrow_down_vert_fonce.png")
        self.bt_arrow_dropdown.setIcon(img)
        self.popup = DropdownPopup()
        self.popup.hide()
        self.popup.POPUP_HIDE.connect(self.display_popup)
        self.popup.ITEM_CLICKED.connect(self.update_value_selected)
        self.init_widget()

    def init_widget(self):
        """
        S'occupe d'initialiser les boutons de la dropdown
        La dropdown est composé d'un bouton où l'on écrit le choix de l'utilisateur
        (ou la valeur par défaut si pas de choix)
        Et d'un bouton qui contient la flèche vers le bas
        Les deux boutons on le même effet sur un click
        """
        # On crée un layout horizontal
        hbox = QHBoxLayout(self)
        # On set la dimension du 1er bouton
        self.bt_dropdown.setFixedSize(250, 24)
        # On ajoute le bouton au widget
        hbox.addWidget(self.bt_dropdown)
        # On set la dimension du 2e bouton
        self.bt_arrow_dropdown.setFixedSize(24, 24)
        # On ajoute le bouton au widget
        hbox.addWidget(self.bt_arrow_dropdown)
        # On supprime les marges interieur et exterieur du layout
        hbox.setContentsMargins(0, 0, 0, 0)
        hbox.setSpacing(0)
        self.setLayout(hbox)

    def update_widget(self, bool):
        """
        S'occupe d'activer ou désactiver la dropdown
        :param bool: True pour activer, False pour désactiver
        """
        # Si True
        if bool:
            # On active les boutons
            self.bt_dropdown.setDisabled(False)
            self.bt_arrow_dropdown.setDisabled(False)
        else:
            # Sinon on désactive les boutons
            self.bt_dropdown.setDisabled(True)
            self.bt_arrow_dropdown.setDisabled(True)
            # On reset la valeur de la dropdown
            self.set_placeholder()

    def add_item(self, item_label):
        """
        S'occupe d'ajouter un item a la liste sélectionnable
        :param item_label: Le texte a ajouter
        """
        self.popup.add_item(item_label)

    def update_value_selected(self, value):
        """
        Gère la sélection d'une valeur par l'utilisateur
        :param value: La valeur sélectionné
        """
        # On met a jour la valeur du bouton pour qu'elle affiche la valeur sélectionnée
        self.bt_dropdown.setText(value)
        # On stock l'information que la dropdown a une valeur sélectionnée
        self.selected = True
        # On émet un signal qui indique que l'utilisateur a sélectionné une valeur
        self.VALUE_SELECTED_SIGNAL.emit(value, self.index)

    def set_activated(self, bool):
        """
        Fonction transitoire pour mettre a jour la dropdown
        :param bool: True pour activer, False pour désactiver
        """
        self.update_widget(bool)

    def set_placeholder(self, placeholder=None):
        """
        Reset la valeur de la dropdown
        :param placeholder: La valeur intiale de la dropdown
        """
        # Si j'ai une nouvelle valeur initiale
        if placeholder:
            # On la stock dans les parametres de la dropdown
            self.placeholder = placeholder
        # On met a jour le text de la dropdown avec la valeur initiale stocké dans les paramètres
        self.bt_dropdown.setText(self.placeholder)

    def display_popup(self):
        """
        S'occupe de l'affichage ou non de la popup
        """
        # Si la popup est visible on la cache
        if not self.popup.isHidden():
            self.popup.hide()
        # Sinon on l'affiche
        else:
            # On récupère le point de départ de la popup
            # Il correspond au point en bas a gauche du bouton (position absolu)
            pos_popup = self.mapToGlobal(QPoint(0, self.height()))
            # On déplace la popup au point calulé
            self.popup.move(pos_popup)
            # On fixe la largeur de la popup = largeur de la dropdown
            self.popup.setFixedWidth(self.width())
            # On l'affiche
            self.popup.show()


class DropdownPopup(QWidget):
    # Signal émit lorsque la popup doit être caché
    POPUP_HIDE = pyqtSignal()
    # Signal émit lorsque on sélectionne un item de la popup
    # Retourne le string de l'item
    ITEM_CLICKED = pyqtSignal(str)

    """
    Popup de la dropdown
    """

    def __init__(self, parent=None):
        super(DropdownPopup, self).__init__(parent=parent)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Popup)
        # _____INITIALISATION WIDGET_____
        self.vbox = QVBoxLayout(self)

    def add_item(self, item_label):
        """
        S'occupe d'ajouter un item a la popup
        :param item_label: Le texte de l'item
        """
        # On crée un object itempopup
        item = PopupItem(item_label)
        # On connecte le signal émit par l'item lorsque l'on click dessus
        item.ITEM_CLICKED.connect(self.item_clicked)
        # On ajoute l'item au layout vertical
        self.vbox.addWidget(item)
        # On supprime les marges interieur et exterieur du layout
        self.vbox.setContentsMargins(0, 0, 0, 0)
        self.vbox.setSpacing(0)
        self.setLayout(self.vbox)

    def item_clicked(self, text):
        """
        On émet un signal pour dire que l'item a était choisit
        On émet un signal pour dire qu'il faut cacher la popup
        :param text: Texte de l'item clické
        """
        self.ITEM_CLICKED.emit(text)
        self.POPUP_HIDE.emit()


class PopupItem(QWidget):
    # Signal émit lorsque on sélectionne l'item
    # Retourne le string de l'item
    ITEM_CLICKED = pyqtSignal(str)

    """
    Item de la popup de la dropdown
    """

    def __init__(self, item_label, parent=None):
        super(PopupItem, self).__init__(parent=parent)
        self.hover = False
        self.installEventFilter(self)
        self.item_label = item_label
        # _____INITIALISATION WIDGET_____
        self.label = QLabel(item_label)
        self.label.setFixedHeight(30)
        self.label.setStyleSheet(black_16_label_stylesheet)
        self.init_label()

    def init_label(self):
        """
        Initialise le layout et ajoute le label
        """
        # On crée un layout horizontal
        hbox = QHBoxLayout(self)
        # On ajoute une marge de 5px a gauche
        hbox.setContentsMargins(5, 0, 0, 0)
        # On ajoute le label au layout
        hbox.addWidget(self.label)
        self.setLayout(hbox)

    def eventFilter(self, object, event):
        """
        Gestion des évènements
        Fonction PyQt appelé a chaque évènement
        :param object: Paramètre obligatoire
        :param event: L'évenement
        :return: Bool
        """
        # Si l'évenement est la rentré de la souris dans l'object
        if event.type() == QEvent.Enter:
            # On stocke l'info que la souris est dans l'object
            self.hover = True
            # On met en blanc le texte
            self.label.setStyleSheet(white_16_label_stylesheet)
            # On met a jour le dessin de l'item
            self.update()
            # On retourne TRUE pour que l'évènement soit pris en compte
            return True
        # Si l'évenement est la sortie de la souris de l'object
        if event.type() == QEvent.Leave:
            # On stocke l'info que la souris n'est pas dans l'object
            self.hover = False
            # On met en noir le texte
            self.label.setStyleSheet(black_16_label_stylesheet)
            # On met a jour le dessin de l'item
            self.update()
            # On retourne TRUE pour que l'évènement soit pris en compte
            return True
        # Si l'évenement est le click sur l'item
        if event.type() == QEvent.MouseButtonRelease:
            # On émet un signal qui indique qu'on a clické sur l'item
            self.ITEM_CLICKED.emit(self.item_label)
            # On retourne TRUE pour que l'évènement soit pris en compte
            return True
        return False

    def draw_fond(self, p):
        """
        Dessine un rectangle de la taille du bloc
        :param p: parametre de dessin
        """
        color = color_vert_fonce if self.hover else color_blanc
        draw_rectangle(p, 0, 0, self.width(), self.height(), color)

    def paintEvent(self, event):
        p = QPainter()
        p.begin(self)
        self.draw(p)
        p.end()

    def draw(self, p):
        self.draw_fond(p)
