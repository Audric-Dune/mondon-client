# !/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import timedelta

from PyQt5.Qt import QMargins
from PyQt5.QtCore import Qt, QEvent
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel, QWidget

from constants.stylesheets import red_12_label_stylesheet,\
    green_14_label_stylesheet,\
    gray_12_label_stylesheet,\
    blue_12_label_stylesheet,\
    blue_14_label_stylesheet, \
    gray_14_label_stylesheet, \
    red_14_label_stylesheet
from ui.utils.timestamp import timestamp_to_hour_little
from ui.application import app


class LineArret(QWidget):
    # _____DEFINITION CONSTANTE CLASS_____
    PADDING_VBOX = 2
    PADDING_HBOX = 0
    PRIMARY_LINE_HEIGHT = 20
    SECONDARY_LINE_HEIGHT = 20
    WIDTH_LABEL_TYPE = 100
    CONTENT_MARGIN = QMargins(0, 5, 0, 5)
    LABEL_MARGIN = 5

    def __init__(self, day_ago, arret, number, parent):
        super(LineArret, self).__init__(parent=parent)
        self.init_widgets(arret, number)
        self.arret = arret
        self.day_ago = day_ago
        self.installEventFilter(self)

    def init_widgets(self, arret, number):
        vbox = QVBoxLayout()
        self.setLayout(vbox)
        vbox.setSpacing(self.PADDING_VBOX)
        vbox.setContentsMargins(self.CONTENT_MARGIN)
        if arret:
            primary_layout = self.create_primary_line(arret, number)
            secondary_layout = self.create_secondary_line(arret)
            vbox.addLayout(primary_layout)
            vbox.addLayout(secondary_layout)
        else:
            no_arret_label = QLabel('Aucun arrêt enregistré')
            no_arret_label.setStyleSheet(green_14_label_stylesheet)
            no_arret_label.setAlignment(Qt.AlignCenter)
            no_arret_label.setFixedHeight(self.PRIMARY_LINE_HEIGHT)
            vbox.addWidget(no_arret_label)

    def create_primary_line(self, arret, number):
        hbox = QHBoxLayout()
        hbox.setSpacing(self.PADDING_HBOX)
        number_label = QLabel("Arrêt n.{}".format(str(number)))
        number_label.setStyleSheet(green_14_label_stylesheet)
        number_label.setMargin(self.LABEL_MARGIN)
        hour_label = QLabel("Début à {}".format(timestamp_to_hour_little(arret.start)))
        hour_label.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        hour_label.setStyleSheet(green_14_label_stylesheet)
        duration_label = QLabel("Durée : {}".format(str(timedelta(seconds=round(arret.end - arret.start)))))
        duration_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        duration_label.setStyleSheet(green_14_label_stylesheet)
        hbox.addWidget(number_label)
        hbox.addWidget(hour_label)
        hbox.addWidget(duration_label)
        return hbox

    def create_secondary_line(self, arret):
        vbox = QVBoxLayout()
        hbox = QHBoxLayout()
        hbox.setSpacing(self.PADDING_HBOX)
        if not arret.raisons:
            no_raison_label = QLabel("Aucune raison sélectionnée")
            no_raison_label.setMargin(self.LABEL_MARGIN)
            no_raison_label.setStyleSheet(red_12_label_stylesheet)
            no_raison_label.setAlignment(Qt.AlignCenter)
            hbox.addWidget(no_raison_label)
            vbox.addLayout(hbox)
            return vbox
        first_raison = True
        for raison in arret.raisons:
            hbox_temp = QHBoxLayout()
            hbox_temp.setSpacing(self.PADDING_HBOX)
            type_label = QLabel(raison.type)
            type_label.setMargin(self.LABEL_MARGIN)
            type_label.setFixedWidth(self.WIDTH_LABEL_TYPE)
            raison_label = QLabel(raison.raison)
            # On met le label et la croix en couleur en fonction du type
            if raison.type == "Prévu":
                raison_label.setStyleSheet(blue_14_label_stylesheet if first_raison else blue_12_label_stylesheet)
                type_label.setStyleSheet(blue_14_label_stylesheet if first_raison else blue_12_label_stylesheet)
            elif raison.type == "Imprévu":
                raison_label.setStyleSheet(red_14_label_stylesheet if first_raison else red_12_label_stylesheet)
                type_label.setStyleSheet(red_14_label_stylesheet if first_raison else red_12_label_stylesheet)
            else:
                raison_label.setStyleSheet(gray_14_label_stylesheet if first_raison else gray_12_label_stylesheet)
                type_label.setStyleSheet(gray_14_label_stylesheet if first_raison else gray_12_label_stylesheet)
            hbox_temp.addWidget(type_label)
            hbox_temp.addWidget(raison_label)
            vbox.addLayout(hbox_temp)
            first_raison = False
        return vbox

    def eventFilter(self, object, event):
        """
        Gestion des évènements
        Fonction PyQt appelé a chaque évènement
        :param object: Paramètre obligatoire
        :param event: L'évenement
        :return: Bool
        """
        # S'occupe d'ouvrir une window de l'arret si on double click sur lui dans la liste d'arret
        if event.type() == QEvent.MouseButtonDblClick:
            if self.arret:
                app.create_arret_window(start_arret=self.arret.start, day_ago=self.day_ago)
                return True
        return False
