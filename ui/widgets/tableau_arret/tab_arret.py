# !/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import timedelta

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel, QGridLayout

from constants.colors import color_bleu_gris
from constants.dimensions import width_col_num, width_col_hour, width_col_time, width_col_type, width_col_raison
from constants.param import \
    DEBUT_PROD_MATIN, \
    FIN_PROD_SOIR, \
    FIN_PROD_SOIR_VENDREDI, \
    DEBUT_PROD_SOIR, \
    FIN_PROD_MATIN_VENDREDI
from constants.stylesheets import orange_label_stylesheet, red_label_stylesheet, white_label_stylesheet
from stores.data_store_manager import data_store_manager
from stores.settings_store import settings_store
from ui.utils.drawing import draw_rectangle
from ui.utils.timestamp import (
    timestamp_at_day_ago,
    timestamp_at_time,
    timestamp_to_day,
    timestamp_to_hour_little,
)
from ui.widgets.public.mondon_widget import MondonWidget


class TabArret(MondonWidget):
    def __init__(self, parent, moment):
        super(TabArret, self).__init__(parent=parent)
        self.moment = moment
        self.day_ago = 0
        self.list_arret = []
        self.labels_hours = []
        self.labels_time = []
        self.labels_type = []
        self.labels_raison = []
        self.init_widgets()
        self.get_arret()

    def on_settings_changed(self, prev_live, prev_day_ago, prev_zoom):
        self.day_ago = settings_store.day_ago
        self.get_arret()
        self.update_label()
        self.update()

    def on_data_changed(self):
        self.get_arret()
        self.update_label()

    def create_grid(self):
        grid = QGridLayout()
        grid.setSpacing(0)
        for line in range(15):
            index = line
            label_index = QLabel(str(index + 1))
            label_index.setFixedWidth(width_col_num)
            label_index.setAlignment(Qt.AlignCenter)
            label_index.setStyleSheet(white_label_stylesheet)
            grid.addWidget(label_index, line, 0)
            self.labels_hours.append(QLabel())
            self.labels_hours[index].setAlignment(Qt.AlignCenter)
            self.labels_hours[index].setFixedWidth(width_col_hour)
            self.labels_hours[index].setStyleSheet(white_label_stylesheet)
            grid.addWidget(self.labels_hours[index], line, 1)
            self.labels_time.append(QLabel())
            self.labels_time[index].setAlignment(Qt.AlignCenter)
            self.labels_time[index].setFixedWidth(width_col_time)
            self.labels_time[index].setStyleSheet(white_label_stylesheet)
            grid.addWidget(self.labels_time[index], line, 2)
            self.labels_type.append(QLabel())
            self.labels_type[index].setAlignment(Qt.AlignCenter)
            self.labels_type[index].setFixedWidth(width_col_type)
            self.labels_type[index].setStyleSheet(white_label_stylesheet)
            grid.addWidget(self.labels_type[index], line, 3)
            self.labels_raison.append(QLabel())
            self.labels_raison[index].setAlignment(Qt.AlignLeft)
            self.labels_raison[index].setFixedWidth(width_col_raison)
            self.labels_raison[index].setStyleSheet(white_label_stylesheet)
            grid.addWidget(self.labels_raison[index], line, 4)
        return grid

    @staticmethod
    def create_grid_title():
        grid = QGridLayout()
        grid.setSpacing(0)
        label_index = QLabel("Num")
        label_index.setFixedWidth(width_col_num)
        label_index.setAlignment(Qt.AlignCenter)
        label_index.setStyleSheet(white_label_stylesheet)
        grid.addWidget(label_index, 0, 0)
        label_hours = QLabel("Heure")
        label_hours.setAlignment(Qt.AlignCenter)
        label_hours.setFixedWidth(width_col_hour)
        label_hours.setStyleSheet(white_label_stylesheet)
        grid.addWidget(label_hours, 0, 1)
        label_time = QLabel("Temps")
        label_time.setAlignment(Qt.AlignCenter)
        label_time.setFixedWidth(width_col_time)
        label_time.setStyleSheet(white_label_stylesheet)
        grid.addWidget(label_time, 0, 2)
        label_type = QLabel("Type")
        label_type.setAlignment(Qt.AlignCenter)
        label_type.setFixedWidth(width_col_type)
        label_type.setStyleSheet(white_label_stylesheet)
        grid.addWidget(label_type, 0, 3)
        label_raison = QLabel("Raison")
        label_raison.setAlignment(Qt.AlignCenter)
        label_raison.setFixedWidth(width_col_raison)
        label_raison.setStyleSheet(white_label_stylesheet)
        grid.addWidget(label_raison, 0, 4)
        return grid

    def init_widgets(self):
        hbox = QHBoxLayout()
        hbox.setContentsMargins(0, 0, 0, 0)
        hbox.addStretch()
        vbox = QVBoxLayout()
        vbox.setContentsMargins(0, 0, 0, 0)
        title = self.create_grid_title()
        grid = self.create_grid()
        vbox.addLayout(title)
        vbox.addLayout(grid)
        hbox.addLayout(vbox)
        hbox.addStretch()
        self.setLayout(hbox)

    def get_arret(self):
        """
        S'occupe de créer une liste d'models Arret pour le moment de la journée courante
        :return:
        """
        # Récupere le store courant
        store = data_store_manager.get_current_store()
        # Stock la liste des arrets trier par ordre croissant (par rapport au start)
        arrets = store.arrets
        # Récupere le dictionnaire des arrets
        dic_arret = store.dic_arret
        # Récupere le timestamp du jours actuel
        ts = timestamp_at_day_ago(self.day_ago)

        # Check si on est un vendredi
        # Dans ce cas les équipes travail 7h (6h-13h,13h-21h)
        vendredi = timestamp_to_day(ts) == "vendredi"
        start = DEBUT_PROD_MATIN
        mid = FIN_PROD_MATIN_VENDREDI if vendredi else DEBUT_PROD_SOIR
        end = FIN_PROD_SOIR_VENDREDI if vendredi else FIN_PROD_SOIR

        # Definit les bornes de sélection des arret en fonction du moment de la journée (matin ou soir)
        if self.moment == "matin":
            end = mid
        if self.moment == "soir":
            start = mid
        start_ts = timestamp_at_time(ts, hours=start)
        end_ts = timestamp_at_time(ts, hours=end)

        # Initialise la liste d'arret
        list_arret = []
        # Parcours la liste des arret
        for arret in arrets:
            start_arret = arret[0]
            end_arret = arret[1]
            # Si le debut de l'arret est compris dans les bornes de selection
            if end_ts >= start_arret >= start_ts:
                # Et si la fin de l'arret est bien definit
                if end_arret > 0:
                    # On ajoute a la liste des arrets l'models Arret stocké dans le dictionnaire
                    list_arret.append(dic_arret[start_arret])
            # Sinon on continue la boucle
            else:
                continue
        self.list_arret = list_arret

    def update_label(self):
        # Boucle sur les 15 valeur possibles
        for i in range(15):
            # Si on a des données à afficher, on affiche l'heure et le temps
            if i < len(self.list_arret):
                current_arret = self.list_arret[i]
                hour = current_arret.start
                temps = current_arret.end - current_arret.start
                # Mis à jour des textes
                self.labels_hours[i].setText(timestamp_to_hour_little(hour))
                self.labels_time[i].setText(str(timedelta(seconds=round(temps))))
                # Mis à jour des couleurs
                if temps <= 15 * 60:  # Moins de 15 minutes
                    self.labels_time[i].setStyleSheet(white_label_stylesheet)
                elif temps <= 30 * 60:  # Entre 15 minutes et 30 minutes
                    self.labels_time[i].setStyleSheet(orange_label_stylesheet)
                else:  # Plus de 30 minutes
                    self.labels_time[i].setStyleSheet(red_label_stylesheet)
            else:
                # Reset les labels avec un string vide
                self.labels_hours[i].setText("")
                self.labels_time[i].setText("")
                self.labels_type[i].setText("")
                self.labels_raison[i].setText("")
                # Reset la couleur en blanc
                self.labels_time[i].setStyleSheet(white_label_stylesheet)

    def paintEvent(self, event):
        p = QPainter()
        p.begin(self)
        self.draw(p)
        p.end()

    def draw_fond(self, p):
        draw_rectangle(p, 0, 0, self.width(), self.height(), color_bleu_gris)

    def draw(self, p):
        self.draw_fond(p)
