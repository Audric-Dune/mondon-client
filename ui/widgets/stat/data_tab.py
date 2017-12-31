# !/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt

from constants.colors import color_gris_clair, color_bleu_gris
from constants.stylesheets import green_20_label_stylesheet, white_label_stylesheet, white_title_label_stylesheet
from ui.widgets.public.mondon_widget import MondonWidget
from ui.utils.data import affiche_entier
from ui.widgets.prod.chart_stat.bar import Bar
from stores.stat_store import stat_store
from stores.settings_stat_store import settings_stat_store


class DataTab(MondonWidget):
    """
    Dessine le tableau de statistique
    """
    def __init__(self, parent=None):
        super(DataTab, self).__init__(parent=parent)
        self.background_color = color_gris_clair
        self.title_label = QLabel()
        self.vbox_master = QVBoxLayout()
        self.init_widget()
        self.update_widget()

    def on_settings_stat_changed(self):
        """
        Est appelé quand les settings changent
        Met à jour les widgets
        """
        self.update_widget()

    def update_widget(self):
        """
        Met à jour le titre quand les settings changent
        """
        text_title = "Statistique {stat} : {time_stat}".format(
            stat=settings_stat_store.data_type, time_stat=settings_stat_store.time_stat)
        self.title_label.setText(text_title)

    def init_widget(self):
        """
        Initialize les layouts
        """
        self.title_label.setStyleSheet(green_20_label_stylesheet)
        self.title_label.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        self.title_label.setFixedHeight(40)
        self.vbox_master.addWidget(self.title_label)
        self.vbox_master.setContentsMargins(0, 0, 0, 0)
        self.vbox_master.addLayout(self.create_stat_metrage())
        self.setLayout(self.vbox_master)

    def create_stat_metrage(self):
        """
        Crée les bloc de statistique pour les équipes mqtin, soir, total dans un layout
        :return: Le layout
        """
        hbox = QHBoxLayout()
        hbox.addWidget(BlocStatMetrage(parent=self, titre="Equipe matin", moment="matin"))
        hbox.addWidget(BlocStatMetrage(parent=self, titre="Equipe soir", moment="soir"))
        hbox.addWidget(BlocStatMetrage(parent=self, titre="Equipes cumulées", moment="total"))
        return hbox


class BlocStatMetrage(MondonWidget):
    """
    Dessine un bloc de statistique métrage
    """
    def __init__(self, parent=None, titre=None, moment=None):
        super(BlocStatMetrage, self).__init__(parent=parent)
        self.set_background_color(color_bleu_gris)
        self.titre = titre
        self.moment = moment
        self.vbox = QVBoxLayout()
        self.bar = Bar(parent=self, little=True)
        self.titre_label = QLabel(titre)
        self.total_label = QLabel()
        self.mean_label = QLabel()
        self.max_label = QLabel()
        self.init_widget()
        self.update_widget()

    def on_data_stat_changed(self):
        """
        Est appelé quand les data changent
        Met à jour les widgets
        """
        self.update_widget()

    def update_widget(self):
        """
        Met à jour les data des widgets quand les data changent
        """
        self.bar.set_percent(stat_store.stat[self.moment]["percent"])
        self.total_label.setText("{} m".format(affiche_entier(stat_store.stat[self.moment]["total"])))
        self.mean_label.setText("{} m/jour".format(affiche_entier(stat_store.stat[self.moment]["mean"])))
        self.max_label.setText("{} m".format(affiche_entier(stat_store.stat[self.moment]["max"])))

    def init_widget(self):
        """
        Positionne les layouts
        """
        self.vbox.addLayout(self.create_line_titre(self.titre_label))
        self.vbox.addLayout(self.create_line_bar(self.bar))
        self.vbox.addLayout(self.create_line_stat(titre="Métrage total", label=self.total_label))
        self.vbox.addLayout(self.create_line_stat(titre="Moyenne", label=self.mean_label))
        self.vbox.addLayout(self.create_line_stat(titre="Maximum", label=self.max_label))
        self.setLayout(self.vbox)

    @staticmethod
    def create_line_titre(label):
        """
        Crée un layout pour le titre du bloc
        :param label: Le label contenant le titre
        :return: Le layout
        """
        hbox = QHBoxLayout()
        label.setStyleSheet(white_title_label_stylesheet)
        label.setFixedHeight(30)
        label.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        hbox.addWidget(label)
        return hbox

    @staticmethod
    def create_line_bar(bar):
        """
        Crée un layout pour la bar de pourcentage
        :param bar: La bar de pourcentage
        :return: Le layout
        """
        hbox = QHBoxLayout()
        bar.setFixedHeight(30)
        hbox.addWidget(bar)
        return hbox

    @staticmethod
    def create_line_stat(titre, label):
        """
        Crée un layout pour une donnée
        :param titre: Le tritre de la connée
        :param label: Le label de la donnée
        :return: Le layout
        """
        hbox = QHBoxLayout()
        titre_label = QLabel(titre)
        titre_label.setStyleSheet(white_label_stylesheet)
        hbox.addWidget(titre_label, alignment=Qt.AlignLeft)
        label.setStyleSheet(white_label_stylesheet)
        hbox.addWidget(label)
        return hbox
