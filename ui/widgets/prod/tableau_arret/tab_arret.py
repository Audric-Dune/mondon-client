# !/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtCore import Qt, QMargins
from PyQt5.QtWidgets import QVBoxLayout, QScrollArea, QWidget

from constants.colors import color_bleu_gris
from constants.param import \
    DEBUT_PROD_MATIN, \
    FIN_PROD_SOIR, \
    FIN_PROD_SOIR_VENDREDI, \
    DEBUT_PROD_SOIR, \
    FIN_PROD_MATIN_VENDREDI
from constants.stylesheets import scroll_bar_stylesheet
from stores.data_store_manager import data_store_manager
from stores.settings_store import settings_store
from ui.utils.layout import clear_layout
from ui.utils.timestamp import (
    timestamp_at_day_ago,
    timestamp_at_time,
    timestamp_to_day
)
from ui.widgets.prod.tableau_arret.line_arret import LineArret
from ui.widgets.public.mondon_widget import MondonWidget


class TabArret(MondonWidget):
    # _____DEFINITION CONSTANTE CLASS_____
    NO_MARGIN = QMargins(0, 0, 0, 0)
    """
    Gère le tableau d'arret, récupère les données en fonction de son paramètre moment (matin ou soir)
    """
    def __init__(self, parent, moment):
        super(TabArret, self).__init__(parent=parent)
        self.set_background_color(color_bleu_gris)
        self.moment = moment
        self.day_ago = 0
        self.list_arret = []
        self.memory_number_arret = 0
        self.get_arret()
        self.scroll_layout = None
        self.scroll = QScrollArea()
        self.scroll.setStyleSheet(scroll_bar_stylesheet)
        self.init_widgets()
        self.update_widget()

    def on_settings_changed(self, prev_live, prev_day_ago, prev_zoom):
        self.day_ago = settings_store.day_ago
        self.get_arret()
        self.update_widget()

    def on_data_changed(self):
        self.get_arret()
        self.scroll.setFixedWidth(self.width()-25)
        self.update_widget()

    def init_widgets(self):
        """
        Initialise les widgets et met en place la scrollbar
        """
        list_box = QVBoxLayout()
        self.setLayout(list_box)

        list_box.addWidget(self.scroll)
        self.scroll.setWidgetResizable(True)
        scroll_content = QWidget(self.scroll)
        scroll_content.setStyleSheet("background-color:{};".format(color_bleu_gris.hex_string))
        self.scroll_layout = QVBoxLayout(scroll_content)
        self.scroll_layout.setAlignment(Qt.AlignTop)
        self.scroll_layout.setSpacing(0)
        scroll_content.setLayout(self.scroll_layout)
        self.scroll.setWidget(scroll_content)

    def update_widget(self):
        """
        S'occupe de vider le tableau existant et de le remplir avec les nouvelles données
        :return:
        """
        self.scroll_layout = clear_layout(self.scroll_layout)
        number = 1
        # Parcour la liste des arrets et crée une line pour chaque arret
        for arret in self.list_arret:
            line_arret = LineArret(parent=self, day_ago=self.day_ago, arret=arret, number=number)
            self.scroll_layout.addWidget(line_arret)
            number += 1
        if number == 1:
            line_arret = LineArret(parent=self, day_ago=self.day_ago, arret=None, number=number)
            self.scroll_layout.addWidget(line_arret)

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
