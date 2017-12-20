# !/usr/bin/env python
# -*- coding: utf-8 -*-
from datetime import timedelta
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QVBoxLayout, QScrollArea, QWidget, QFileDialog, QDialog
from PyQt5.QtGui import QPainter, QFont, QBrush, QTextDocument, QPdfWriter, QPixmap, QImage, QColor, QTransform
from PyQt5.QtPrintSupport import QPrinter, QPrintDialog
from PyQt5.QtCore import QSize, Qt, QPoint, QRectF, QRect
from constants.colors import (
    color_blanc,
    color_bleu_gris,
    color_gris_clair,
    color_gris_fonce,
    color_gris_moyen,
    color_noir,
    color_rouge,
    color_vert,
    color_bleu_dune,
    color_jaune_dune,
    color_orange,
)
from constants.dimensions import (
    chart_margin_bottom,
    chart_margin_left,
    chart_margin_right,
    chart_margin_top,
    chart_min_hour,
    chart_max_hour,
    width_grille,
)
from constants.param import VITESSE_LIMITE_ASSIMILATION_ARRET, VITESSE_MOYENNE_MAXI, DEBUT_PROD_MATIN, FIN_PROD_SOIR_VENDREDI, FIN_PROD_SOIR, FIN_PROD_MATIN, FIN_PROD_MATIN_VENDREDI
from stores.data_store_manager import data_store_manager
from stores.settings_store import settings_store
from ui.utils.data import affiche_entier
from ui.utils.drawing import draw_rectangle, draw_text
from ui.utils.timestamp import (
    hour_in_timestamp,
    timestamp_at_day_ago,
    timestamp_at_time,
    timestamp_au_debut_de_hour,
    timestamp_to_date_little,
    timestamp_to_day,
    timestamp_to_hour_little
)
from ui.widgets.public.mondon_widget import MondonWidget

from ui.utils.drawing import draw_rectangle, draw_text
from ui.utils.timestamp import timestamp_at_day_ago
from ui.widgets.prod.chart.chart import Chart
from ui.widgets.prod.chart_stat.stat_titre import StatTitre
from ui.widgets.prod.tableau_arret.tab_arret_menu import TabArretMenu

from constants.colors import color_bleu_gris
from constants.stylesheets import white_title_label_stylesheet, button_stylesheet, scroll_bar_stylesheet
from ui.widgets.public.mondon_widget import MondonWidget
from ui.widgets.public.pixmap_button import PixmapButton


class RapportMenu(MondonWidget):
    PIXMAPBUTTON_SIZE = QSize(40, 40)

    def __init__(self, parent=None):
        super(RapportMenu, self).__init__(parent=parent)
        self.background_color = color_bleu_gris
        self.bt_impression = PixmapButton(parent=self)
        self.bt_save = PixmapButton(parent=self)
        self.vbox = QVBoxLayout()
        self.hbox = QHBoxLayout()
        self.rapport = Rapport(parent=self)
        self.scrool_bar = QScrollArea()
        self.init_button()
        self.init_widget()

    def init_widget(self):
        label = QLabel("RAPPORT_MENU")
        label.setStyleSheet(white_title_label_stylesheet)
        self.hbox.addWidget(label)
        self.hbox.addWidget(self.bt_save)
        self.hbox.addWidget(self.bt_impression)
        self.vbox.addLayout(self.hbox)

        # self.scrool_bar.setWidget(self.rapport)
        self.scrool_bar.setStyleSheet(scroll_bar_stylesheet)
        self.vbox.addWidget(self.scrool_bar)

        self.setLayout(self.vbox)

    def init_button(self):
        # Bouton sauvegarder
        self.bt_save.clicked.connect(self.save_pdf)
        self.bt_save.setStyleSheet(button_stylesheet)
        self.bt_save.setFixedSize(self.PIXMAPBUTTON_SIZE)
        self.bt_save.setContentsMargins(8)
        self.bt_save.addImage("assets/images/save_as.png")
        # Bouton impression
        self.bt_impression.clicked.connect(self.impression)
        self.bt_impression.setStyleSheet(button_stylesheet)
        self.bt_impression.setFixedSize(self.PIXMAPBUTTON_SIZE)
        self.bt_impression.addImage("assets/images/impression.png")

    def save_pdf(self):
        printer = QPrinter()
        painter = QPainter()
        file = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        name_file = "{}/2017_02_12_rapport_production_bobine.pdf".format(file)
        printer.setOutputFileName(name_file)
        printer.setOutputFormat(QPrinter.PdfFormat)
        printer.setPageMargins(10, 10, 10, 10, QPrinter.Point)
        painter.begin(printer)
        self.rapport.drawing(painter)
        painter.end()
        self.affiche_pdf(name_file)

    def impression(self):
        printer = QPrinter()
        dialog = QPrintDialog(printer, self)
        if dialog.exec_() != QDialog.Accepted:
            return
        painter = QPainter()
        printer.setPageMargins(10, 10, 10, 10, QPrinter.Point)
        painter.begin(printer)
        self.rapport.drawing(painter)
        painter.end()

    @staticmethod
    def affiche_pdf(name_file):
        import os
        """affiche le pdf créé, dans le visualiseur pdf par défaut de l'OS"""
        if os.path.exists(name_file):
            try:
                # solution pour Windows
                os.startfile(name_file)
            except:
                pass


class Rapport(MondonWidget):
    PAGE_W = 770
    PAGE_H = 1100
    DEC_X_CHART = 65
    DEC_Y_STAT_1 = 60
    DEC_Y_HIST = 120
    DEC_Y_CHART = 180
    DEC_Y_PERF = 420
    DEC_Y_STAT = 480
    DEC_Y_ARRET = 650
    DEC_Y_LIST = 720
    CASTOR_H = 38
    CASTOR_W = 115
    DEC_Y_CASTOR = PAGE_H - CASTOR_H
    DEC_X_CASTOR = PAGE_W / 2 - CASTOR_W / 2
    CHART_H = 200
    CHART_W = 640
    TITRE_W = 700

    def __init__(self, parent=None, painter=None):
        super(Rapport, self).__init__(parent=parent)
        p = painter
        if p:
            self.drawing(p)

    def draw_background(self, p):
        draw_rectangle(p, self.DEC_X_CHART, self.DEC_Y_CHART, self.CHART_W, self.CHART_H, color_gris_clair)

    def draw_speed(self, p):

        def get_speed():
            speeds = data_store_manager.get_current_store().data
            i = 0
            current_sum = 0
            new_data = []
            for speed in speeds:
                if i < 90:
                    value = speed[1]
                    current_sum += value
                else:
                    i = 0
                    new_data.append(round(current_sum / 90))
                    current_sum = 0
                i += 1
            new_data.append(round(current_sum / 90))
            return new_data

        speeds = get_speed()
        i = 0
        for speed in speeds:
            speed = speed if speed < 190 else 190
            color = color_vert if speed > VITESSE_LIMITE_ASSIMILATION_ARRET else color_rouge
            draw_rectangle(p, self.DEC_X_CHART + i, self.CHART_H - speed + self.DEC_Y_CHART, 1, speed + 1, color)
            i += 1
        current_store = data_store_manager.get_current_store()
        vendredi = timestamp_to_day(timestamp_at_day_ago(current_store.day_ago)) == "vendredi"
        if vendredi:
            draw_rectangle(p, self.DEC_X_CHART + (40*14), self.DEC_Y_CHART, 40*2, self.CHART_H, color_gris_moyen)
            draw_text(p, self.DEC_X_CHART + (40*14), self.DEC_Y_CHART, 40*2, self.CHART_H, color_gris_fonce, align="C", font_size=10, text="Vendredi")

    def draw_border(self, p):
        draw_rectangle(p, self.DEC_X_CHART, self.DEC_Y_CHART, 1, self.CHART_H, color_bleu_gris)
        draw_rectangle(p, self.DEC_X_CHART, self.DEC_Y_CHART, self.CHART_W, 1, color_bleu_gris)
        draw_rectangle(p, self.DEC_X_CHART + self.CHART_W, self.DEC_Y_CHART, 1, self.CHART_H + 1, color_bleu_gris)
        draw_rectangle(p, self.DEC_X_CHART, self.DEC_Y_CHART + self.CHART_H, self.CHART_W, 1, color_bleu_gris)

    def draw_v_grid(self, p):
        i = 0
        hour = 6
        while i <= 32:
            dec_hour = 3 if i % 2 == 0 else 0
            color = color_gris_moyen if i % 2 == 0 else color_gris_clair
            draw_rectangle(p, self.DEC_X_CHART + (20 * i), self.DEC_Y_CHART, 1, self.CHART_H + 5 + dec_hour, color)
            if i % 2 == 0:
                draw_text(p,
                          x=self.DEC_X_CHART + (20 * i) - 25,
                          y=self.DEC_Y_CHART + self.CHART_H + 5,
                          width=50,
                          height=20,
                          color=color_noir,
                          align="C",
                          font_size=8,
                          text="{}:00".format(hour))
                hour += 1
            i += 1

    def draw_h_grid(self, p):
        i = 0
        speed = 0
        while i <= 4:
            speed = 180 if i == 4 else speed
            color = color_gris_clair if i < 4 else color_gris_moyen
            draw_rectangle(p,
                           self.DEC_X_CHART - 3,
                           self.CHART_H - speed + self.DEC_Y_CHART,
                           self.CHART_W + 3,
                           1,
                           color)
            draw_text(p,
                      x=self.DEC_X_CHART - 35,
                      y=self.CHART_H - speed + self.DEC_Y_CHART - 10,
                      width=30,
                      height=20,
                      color=color_noir,
                      align="D",
                      font_size=8,
                      text=str(speed))
            speed += 50
            i += 1

    def draw_global_border(self, p):
        draw_rectangle(p, 0, 0, 1, self.PAGE_H - self.CASTOR_H / 2, color_bleu_dune)
        draw_rectangle(p, 420, 10, 350, 1, color_bleu_dune)
        draw_rectangle(p, self.PAGE_W, 10, 1, 1091 - self.CASTOR_H / 2, color_bleu_dune)
        draw_rectangle(p, 0, self.PAGE_H - self.CASTOR_H / 2, self.PAGE_W / 2 - self.CASTOR_W / 2 - 20, 1, color_bleu_dune)
        draw_rectangle(p, self.PAGE_W / 2 + self.CASTOR_W / 2 + 20, self.PAGE_H - self.CASTOR_H / 2, self.PAGE_W / 2 - self.CASTOR_W / 2 - 20, 1, color_bleu_dune)

    def draw_titre_1(self, p):
        draw_rectangle(p, 0, 0, 400, 40, color_jaune_dune)
        draw_text(p, 0, 0, 400, 40, color_noir, "C", 16, "Rapport quotidient production bobine")

    def draw_stat_1(self, p):
        current_store = data_store_manager.get_current_store()
        draw_rectangle(p, 0, self.DEC_Y_STAT_1, self.PAGE_W, 1, color_bleu_dune)
        draw_rectangle(p, 0, self.DEC_Y_STAT_1 + 40, self.PAGE_W, 1, color_bleu_dune)
        date = timestamp_to_date_little(timestamp_at_day_ago(current_store.day_ago))
        draw_text(p, 10, self.DEC_Y_STAT_1, 200, 40, color_noir, "G", 16, date, bold=True)
        time_imprevu = current_store.imprevu_arret_time_matin + current_store.imprevu_arret_time_soir
        imprevu_time_str = str(timedelta(seconds=round(time_imprevu)))
        text = ("{time} d'arrêt imprévu".format(time=imprevu_time_str))
        color = color_rouge if time_imprevu > 0 else color_vert
        draw_text(p, self.PAGE_W - 300 - 10, self.DEC_Y_STAT_1, 300, 40, color, "D", 16, text, bold=True)
        vendredi = timestamp_to_day(timestamp_at_day_ago(current_store.day_ago)) == "vendredi"
        total_s = 3600 * (FIN_PROD_SOIR_VENDREDI - DEBUT_PROD_MATIN) if vendredi else 3600 * (FIN_PROD_SOIR - DEBUT_PROD_MATIN)
        maxi_metrage = VITESSE_MOYENNE_MAXI * total_s / 60
        metrage_total = current_store.metrage_matin + current_store.metrage_soir
        percent = round(metrage_total / maxi_metrage * 100, 2)
        if percent < 25:
            color = color_rouge
        elif percent < 50:
            color = color_orange
        else:
            color = color_vert
        draw_text(p, 200, self.DEC_Y_STAT_1, 200, 40, color, "G", 16, "{}%".format(percent), bold=True)
        draw_text(p, 300, self.DEC_Y_STAT_1, 200, 40, color_noir, "C", 16, "{}m".format(affiche_entier(metrage_total)), bold=True)

    def draw_tite_historique(self, p):
        draw_rectangle(p, (self.PAGE_W - self.TITRE_W) / 2, self.DEC_Y_HIST, self.TITRE_W, 40, color_bleu_dune)
        draw_text(p, (self.PAGE_W - self.TITRE_W) / 2 + 10, self.DEC_Y_HIST, 400, 40, color_jaune_dune, "G", 16, "Historique des vitesses")

    def draw_titre_performance(self, p):
        draw_rectangle(p, (self.PAGE_W - self.TITRE_W) / 2, self.DEC_Y_PERF, self.TITRE_W, 40, color_bleu_dune)
        draw_text(p, (self.PAGE_W - self.TITRE_W) / 2 + 10, self.DEC_Y_PERF, 400, 40, color_jaune_dune, "G", 16, "Performances de la journée")

    def draw_stat(self, p):
        current_store = data_store_manager.get_current_store()
        vendredi = timestamp_to_day(timestamp_at_day_ago(current_store.day_ago)) == "vendredi"
        total_s = 3600 * (FIN_PROD_SOIR_VENDREDI - DEBUT_PROD_MATIN) if vendredi else 3600 * (FIN_PROD_SOIR - DEBUT_PROD_MATIN)
        maxi_metrage_total = VITESSE_MOYENNE_MAXI * total_s / 60
        maxi_metrage_equipe = VITESSE_MOYENNE_MAXI * total_s / 120
        metrage_total = current_store.metrage_matin + current_store.metrage_soir
        metrage_matin = current_store.metrage_matin
        metrage_soir = current_store.metrage_soir
        percent_total = round(metrage_total / maxi_metrage_total * 100, 2)
        percent_matin = round(metrage_matin / maxi_metrage_equipe * 100, 2)
        percent_soir = round(metrage_soir / maxi_metrage_equipe * 100, 2)
        time_total_matin = current_store.arret_time_matin
        time_total_soir = current_store.arret_time_soir
        time_total_day = time_total_matin + time_total_soir
        time_imprevu_matin = current_store.imprevu_arret_time_matin
        time_imprevu_soir = current_store.imprevu_arret_time_soir
        time_imprevu_total = time_imprevu_matin + time_imprevu_soir
        time_prevu_matin = time_total_matin - time_imprevu_matin
        time_prevu_soir = time_total_soir - time_imprevu_soir
        time_prevu_total = time_prevu_matin + time_prevu_soir
        DEC_X = (self.PAGE_W - self.TITRE_W) / 2
        i = 0
        while i < 3:
            if i == 0:
                text = "Equipe du matin"
                percent = percent_matin
                metre = metrage_matin
                time_total = time_total_matin
                time_imprevu = time_imprevu_matin
                time_prevu = time_prevu_matin
            elif i == 1:
                text = "Equipe du soir"
                percent = percent_soir
                metre = metrage_soir
                time_total = time_total_soir
                time_imprevu = time_imprevu_soir
                time_prevu = time_prevu_soir
            else:
                text = "Equipes cumulées"
                percent = percent_total
                metre = metrage_total
                time_total = time_total_day
                time_imprevu = time_imprevu_total
                time_prevu = time_prevu_total
            # ____DRAW_TITRE___
            draw_text(p, DEC_X + 10, self.DEC_Y_STAT, (self.TITRE_W - 40) / 3, 20, color_noir, "G", 14, text)
            draw_rectangle(p, DEC_X, self.DEC_Y_STAT + 22, (self.TITRE_W - 40) / 3, 1, color_bleu_dune)
            # ____DRAW_BAR___
            if not percent:
                percent = 0
            if percent < 25:
                color = color_rouge
            elif percent < 50:
                color = color_orange
            else:
                color = color_vert
            draw_rectangle(p, DEC_X + 10, self.DEC_Y_STAT + 35, percent / 100 * ((self.TITRE_W - 40) / 3 - 20), 30, color)
            if percent > 50:
                draw_text(p, DEC_X + 10, self.DEC_Y_STAT + 35, percent / 100 * ((self.TITRE_W - 40) / 3 - 20) - 10, 30, color_blanc, "D", 12, "{}%".format(percent))
            else:
                draw_text(p, DEC_X + 20 + percent / 100 * ((self.TITRE_W - 40) / 3 - 20), self.DEC_Y_STAT + 35, 100, 30, color_noir, "G", 12, "{}%".format(percent))
            draw_rectangle(p, DEC_X + 10, self.DEC_Y_STAT + 35, (self.TITRE_W - 40) / 3 - 20 + 1, 1, color_noir)
            draw_rectangle(p, DEC_X + 10, self.DEC_Y_STAT + 35, 1, 30, color_noir)
            draw_rectangle(p, DEC_X + 10 + (self.TITRE_W - 40) / 3 - 20, self.DEC_Y_STAT + 35 + 1, 1, 30, color_noir)
            draw_rectangle(p, DEC_X + 10, self.DEC_Y_STAT + 35 + 30, (self.TITRE_W - 40) / 3 - 20, 1, color_noir)
            # ____DRAW_LABEL___
            draw_rectangle(p, DEC_X, self.DEC_Y_STAT + 35 + 35, 1, 80, color_gris_moyen)
            draw_text(p, DEC_X + 10, self.DEC_Y_STAT + 35 + 35, 250, 20, color_noir, "G", 12, "{}m".format(affiche_entier(metre)))
            draw_text(p, DEC_X + 10, self.DEC_Y_STAT + 35 + 55, 250, 20, color_noir, "G", 12, "{} d'arrêt cumulé".format(str(timedelta(seconds=round(time_total)))))
            draw_text(p, DEC_X + 10, self.DEC_Y_STAT + 35 + 75, 250, 20, color_noir, "G", 12, "{} d'arrêt prévu".format(str(timedelta(seconds=round(time_prevu)))))
            color = color_rouge if time_imprevu > 0 else color_vert
            draw_text(p, DEC_X + 10, self.DEC_Y_STAT + 35 + 95, 250, 20, color, "G", 12, "{} d'arrêt imprévu".format(str(timedelta(seconds=round(time_imprevu)))))
            DEC_X += (self.TITRE_W - 40) / 3 + 20
            i += 1

    def draw_titre_arret(self, p):
        draw_rectangle(p, (self.PAGE_W - self.TITRE_W) / 2, self.DEC_Y_ARRET, self.TITRE_W, 40, color_bleu_dune)
        draw_text(p, (self.PAGE_W - self.TITRE_W) / 2 + 10, self.DEC_Y_ARRET, 400, 40, color_jaune_dune, "G", 16,
                  "Détail des arrêts remarquables machines")
        draw_text(p, (self.PAGE_W - self.TITRE_W) / 2 + 10, self.DEC_Y_ARRET + 45, 600, 20, color_gris_fonce, "G", 12,
                  "Par remarquable on assimile les arrêts imprévus ou supérieurs à 1 heure", italic=True)

    def draw_list_arret(self, p, moment):
        current_store = data_store_manager.get_current_store()
        arrets = current_store.arrets
        vendredi = timestamp_to_day(timestamp_at_day_ago(current_store.day_ago)) == "vendredi"
        if moment == "matin":
            DEC_X = (self.PAGE_W - self.TITRE_W) / 2
            start_hour = DEBUT_PROD_MATIN
            end_hour = FIN_PROD_MATIN_VENDREDI if vendredi else FIN_PROD_MATIN
        else:
            DEC_X = (self.PAGE_W - self.TITRE_W) / 2 + 350
            start_hour = FIN_PROD_MATIN_VENDREDI if vendredi else FIN_PROD_MATIN
            end_hour = FIN_PROD_SOIR_VENDREDI if vendredi else FIN_PROD_SOIR
        start_ts = timestamp_at_time(timestamp_at_day_ago(current_store.day_ago), hours=start_hour)
        end_ts = timestamp_at_time(timestamp_at_day_ago(current_store.day_ago), hours=end_hour)
        DEC_Y = 0
        i = 0

        for arret in arrets:
            start_arret = arret[0]
            end_arret = arret[1]
            type = arret[2][0].type if arret[2] else "non renseigné"
            if (start_ts < arret[0] < end_ts and arret[1] - arret[0] > 3600) or (start_ts < arret[0] < end_ts and type == "Imprévu"):
                start = str(timestamp_to_hour_little(start_arret))
                duree = str(timedelta(seconds=round(end_arret - start_arret)))
                text_arret = "Arrêt {type} à {start}, durée {duree}".format(type=type, start=start, duree=duree)
                if type == "Imprévu" or type == "non renseigné":
                    color = color_rouge
                elif type == "Prévu":
                    color = color_bleu_dune
                else:
                    color = color_gris_fonce
                draw_text(p, DEC_X + 10, self.DEC_Y_LIST + DEC_Y, 330, 20, color, "G", 12, text_arret, bold=True)
                if type != "non renseigné":
                    draw_text(p, DEC_X + 10, self.DEC_Y_LIST + DEC_Y + 20, 330, 20, color_noir, "G", 12, arret[2][0].raison)
                i += 1
                DEC_Y += 50

    def draw_castor(self, p):
        pixmap = QPixmap("assets/images/logo_dune.png")
        p.setRenderHint(QPainter.SmoothPixmapTransform)
        p.drawPixmap(QRect(self.DEC_X_CASTOR, self.DEC_Y_CASTOR + 1, 115, 38), pixmap)

    def drawing(self, p):
        self.draw_global_border(p)
        self.draw_titre_1(p)
        self.draw_stat_1(p)
        self.draw_tite_historique(p)
        # ____DRAW_CHART___
        self.draw_h_grid(p)  # Grille horizontale & légende
        self.draw_v_grid(p)  # Grille verticale & légende
        self.draw_speed(p)  # Les vitesses
        self.draw_border(p)  # La bordure
        self.draw_titre_performance(p)
        self.draw_stat(p)
        self.draw_titre_arret(p)
        self.draw_list_arret(p, "matin")
        self.draw_list_arret(p, "soir")
        self.draw_castor(p)
