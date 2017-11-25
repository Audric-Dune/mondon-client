# !/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout
from ui.widgets.arret_window.arret_window_title import ArretWindowTitle
from ui.widgets.arret_window.arret_window_select_raison import ArretWindowSelectRaison
from ui.widgets.arret_window.arret_window_select_type import ArretWindowSelectType
from ui.widgets.arret_window.arret_window_ajout_raison import ArretWindowAjoutRaison
from ui.widgets.arret_window.arret_window_list_raison import ArretWindowListRaison


class ArretWindow(QMainWindow):
    """
    Windown créer automatiquement lorsque la machine passe en arrêt
    Permet de configurer les raisons qui ont provoqué l'arrêt
    """
    def __init__(self, on_close, arret):
        super(ArretWindow, self).__init__(None)
        arret.ARRET_TYPE_CHANGED_SIGNAL.connect(self.update_widget_from_type)
        self.arret = arret
        self.on_close = on_close
        self.last_type_selected = None
        # _____INITIALISATION WIDGET_____
        self.central_widget = QWidget(self)
        self.vbox = QVBoxLayout(self.central_widget)
        self.arret_window_title = ArretWindowTitle(self.arret, parent=self.central_widget)
        self.arret_window_list_raison = ArretWindowListRaison(self.arret, parent=self.central_widget)
        self.arret_window_select_type = ArretWindowSelectType(self.arret, parent=self.central_widget)
        self.arret_window_select_raison = None
        self.arret_window_ajout_raison = None
        self.init_widget()

    def init_widget(self):
        """
        Ajout les widgets initiaux au layout
        """
        # On fixe la taille du bloc titre pour rendre le bloc selection type maitre
        self.arret_window_title.setFixedHeight(60)
        self.vbox.addWidget(self.arret_window_title)
        self.vbox.addWidget(self.arret_window_list_raison)
        self.vbox.addWidget(self.arret_window_select_type)
        # On ajoute le layout au widget central (permet de gérer les marges de la fenêtre
        self.central_widget.setLayout(self.vbox)
        self.setCentralWidget(self.central_widget)

    def update_widget_from_type(self):
        """
        Appel de la fonction à l'émission du signal ARRET_TYPE_CHANGED_SIGNAL
        S'occupe de gérer la création/suppression du bloc selection raison
        """
        # On regarde si le bloc selection raison existe
        if not self.arret_window_select_raison:
            # Si elle n'existe pas on la crée
            self.create_arret_window_select_raison()
            # On stocke le type d'arret en mémoire
            self.last_type_selected = self.arret.type_cache
        # Sinon on regarde si le type d'arret en mémoire correspond ou type d'arret selectionné
        elif self.arret.type_cache == self.last_type_selected:
            # Si oui, on supprime le bloc sélection raison
            self.remove_arret_window_select_raison()
            # On supprime le bloc validation, si il y en a une
            self.remove_arret_window_ajout_raison()
            # On met a jour la valeur type d'arret stocker en mémoire dans l'objet Arret
            self.arret.remove_type()
            # On supprime le type d'arret stocker en mémoire
            self.last_type_selected = None
        else:
            # Sinon, on supprime le bloc arret raison et on la recrée pour quelle s'initialise
            # avec le type d'arret sélectionné
            self.remove_arret_window_select_raison()
            self.create_arret_window_select_raison()
            # On supprime le bloc validation, si il y en a une
            self.remove_arret_window_ajout_raison()
            # On stocke le type d'arret en mémoire
            self.last_type_selected = self.arret.type_cache
        # Utilisation d'un QTimer pour redimensionner la window
        # (on attend que les fonctions ci-dessus soit réellement exécuté)
        QTimer.singleShot(0, self.resize_window)

    def update_widget_from_validation(self, validation):
        """
        Appel de la fonction à l'émission du signal VALIDATION_CONDITION
        S'occupe de gérer la création/suppression du bloc validation
        """
        # On regarde si on a émis un signal pour créé le bloc validation
        # On vérifie que le bloc validation n'existe pas
        # On vérifie si les conditions de validation sont réunis
        if validation and not self.arret_window_ajout_raison and self.arret_window_select_raison.validation_condition:
            self.create_arret_window_validation()
        # On regarde si on a émis un signal pour créé le bloc validation
        # On vérifie si le bloc validation existe
        # On vérifie si les conditions de validation sont réunis
        elif validation and self.arret_window_ajout_raison and self.arret_window_select_raison.validation_condition:
            # Dans ce cas on a rien à faire
            pass
        else:
            # Sinon on supprime le bloc validation
            self.remove_arret_window_ajout_raison()
        # Utilisation d'un QTimer pour redimensionner la window
        # (on attend que les fonctions ci-dessus soit réellement exécuté)
        QTimer.singleShot(0, self.resize_window)

    def update_widget_from_add_raison(self):
        """
        S'occupe d'appeler la fonction de l'object arret pour ajouter une raison en base de donnée
        Met a jour la fenetre
        """
        self.arret.add_raison_on_database()
        # Met a jour la liste des raisons
        self.arret_window_list_raison.update_widget()
        # Utilisation d'un QTimer pour redimensionner la window
        # (on attend que les fonctions ci-dessus soit réellement exécuté)
        QTimer.singleShot(0, self.resize_window)

    def create_arret_window_select_raison(self):
        """
        S'occupe de créé le bloc selection raison
        On connect le signal VALIDATION_CONDITION_SIGNAL à la fonction update_widget_from_validation
        On ajoute le bloc sélection raison au layout
        """
        self.arret_window_select_raison = ArretWindowSelectRaison(self.arret, parent=self.central_widget)
        self.arret_window_select_raison.VALIDATION_CONDITION_SIGNAL.connect(self.update_widget_from_validation)
        self.vbox.addWidget(self.arret_window_select_raison)

    def create_arret_window_validation(self):
        """
        S'occupe de créé le bloc validation
        On ajoute le bloc validation au layout
        """
        self.arret_window_ajout_raison = ArretWindowAjoutRaison()
        self.arret_window_ajout_raison.ADD_RAISON_SIGNAL.connect(self.update_widget_from_add_raison)
        self.vbox.addWidget(self.arret_window_ajout_raison)

    def remove_arret_window_select_raison(self):
        """
        S'occupe de supprimer le bloc selection raison
        On retire le bloc selection raison au layout
        On supprime l'object bloc raison
        On met a jour la valeur raison de l'arret stocker en mémoire dans l'objet Arret
        On initialise la variable qui stock le bloc selection raison
        """
        self.vbox.removeWidget(self.arret_window_select_raison)
        self.arret_window_select_raison.deleteLater()
        self.arret.remove_raison()
        self.arret_window_select_raison = None

    def remove_arret_window_ajout_raison(self):
        """
        S'occupe de supprimer le bloc selection validation
        On retire le bloc selection validation au layout
        On supprime l'object bloc validation
        On initialise la variable qui stock le bloc selection validation
        """
        # On vérifie si la window validation existe
        if self.arret_window_ajout_raison:
            self.vbox.removeWidget(self.arret_window_ajout_raison)
            self.arret_window_ajout_raison.deleteLater()
        self.arret_window_ajout_raison = None

    def resize_window(self):
        """
        S'occupe de redimmensionner la window arret après un ajout/suppression d'un bloc
        """
        self.setFixedSize(self.minimumSizeHint())

    def closeEvent(self, event):
        self.on_close(self.arret.start)
