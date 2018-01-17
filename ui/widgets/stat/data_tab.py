# !/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import timedelta
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt

from constants.colors import color_gris_clair, color_bleu_gris
from constants.stylesheets import green_maj_label_stylesheet, white_16_label_stylesheet, white_16_bold_label_stylesheet
from ui.widgets.public.mondon_widget import MondonWidget
from ui.utils.data import affiche_entier
from ui.widgets.prod.chart_stat.bar import Bar
from stores.stat_store import stat_store
from stores.settings_stat_store import settings_stat_store
from ui.utils.layout import clear_layout
from ui.utils.timestamp import format_timedelta


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

    def on_data_stat_changed(self):
        """
        Lorsque les données changent on clear le layout et on le recrée avec les nouvelle valeur
        """
        clear_layout(self.vbox_master)
        self.init_widget()

    def init_widget(self):
        """
        Initialize les layouts
        """
        self.vbox_master.setContentsMargins(0, 0, 0, 0)
        self.vbox_master.setSpacing(2)
        self.vbox_master.addWidget(LineTitle())
        if settings_stat_store.data_type == "métrage":
            self.vbox_master.addWidget(LineStat(team="matin"))
            self.vbox_master.addWidget(LineStat(team="soir"))
            self.vbox_master.addWidget(LineStat(team="total"))
        else:
            self.vbox_master.addWidget(LineStat(team="Prévu"))
            self.vbox_master.addWidget(LineStat(team="Imprévu"))
            self.vbox_master.addWidget(LineStat(team="total"))
        self.setLayout(self.vbox_master)


class LineTitle(MondonWidget):
    def __init__(self, parent=None):
        super(LineTitle, self).__init__(parent=parent)
        self.hbox = QHBoxLayout()
        self.setFixedHeight(40)
        self.create_line_tittle()

    def on_settings_stat_changed(self):
        self.create_line_tittle()

    def create_line_tittle(self):
        """
        Crée le layout des titres
        :return: Le layout
        """
        clear_layout(self.hbox)
        self.hbox.setContentsMargins(0, 0, 0, 0)
        self.hbox.setSpacing(0)
        texte = "Equipe" if settings_stat_store.data_type == "métrage" else "Type"
        self.hbox.addWidget(self.create_label_tittle(text=texte, align=Qt.AlignLeft | Qt.AlignVCenter))
        text_total = "Total semaine" if settings_stat_store.format == "week" else "Total mois"
        self.hbox.addWidget(self.create_label_tittle(text=text_total, align=Qt.AlignCenter | Qt.AlignVCenter))
        self.hbox.addWidget(self.create_label_tittle(text="Moyenne jour", align=Qt.AlignCenter | Qt.AlignVCenter))
        self.hbox.addWidget(self.create_label_tittle(text="Maximum", align=Qt.AlignCenter | Qt.AlignVCenter))
        texte = "Ratio capacité" if settings_stat_store.data_type == "métrage" else "Ratio temps d'arrêt"
        self.hbox.addWidget(self.create_label_tittle(text=texte, align=Qt.AlignRight | Qt.AlignVCenter))
        self.setLayout(self.hbox)

    @staticmethod
    def create_label_tittle(text, align):
        """
        Crée un label titre
        :param text: Le texte du label
        :param align: L'alignement du label
        :return: Le label
        """
        label = QLabel(text)
        label.setStyleSheet(green_maj_label_stylesheet)
        label.setAlignment(align)
        return label


class LineStat(MondonWidget):
    def __init__(self, team, parent=None):
        super(LineStat, self).__init__(parent=parent)
        self.set_background_color(color_bleu_gris)
        self.setFixedHeight(40)
        self.hbox = QHBoxLayout()
        self.create_line_stat(team)

    def on_settings_stat_changed(self):
        self.on_loading(self.hbox, size=20, set_text=False, gif_name="loader_blue_white")

    def create_line_stat(self, team):
        """
        Crée le layout des stats d'une équipe avec un background
        :param team: L'équipe
        :return: Le background qui contient le layout
        """
        self.hbox.setContentsMargins(0, 0, 5, 0)
        self.hbox.setSpacing(0)
        bold = team == "total"
        name = "cumulée" if team == "total" else team
        self.hbox.addWidget(self.create_label(text=name, align=Qt.AlignLeft | Qt.AlignVCenter, bold=bold))
        self.hbox.addWidget(self.create_label(text=self.format_data(stat_store.stat[team]["total"]),
                                              align=Qt.AlignCenter | Qt.AlignVCenter,
                                              bold=bold))
        self.hbox.addWidget(self.create_label(text=self.format_data(stat_store.stat[team]["mean"]),
                                              align=Qt.AlignCenter | Qt.AlignVCenter,
                                              bold=bold))
        self.hbox.addWidget(self.create_label(text=self.format_data(stat_store.stat[team]["max"]),
                                              align=Qt.AlignCenter | Qt.AlignVCenter,
                                              bold=bold))
        self.hbox.addLayout(self.create_bar(team=team))
        self.setLayout(self.hbox)

    def create_bar(self, team):
        """
        Crée une bar au format little pour affiché le ratio
        :param team: L'équipe associé à la bar
        :return: Le layout contenant la bar
        """
        content_bar_layout = QHBoxLayout()
        percent = stat_store.stat[team]["percent"]
        bar = Bar(parent=self, percent=percent,
                  display_max_value=settings_stat_store.data_type == "métrage",
                  parametric_color=settings_stat_store.data_type == "métrage")
        bar.setFixedHeight(30)
        content_bar_layout.addWidget(bar)
        return content_bar_layout

    @staticmethod
    def create_label(text, align, bold=False):
        """
        Crée un label standard (avec la possibilité de le mettre ne gras)
        :param text: Le texte du label
        :param align: L'alignement du label
        :param bold: True si texte en gras sinon False
        :return: Le label
        """
        label = QLabel(text.capitalize())
        if bold:
            label.setStyleSheet(white_16_bold_label_stylesheet)
        else:
            label.setStyleSheet(white_16_label_stylesheet)
        label.setAlignment(align)
        label.setFixedHeight(40)
        return label

    @staticmethod
    def format_data(data):
        return affiche_entier(data) if settings_stat_store.data_type == "métrage"\
            else format_timedelta(timedelta(seconds=round(data)))
