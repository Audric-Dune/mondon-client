# !/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QVBoxLayout, QPushButton, QLineEdit
from PyQt5.QtCore import pyqtSignal, QSize, QMargins, Qt
from PyQt5.QtGui import QPainter, QPixmap

from constants.colors import color_bleu_gris
from constants.param import password
from constants.stylesheets import green_title_label_stylesheet,\
    red_title_label_stylesheet,\
    button_little_stylesheet,\
    button_little_red_stylesheet,\
    line_edit_stylesheet
from stores.user_store import user_store

from ui.utils.drawing import draw_rectangle


class PopupUser(QWidget):
    # Signal émit lorsque on sélectionne une réponse
    # Retourne la réponse de l'utilisateur
    POPUP_USER_SIGNAL = pyqtSignal(bool)
    # _____DEFINITION CONSTANTE CLASS_____
    HEIGHT_LINE_EDIT = 30
    WIDTH_LINE_EDIT = 200
    SIZE = QSize(HEIGHT_LINE_EDIT, HEIGHT_LINE_EDIT)
    MARGIN_VBOX_PRINCIPALE = QMargins(15, 15, 15, 15)

    def __init__(self, parent=None, on_close=None):
        super(PopupUser, self).__init__(parent=parent)
        self.on_close = on_close
        self.setWindowTitle("Gestion utilisateur")
        # _____INITIALISATION WIDGET_____
        self.vbox = QVBoxLayout(self)
        self.label_user = QLabel()
        self.password = QLineEdit()
        self.label_invalid = QLabel("Mot de passe incorrect")
        self.bt_valider = QPushButton("Valider")
        self.bt_valider.clicked.connect(self.on_click_bt_valider)
        self.bt_annuler = QPushButton("Annuler")
        self.bt_annuler.clicked.connect(self.on_click_bt_annuler)
        self.init_widget()
        self.update_widget()
        self.show()
        self.setFixedSize(self.width(), self.height())

    def init_widget(self):
        self.vbox.setContentsMargins(self.MARGIN_VBOX_PRINCIPALE)
        self.vbox.setSpacing(10)

        hbox_user = QHBoxLayout()
        hbox_user.addWidget(self.create_icone("assets/images/user_icon.png"))
        self.label_user.setStyleSheet(green_title_label_stylesheet)
        hbox_user.addWidget(self.label_user)
        self.vbox.addLayout(hbox_user)

        hbox_password = QHBoxLayout()
        hbox_password.addWidget(self.create_icone("assets/images/password_icon.png"))
        self.password.setStyleSheet(line_edit_stylesheet)
        self.password.setPlaceholderText("Mot de passe")
        self.password.setEchoMode(QLineEdit.Password)
        self.password.setFixedSize(self.WIDTH_LINE_EDIT, self.HEIGHT_LINE_EDIT)
        hbox_password.addWidget(self.password)
        self.vbox.addLayout(hbox_password)

        hbox_invalid = QHBoxLayout()
        self.label_invalid.setStyleSheet(red_title_label_stylesheet)
        self.label_invalid.hide()
        self.label_invalid.setAlignment(Qt.AlignCenter)
        hbox_invalid.addWidget(self.label_invalid)
        self.vbox.addLayout(hbox_invalid)

        hbox_bt = QHBoxLayout()
        self.bt_valider.setStyleSheet(button_little_stylesheet)
        self.bt_valider.setFixedHeight(self.HEIGHT_LINE_EDIT)
        hbox_bt.addWidget(self.bt_valider)
        self.bt_annuler.setStyleSheet(button_little_red_stylesheet)
        self.bt_annuler.setFixedHeight(self.HEIGHT_LINE_EDIT)
        hbox_bt.addWidget(self.bt_annuler)
        self.vbox.addLayout(hbox_bt)

        self.setLayout(self.vbox)

    def update_widget(self):
        if user_store.user_level == 0:
            self.label_user.setText("Superviseur")
            self.password.setPlaceholderText("Mot de passe")
        else:
            self.label_user.setText("Opérateur")
            self.password.setDisabled(True)
            self.password.setPlaceholderText("Aucun mot de pase")

    def create_icone(self, path_img):
        icone_container = QLabel()
        img = QPixmap(path_img)
        icone_container.setPixmap(img)
        icone_container.setFixedSize(self.SIZE)
        icone_container.setScaledContents(True)
        return icone_container

    def on_click_bt_valider(self):
        password_value = self.password.text()
        if password_value == password:
            user_store.update_user_level(1)
            self.on_close()
        elif user_store.user_level == 1:
            user_store.update_user_level(0)
            self.on_close()
        else:
            self.label_invalid.show()
            self.password.clear()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.on_click_bt_valider()
        if event.key() == Qt.Key_Escape:
            self.on_click_bt_annuler()
        event.accept()

    def on_click_bt_annuler(self):
        self.on_close()

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

    def closeEvent(self, QCloseEvent):
        self.on_close()