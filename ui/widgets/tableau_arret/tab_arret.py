# !/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import timedelta

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel, QScrollArea, QWidget, QPushButton

from constants.colors import color_bleu_gris, color_rouge
from constants.dimensions import width_col_num, width_col_hour, width_col_time, width_col_type, width_col_raison
from constants.param import \
    DEBUT_PROD_MATIN, \
    FIN_PROD_SOIR, \
    FIN_PROD_SOIR_VENDREDI, \
    DEBUT_PROD_SOIR, \
    FIN_PROD_MATIN_VENDREDI
from constants.stylesheets import scroll_bar_stylesheet
from stores.data_store_manager import data_store_manager
from stores.settings_store import settings_store
from ui.utils.drawing import draw_rectangle
from ui.utils.timestamp import (
    timestamp_at_day_ago,
    timestamp_at_time,
    timestamp_to_day,
    timestamp_to_hour_little,
    timestamp_to_hour
)
from ui.utils.layout import clear_layout
from ui.widgets.public.mondon_widget import MondonWidget


class TabArret(MondonWidget):
    def __init__(self, parent, moment):
        super(TabArret, self).__init__(parent=parent)
        self.moment = moment
        self.day_ago = 0
        self.list_arret = []
        self.get_arret()
        self.scroll_layout = None
        self.scroll = QScrollArea(self)
        self.scroll.setStyleSheet(scroll_bar_stylesheet)
        self.scroll.setContentsMargins(0, 0, 0, 0)
        self.scroll.setMaximumHeight(200)
        self.scroll.setMinimumHeight(100)
        self.init_widgets()

    def on_settings_changed(self, prev_live, prev_day_ago, prev_zoom):
        self.day_ago = settings_store.day_ago
        self.get_arret()
        self.update_widget()

    def on_data_changed(self):
        self.get_arret()
        self.scroll.setFixedWidth(self.width()-25)
        self.update_widget()

    def init_widgets(self):
        list_box = QVBoxLayout(self)
        self.setLayout(list_box)

        list_box.addWidget(self.scroll, alignment=Qt.AlignCenter)
        self.scroll.setWidgetResizable(True)
        scroll_content = QWidget(self.scroll)
        scroll_content.setStyleSheet("background-color:red;")

        self.scroll_layout = QVBoxLayout(scroll_content)
        self.scroll_layout.setAlignment(Qt.AlignTop)
        scroll_content.setLayout(self.scroll_layout)
        self.scroll.setWidget(scroll_content)

    def update_widget(self):
        self.scroll_layout = clear_layout(self.scroll_layout)
        number = 1
        for arret in self.list_arret:
            hbox = QHBoxLayout()
            number_label = QLabel(str(number))
            number_label.setStyleSheet("background-color:yellow;")
            hour_label = QLabel(timestamp_to_hour_little(arret.start))
            hour_label.setStyleSheet("background-color:orange;")
            duration_label = QLabel(str(timedelta(seconds=round(arret.end - arret.start))))
            duration_label.setStyleSheet("background-color:pink;")
            hbox.addWidget(number_label)
            hbox.addWidget(hour_label)
            hbox.addWidget(duration_label)
            if not arret.raisons:
                no_raison_label = QLabel("Aucune raison sélectionnée")
                no_raison_label.setStyleSheet("background-color:green;")
                hbox.addWidget(no_raison_label)
                self.scroll_layout.addLayout(hbox)
            else:
                for raison in arret.raisons:
                    type_label = QLabel(raison.type)
                    type_label.setStyleSheet("background-color:orange;")
                    raison_label = QLabel(raison.raison)
                    raison_label.setStyleSheet("background-color:yellow;")
                    hbox.addWidget(type_label)
                    hbox.addWidget(raison_label)
                    self.scroll_layout.addLayout(hbox)
            number += 1

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

    def paintEvent(self, event):
        p = QPainter()
        p.begin(self)
        self.draw(p)
        p.end()

    def draw_fond(self, p):
        draw_rectangle(p, 0, 0, self.width(), self.height(), color_bleu_gris)

    def draw(self, p):
        self.draw_fond(p)
