# !/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import timedelta

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLabel, QHBoxLayout, QVBoxLayout

from commun.constants.colors import color_bleu_dune, color_blanc
from commun.constants.param import DEBUT_PROD_MATIN,\
    FIN_PROD_SOIR_VENDREDI,\
    FIN_PROD_SOIR,\
    FIN_PROD_MATIN,\
    FIN_PROD_MATIN_VENDREDI
from commun.constants.stylesheets import yellow_20_label_stylesheet,\
    black_16_label_stylesheet,\
    red_16_bold_label_stylesheet,\
    red_12_bold_label_stylesheet,\
    green_16_bold_label_stylesheet,\
    orange_16_bold_label_stylesheet,\
    dune_title_stylesheet,\
    blue_12_bold_label_stylesheet,\
    gray_italic_stylesheet,\
    black_12_label_stylesheet
from commun.ui.public.mondon_widget import MondonWidget
from commun.utils.data import affiche_entier, get_ratio_prod
from commun.utils.layout import clear_layout
from commun.utils.timestamp import timestamp_at_day_ago
from commun.utils.timestamp import timestamp_at_time,\
    timestamp_to_date_little,\
    timestamp_to_day,\
    timestamp_to_hour_little

from production.stores.data_store_manager import data_store_manager
from production.ui.widgets.prod.chart_stat.stat_bar import StatBar
from production.ui.widgets.rapport.chart_rapport import ChartRapport


class Rapport(MondonWidget):
    PAGE_W = 770
    PAGE_H = 1100
    TITLE_H = 40

    def __init__(self, parent=None):
        super(Rapport, self).__init__(parent=parent)
        self.set_border(color_bleu_dune, 1)
        self.setFixedSize(self.PAGE_W, self.PAGE_H)
        self.vbox = QVBoxLayout()
        self.init_widget()

    def init_widget(self):
        clear_layout(self.vbox)
        self.vbox.setContentsMargins(0, 0, 0, 0)
        self.vbox.setSpacing(20)

        self.vbox.addLayout(self.create_master_title())
        self.vbox.addWidget(self.create_master_stat())
        self.vbox.addWidget(self.create_title("Historique des vitesses"))
        self.vbox.addWidget(self.create_chart(), alignment=Qt.AlignCenter)
        self.vbox.addWidget(self.create_title("Performance de la journée"))
        self.vbox.addLayout(self.create_stat())
        self.vbox.addWidget(self.create_title("Détail des arrêts remarquables machine"))
        self.vbox.setSpacing(10)
        self.vbox.addLayout(self.create_info_arret())
        self.vbox.addLayout(self.create_list_arret())
        self.setLayout(self.vbox)

    def create_master_title(self):
        hbox_master_title = QHBoxLayout()
        hbox_master_title.setSpacing(0)

        master_title = QLabel("Rapport quotidient production bobine")
        master_title.setFixedSize(400, self.TITLE_H)
        master_title.setStyleSheet(yellow_20_label_stylesheet)
        master_title.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        hbox_master_title.addWidget(master_title, alignment=Qt.AlignLeft)

        space = MondonWidget()
        space.set_background_color(color_blanc)
        space.setFixedSize(20, self.TITLE_H)
        hbox_master_title.addWidget(space, alignment=Qt.AlignLeft)

        hbox_master_title.addStretch(1)
        return hbox_master_title

    @staticmethod
    def create_master_stat():
        back_ground_master_stat = MondonWidget()
        back_ground_master_stat.set_background_color(color_blanc)
        back_ground_master_stat.set_border(color=color_bleu_dune, size=1)
        hbox_master_stat = QHBoxLayout(back_ground_master_stat)
        current_store = data_store_manager.get_current_store()

        date = timestamp_to_date_little(timestamp_at_day_ago(current_store.day_ago))
        label_date = QLabel(date)
        label_date.setStyleSheet(black_16_label_stylesheet)

        time_imprevu = current_store.imprevu_arret_time_matin + current_store.imprevu_arret_time_soir
        imprevu_time_str = str(timedelta(seconds=round(time_imprevu)))
        text_imprevu_time = ("{time} d'arrêt imprévu".format(time=imprevu_time_str))
        label_imprevu_time = QLabel(text_imprevu_time)
        imprevu_time_label_stylesheet = red_16_bold_label_stylesheet if time_imprevu > 0 \
            else green_16_bold_label_stylesheet
        label_imprevu_time.setStyleSheet(imprevu_time_label_stylesheet)

        metrage_total = current_store.metrage_matin + current_store.metrage_soir
        label_metrage_total = QLabel("{}m".format(affiche_entier(metrage_total)))
        label_metrage_total.setStyleSheet(black_16_label_stylesheet)
        percent = get_ratio_prod("total")

        label_percent = QLabel("{}%".format(percent))
        if percent < 25:
            percent_stylesheet = red_16_bold_label_stylesheet
        elif percent < 50:
            percent_stylesheet = orange_16_bold_label_stylesheet
        else:
            percent_stylesheet = green_16_bold_label_stylesheet
        label_percent.setStyleSheet(percent_stylesheet)

        hbox_master_stat.addWidget(label_date, alignment=Qt.AlignLeft)
        hbox_master_stat.addWidget(label_percent)
        hbox_master_stat.addWidget(label_metrage_total)
        hbox_master_stat.addWidget(label_imprevu_time, alignment=Qt.AlignRight)
        return back_ground_master_stat

    def create_title(self, text):
        back_ground_master_stat = MondonWidget()
        back_ground_master_stat.set_background_color(color_bleu_dune)
        back_ground_master_stat.setFixedHeight(self.TITLE_H)
        hbox = QHBoxLayout(back_ground_master_stat)
        title_label = QLabel(text)
        title_label.setStyleSheet(dune_title_stylesheet)
        hbox.addWidget(title_label)
        return back_ground_master_stat

    @staticmethod
    def create_chart():
        chart = ChartRapport()
        chart.setFixedSize(700, 220)
        return chart

    def create_stat(self):
        hbox = QHBoxLayout()
        hbox.setContentsMargins(20, 0, 20, 0)
        hbox.addLayout(self.create_stat_bloc(team="matin"))
        hbox.addLayout(self.create_stat_bloc(team="soir"))
        hbox.addLayout(self.create_stat_bloc(team="total"))
        return hbox

    @staticmethod
    def create_stat_bloc(team):
        vbox_bloc_stat = QVBoxLayout()
        vbox_bloc_stat.setSpacing(0)
        if team == "total":
            team_str = "Equipe cumulée"
        else:
            team_str = "Equipe du {}".format(team)
        vbox_bloc_stat.addWidget(StatBar(titre=team_str, moment=team, mode="rapport"))
        return vbox_bloc_stat

    @staticmethod
    def create_info_arret():
        hbox = QHBoxLayout()
        label_info = QLabel("Par remarquable on assimile les arrêts imprévus ou supérieurs à 30 minutes")
        label_info.setStyleSheet(gray_italic_stylesheet)
        hbox.addWidget(label_info)
        return hbox

    def create_list_arret(self):
        hbox = QHBoxLayout()
        hbox.addLayout(self.create_bloc_arret(moment="matin"))
        hbox.addLayout(self.create_bloc_arret(moment="soir"))
        return hbox

    @staticmethod
    def create_bloc_arret(moment):
        vbox = QVBoxLayout()
        current_store = data_store_manager.get_current_store()
        arrets = current_store.arrets
        vendredi = timestamp_to_day(timestamp_at_day_ago(current_store.day_ago)) == "vendredi"
        if moment == "matin":
            start_hour = DEBUT_PROD_MATIN
            end_hour = FIN_PROD_MATIN_VENDREDI if vendredi else FIN_PROD_MATIN
        else:
            start_hour = FIN_PROD_MATIN_VENDREDI if vendredi else FIN_PROD_MATIN
            end_hour = FIN_PROD_SOIR_VENDREDI if vendredi else FIN_PROD_SOIR
        start_ts = timestamp_at_time(timestamp_at_day_ago(current_store.day_ago), hours=start_hour)
        end_ts = timestamp_at_time(timestamp_at_day_ago(current_store.day_ago), hours=end_hour)
        # Trie les arrets par ordre chronologique
        arrets = sorted(arrets, key=lambda arret: arret[0])
        limit_imprevu = 0

        def count_valid_arret(arrets, limit_imprevu):
            count = 0
            for arret in arrets:
                start_arret = arret[0]
                end_arret = arret[1]
                type = arret[2][0].type if arret[2] else "non renseigné"
                if (start_ts <= start_arret <= end_ts and end_arret - start_arret >= 1800)\
                        or (start_ts <= start_arret <= end_ts and type == "Imprévu"
                            and end_arret - start_arret >= limit_imprevu):
                    count += 1
            return count > 10

        while count_valid_arret(arrets, limit_imprevu):
            limit_imprevu += 10

        for arret in arrets:
            container_arret = QVBoxLayout()
            container_arret.setSpacing(0)
            start_arret = arret[0]
            end_arret = arret[1]
            type = arret[2][0].type if arret[2] else "non renseigné"
            if (start_ts <= start_arret <= end_ts and end_arret - start_arret >= 1800) \
                    or (start_ts <= start_arret <= end_ts and type == "Imprévu"
                        and end_arret - start_arret >= limit_imprevu):
                start = str(timestamp_to_hour_little(start_arret))
                duree = str(timedelta(seconds=round(end_arret - start_arret)))
                text_arret = "Arrêt {type} à {start}, durée {duree}".format(type=type, start=start, duree=duree)
                if type == "Imprévu" or type == "non renseigné":
                    stylesheet = red_12_bold_label_stylesheet
                else:
                    stylesheet = blue_12_bold_label_stylesheet
                title_arret = QLabel(text_arret)
                title_arret.setStyleSheet(stylesheet)
                container_arret.addWidget(title_arret, alignment=Qt.AlignTop)

                def add_label_to_container(vbox, label):
                    label.setStyleSheet(black_12_label_stylesheet)
                    label.setWordWrap(True)
                    vbox.addWidget(label, alignment=Qt.AlignTop)
                    vbox.addLayout(container_arret)

                if arret[2]:
                    if type == "Imprévu":
                        for raison in arret[2]:
                            if raison.type == "Nettoyage" or raison.type == "Prévu":
                                continue
                            add_label_to_container(container_arret, QLabel(raison.raison))
                    else:
                        add_label_to_container(container_arret, QLabel(arret[2][0].raison))
                else:
                    add_label_to_container(container_arret, QLabel(""))
                vbox.addLayout(container_arret)
        vbox.addStretch(1)
        return vbox

    def on_settings_changed(self, prev_live, prev_day_ago, prev_zoom):
        self.init_widget()

    def on_data_changed(self):
        self.update()
