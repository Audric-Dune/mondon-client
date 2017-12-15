# !/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import timedelta
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QVBoxLayout, QScrollArea, QWidget
from PyQt5.QtGui import QPainter, QFont, QBrush, QTextDocument, QPdfWriter
from PyQt5.QtPrintSupport import QPrinter, QPrintDialog
from PyQt5.QtCore import QSize, Qt, QPoint
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
from constants.param import VITESSE_LIMITE_ASSIMILATION_ARRET, VITESSE_MOYENNE_MAXI, DEBUT_PROD_MATIN, FIN_PROD_SOIR_VENDREDI, FIN_PROD_SOIR
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
    timestamp_to_day
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
    PAGE_W = 770
    PAGE_H = 1100
    DEC_X_CHART = 65
    DEC_Y_STAT_1 = 60
    DEC_Y_HIST = 120
    DEC_Y_CHART = 180
    DEC_Y_PERF = 420
    DEC_Y_STAT = 480
    CHART_H = 200
    CHART_W = 640
    TITRE_W = 700

    def __init__(self, parent=None):
        super(RapportMenu, self).__init__(parent=parent)
        self.background_color = color_bleu_gris
        self.bt_impression = PixmapButton(parent=self)
        self.vbox = QVBoxLayout()
        self.hbox = QHBoxLayout()
        self.scrool_bar = QScrollArea()
        self.rapport = self.create_rapport()
        self.init_button()
        self.init_widget()

    def init_widget(self):
        label = QLabel("RAPPORT_MENU")
        label.setStyleSheet(white_title_label_stylesheet)
        self.hbox.addWidget(label)
        self.hbox.addWidget(self.bt_impression)
        self.vbox.addLayout(self.hbox)

        self.scrool_bar.setWidget(self.rapport)
        self.scrool_bar.setStyleSheet(scroll_bar_stylesheet)
        self.vbox.addWidget(self.scrool_bar)

        self.setLayout(self.vbox)

    def init_button(self):
        # Bouton impression
        self.bt_impression.clicked.connect(self.impression)
        self.bt_impression.setStyleSheet(button_stylesheet)
        self.bt_impression.setFixedSize(self.PIXMAPBUTTON_SIZE)
        self.bt_impression.addImage("assets/images/impression.png")

    def impression(self):
        printer = QPrinter()
        printer.setOutputFileName("print.pdf")
        painter = QPainter()
        painter.begin(printer)
        self.drawing(painter)
        painter.end()
        self.pdf()

    @staticmethod
    def pdf():
        pdf = QPdfWriter()
        pdf = open('print.pdf', encoding='utf-8').read()  # ascii PDF here
        # print("open")
        # doc = QTextDocument(pdf)
        printer = QPrinter()
        dialog = QPrintDialog(printer)
        if dialog.exec_() == True:
            # doc.print_(printer)
            print("print")
    # def impression(self):
    #     printer = QPrinter(QPrinter.HighResolution)
    #     painter = QPainter()
    #     painter.begin(printer)
    #     # rectangle = painter.viewport()
    #     # size = self.rapport.size()
    #     # size.scale(rectangle.size(), Qt.KeepAspectRatio)
    #     # painter.setViewport(rectangle.x(), rectangle.y(), size.width(), size.height())
    #     self.rapport.render(painter)
    #     painter.end()

    # def impression(self):
    #     widget = self.rapport
    #     painter = QPainter(QPrinter())
    #     rectangle = painter.viewport()
    #     size = widget.size()
    #     size.scale(rectangle.size(), Qt.KeepAspectRatio)
    #     painter.setViewport(rectangle.x(), rectangle.y(), size.width(), size.height())
    #     widget.render(painter)

    # def impression(self):
    #     printer = QPrinter()
    #     dialog = QPrintDialog(printer)
    #     dialog.setModal(True)
    #     dialog.setWindowTitle("Print Document")
    #     if dialog.exec_() == True:
    #         self.rapport.print_(printer)

    def create_rapport(self):
        vbox = QVBoxLayout()

        self.chart = Chart(parent=self)
        self.chart.setFixedHeight(300)
        self.chart.setFixedWidth(750)
        vbox.addWidget(self.chart)

        stat_menu = StatTitre(parent=self, note=False)
        vbox.addWidget(stat_menu)

        tab_arret_menu = TabArretMenu(parent=self, scrollbar=False)
        vbox.addWidget(tab_arret_menu)

        rapport = QWidget()
        rapport.setLayout(vbox)

        return rapport

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
            print(len(new_data))
            return new_data

        speeds = get_speed()
        i = 0
        for speed in speeds:
            color = color_vert if speed > VITESSE_LIMITE_ASSIMILATION_ARRET else color_rouge
            draw_rectangle(p, self.DEC_X_CHART + i, self.CHART_H - speed + self.DEC_Y_CHART, 1, speed + 1, color)
            i += 1

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
        draw_rectangle(p, 420, 10, 350, 1, color_bleu_dune)
        draw_rectangle(p, 0, 0, 1, self.PAGE_H, color_bleu_dune)
        draw_rectangle(p, 0, self.PAGE_H, self.PAGE_W, 1, color_bleu_dune)
        draw_rectangle(p, self.PAGE_W, 10, 1, 1091, color_bleu_dune)

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
        draw_text(p, self.PAGE_W - 200 - 10, self.DEC_Y_STAT_1, 200, 40, color_rouge, "D", 16, text, bold=True)
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
        draw_text(p, (self.PAGE_W - self.TITRE_W) / 2 + 10, self.DEC_Y_HIST, 400, 40, color_jaune_dune, "G", 16, "Historique des vitesse")

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
        DEC_X = (self.PAGE_W - self.TITRE_W) / 2
        i = 0
        while i < 3:
            if i == 0:
                text = "Equipe du matin"
                percent = percent_matin
            elif i == 1:
                text = "Equipe du soir"
                percent = percent_soir
            else:
                text = "Equipes cumulées"
                percent = percent_total

            draw_text(p, DEC_X + 10, self.DEC_Y_STAT, (self.TITRE_W - 40) / 3, 20, color_noir, "G", 14, text)
            draw_rectangle(p, DEC_X, self.DEC_Y_STAT + 22, (self.TITRE_W - 40) / 3, 1, color_bleu_dune)

            if percent < 25:
                color = color_rouge
            elif percent < 50:
                color = color_orange
            else:
                color = color_vert
            draw_rectangle(p, DEC_X + 10, self.DEC_Y_STAT + 35, percent / 100 * ((self.TITRE_W - 40) / 3 - 20), 30, color)

            draw_rectangle(p, DEC_X + 10, self.DEC_Y_STAT + 35, (self.TITRE_W - 40) / 3 - 20 + 1, 1, color_noir)
            draw_rectangle(p, DEC_X + 10, self.DEC_Y_STAT + 35, 1, 30, color_noir)
            draw_rectangle(p, DEC_X + 10 + (self.TITRE_W - 40) / 3 - 20, self.DEC_Y_STAT + 35 + 1, 1, 30, color_noir)
            draw_rectangle(p, DEC_X + 10, self.DEC_Y_STAT + 35 + 30, (self.TITRE_W - 40) / 3 - 20, 1, color_noir)
            DEC_X += (self.TITRE_W - 40) / 3 + 20
            i += 1

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

