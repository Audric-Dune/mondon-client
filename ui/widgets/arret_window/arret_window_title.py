# !/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import timedelta

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QLabel, QHBoxLayout

from constants.colors import color_bleu_gris
from constants.stylesheets import white_20_label_stylesheet, white_24_label_stylesheet
from ui.utils.drawing import draw_rectangle
from ui.utils.timestamp import timestamp_to_hour_little, timestamp_to_date_little
from ui.widgets.public.mondon_widget import MondonWidget


class ArretWindowTitle(MondonWidget):
    """
    Bloc titre de la window arret
    Affiche le temps de l'arret, l'heure de début et le jour
    """
    def __init__(self, arret, parent):
        super(ArretWindowTitle, self).__init__(parent=parent)
        self.arret = arret
        # _____INITIALISATION WIDGET_____
        self.label_date = QLabel()
        self.label_hour = QLabel()
        self.label_duration = QLabel()
        self.update_widget()
        self.init_widget()

    def init_widget(self):
        """
        Initialise le layout et insère les labels date du jour, durée d'arret et heure de début
        """
        hbox = QHBoxLayout()
        self.label_date.setStyleSheet(white_20_label_stylesheet)
        self.label_date.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        hbox.addWidget(self.label_date)
        self.label_duration.setStyleSheet(white_24_label_stylesheet)
        self.label_duration.setAlignment(Qt.AlignCenter)
        hbox.addWidget(self.label_duration)
        self.label_hour.setStyleSheet(white_20_label_stylesheet)
        self.label_hour.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        hbox.addWidget(self.label_hour)
        self.setLayout(hbox)

    def update_widget(self):
        """
        Met a jour les textes des labels date du jour, durée d'arret et heure de début
        """
        self.label_date.setText(str(timestamp_to_date_little(self.arret.start)))
        self.label_hour.setText(str(timestamp_to_hour_little(self.arret.start)))
        self.label_duration.setText(str(timedelta(seconds=round(self.arret.end - self.arret.start))))

    def on_data_changed(self):
        """
        Fonction héritée de mondon_widget
        Est appelé automatiquement après modification des data
        """
        self.update_widget()

    def paintEvent(self, event):
        p = QPainter()
        p.begin(self)
        self.draw(p)
        p.end()

    def draw_fond(self, p):
        """
        Dessine un rectangle de la taille du bloc
        :param p: parametre de dessin
        """
        draw_rectangle(p, 0, 0, self.width(), self.height(), color_bleu_gris)

    def draw(self, p):
        self.draw_fond(p)
