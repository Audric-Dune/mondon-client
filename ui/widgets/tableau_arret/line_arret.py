# !/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import timedelta

from PyQt5.Qt import QMargins
from PyQt5.QtCore import Qt, QEvent
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel, QWidget

from constants.stylesheets import red_title_label_stylesheet,\
    green_title_label_stylesheet,\
    gray_title_label_stylesheet

from ui.utils.timestamp import timestamp_to_hour_little
from ui.utils.layout import clear_layout
from ui.application import app


class LineArret(QWidget):
    # _____DEFINITION CONSTANTE CLASS_____
    PADDING_VBOX = 2
    PADDING_HBOX = 0
    PRIMARY_LINE_HEIGHT = 30
    SECONDARY_LINE_HEIGHT = 25
    WIDTH_LABEL_TYPE = 80
    CONTENT_MARGIN = QMargins(0, 5, 0, 5)
    LABEL_MARGIN = 5

    def __init__(self, day_ago, arret, number, parent):
        super(LineArret, self).__init__(parent=parent)
        self.init_widgets(arret, number)
        self.arret = arret
        self.day_ago = day_ago
        self.installEventFilter(self)

    def init_widgets(self, arret, number):
        primary_layout = self.create_primary_line(arret, number)
        secondary_layout = self.create_secondary_line(arret)

        vbox = QVBoxLayout()
        vbox.setSpacing(self.PADDING_VBOX)
        vbox.setContentsMargins(self.CONTENT_MARGIN)
        vbox.addLayout(primary_layout)
        vbox.addLayout(secondary_layout)
        self.setLayout(vbox)

    def create_primary_line(self, arret, number):
        hbox = QHBoxLayout()
        hbox.setSpacing(self.PADDING_HBOX)
        number_label = QLabel("Arrêt n.{}".format(str(number)))
        number_label.setFixedHeight(self.PRIMARY_LINE_HEIGHT)
        number_label.setStyleSheet(green_title_label_stylesheet)
        number_label.setMargin(self.LABEL_MARGIN)
        hour_label = QLabel("Début à {}".format(timestamp_to_hour_little(arret.start)))
        hour_label.setStyleSheet(green_title_label_stylesheet)
        duration_label = QLabel("Durée : {}".format(str(timedelta(seconds=round(arret.end - arret.start)))))
        duration_label.setStyleSheet(green_title_label_stylesheet)
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
            no_raison_label.setStyleSheet(red_title_label_stylesheet)
            no_raison_label.setAlignment(Qt.AlignCenter)
            no_raison_label.setFixedHeight(self.SECONDARY_LINE_HEIGHT)
            hbox.addWidget(no_raison_label)
            vbox.addLayout(hbox)
            return vbox
        for raison in arret.raisons:
            hbox_temp = QHBoxLayout()
            hbox_temp.setSpacing(self.PADDING_HBOX)
            type_label = QLabel(raison.type)
            type_label.setMargin(self.LABEL_MARGIN)
            type_label.setFixedHeight(self.SECONDARY_LINE_HEIGHT)
            type_label.setFixedWidth(self.WIDTH_LABEL_TYPE)
            raison_label = QLabel(raison.raison)
            if raison.type == "Prévu":
                raison_label.setStyleSheet(gray_title_label_stylesheet)
                type_label.setStyleSheet(gray_title_label_stylesheet)
            else:
                raison_label.setStyleSheet(red_title_label_stylesheet)
                type_label.setStyleSheet(red_title_label_stylesheet)
            hbox_temp.addWidget(type_label)
            hbox_temp.addWidget(raison_label)
            vbox.addLayout(hbox_temp)
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
            app.create_arret_window(start_arret=self.arret.start, day_ago=self.day_ago)
            return True

        return False