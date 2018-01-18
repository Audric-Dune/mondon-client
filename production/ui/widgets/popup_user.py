# !/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtCore import pyqtSignal, QSize, QMargins, Qt
from PyQt5.QtGui import QPainter, QPixmap
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QVBoxLayout, QPushButton, QLineEdit

from commun.constants.colors import color_bleu_gris
from commun.constants.param import USER
from commun.constants.stylesheets import red_title_label_stylesheet,\
    button_little_stylesheet,\
    button_little_red_stylesheet,\
    line_edit_stylesheet
from commun.ui.public.dropdown import Dropdown
from commun.utils.drawing import draw_rectangle

from production.stores.user_store import user_store


class PopupUser(QWidget):
    # Signal émit lorsque on sélectionne une réponse
    # Retourne la réponse de l'utilisateur
    POPUP_USER_SIGNAL = pyqtSignal(bool)
    # _____DEFINITION CONSTANTE CLASS_____
    HEIGHT_LINE_EDIT = 24
    HEIGHT_BT = 30
    WIDTH_LINE_EDIT = 200
    SIZE = QSize(HEIGHT_LINE_EDIT, HEIGHT_LINE_EDIT)
    MARGIN_VBOX_PRINCIPALE = QMargins(15, 15, 15, 15)

    def __init__(self, parent=None, on_close=None):
        super(PopupUser, self).__init__(parent=parent)
        self.on_close = on_close
        self.user_selected = None
        self.setWindowTitle("Gestion utilisateur")
        # _____INITIALISATION WIDGET_____
        self.vbox = QVBoxLayout(self)
        self.dropdown_user = self.create_dropdown_user()
        self.password = QLineEdit()
        self.label_invalid = QLabel("Mot de passe incorrect")
        self.label_no_user = QLabel("Aucun utilisateur sélectionné")
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
        hbox_user.addWidget(self.create_icone("commun/assets/images/user_icon.png"))
        hbox_user.addWidget(self.dropdown_user)
        self.vbox.addLayout(hbox_user)

        hbox_password = QHBoxLayout()
        hbox_password.addWidget(self.create_icone("commun/assets/images/password_icon.png"))
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

        hbox_no_user = QHBoxLayout()
        self.label_no_user.setStyleSheet(red_title_label_stylesheet)
        self.label_no_user.hide()
        self.label_no_user.setAlignment(Qt.AlignCenter)
        hbox_invalid.addWidget(self.label_no_user)
        self.vbox.addLayout(hbox_no_user)

        hbox_bt = QHBoxLayout()
        self.bt_valider.setStyleSheet(button_little_stylesheet)
        self.bt_valider.setFixedHeight(self.HEIGHT_BT)
        hbox_bt.addWidget(self.bt_valider)
        self.bt_annuler.setStyleSheet(button_little_red_stylesheet)
        self.bt_annuler.setFixedHeight(self.HEIGHT_BT)
        hbox_bt.addWidget(self.bt_annuler)
        self.vbox.addLayout(hbox_bt)

        self.setLayout(self.vbox)

    def create_dropdown_user(self):
        dropdown_user = Dropdown(index=None)
        dropdown_user.setFixedWidth(self.WIDTH_LINE_EDIT)
        for user in USER.items():
            dropdown_user.add_item(user[0])
        dropdown_user.set_placeholder("Utilisateur")
        dropdown_user.VALUE_SELECTED_SIGNAL.connect(self.on_select_user_changed)
        return dropdown_user

    def on_select_user_changed(self, user, index):
        self.user_selected = user
        self.update_widget()

    def update_widget(self):
        if self.user_selected == "Superviseur":
            self.password.setDisabled(False)
            self.password.setPlaceholderText("Mot de passe")
        elif self.user_selected == "Opérateur":
            self.password.setDisabled(True)
            self.password.setPlaceholderText("Aucun mot de pase")
        else:
            self.password.setDisabled(True)

    def create_icone(self, path_img):
        icone_container = QLabel()
        img = QPixmap(path_img)
        icone_container.setPixmap(img)
        icone_container.setFixedSize(self.SIZE)
        icone_container.setScaledContents(True)
        return icone_container

    def on_click_bt_valider(self):
        if not self.user_selected:
            self.label_no_user.show()
        else:
            self.label_no_user.hide()
            if USER[self.user_selected]:
                password = USER[self.user_selected]
                if password == self.password.text():
                    user_store.update_user_level(1)
                    self.on_close()
                else:
                    self.label_invalid.show()
                    self.password.clear()
            else:
                user_store.update_user_level(0)
                self.on_close()

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
