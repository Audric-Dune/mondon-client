# !/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QHBoxLayout, QLabel, QVBoxLayout, QScrollArea, QWidget
from PyQt5.QtGui import QPainter, QFont, QBrush
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
from constants.param import VITESSE_LIMITE_ASSIMILATION_ARRET
from stores.data_store_manager import data_store_manager
from stores.settings_store import settings_store
from ui.utils.drawing import draw_rectangle, draw_text
from ui.utils.timestamp import (
    hour_in_timestamp,
    timestamp_at_day_ago,
    timestamp_at_time,
    timestamp_au_debut_de_hour,
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
    DEC_X = 40
    DEC_Y = 50
    CHART_H = 200
    CHART_W = 480

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
        draw_rectangle(p, self.DEC_X, self.DEC_Y, self.CHART_W, self.CHART_H, color_gris_clair)

    def draw_speed(self, p):

        def get_speed():
            speeds = data_store_manager.get_current_store().data
            i = 0
            current_sum = 0
            data_120 = []
            for speed in speeds:
                if i < 120:
                    value = speed[1]
                    current_sum += value
                else:
                    i = 0
                    data_120.append(current_sum / 120)
                    current_sum = 0
                i += 1
            data_120.append(round(current_sum / 120))
            return data_120

        speeds = get_speed()
        i = 0
        for speed in speeds:
            color = color_vert if speed > VITESSE_LIMITE_ASSIMILATION_ARRET else color_rouge
            draw_rectangle(p, self.DEC_X + i, self.CHART_H - speed + self.DEC_Y, 1, speed + 1, color)
            i += 1

    def draw_border(self, p):
        draw_rectangle(p, self.DEC_X, self.DEC_Y, 1, self.CHART_H, color_bleu_gris)
        draw_rectangle(p, self.DEC_X, self.DEC_Y, self.CHART_W, 1, color_bleu_gris)
        draw_rectangle(p, self.DEC_X + self.CHART_W, self.DEC_Y, 1, self.CHART_H + 1, color_bleu_gris)
        draw_rectangle(p, self.DEC_X, self.DEC_Y + self.CHART_H, self.CHART_W, 1, color_bleu_gris)

    def draw_v_grid(self, p):
        i = 0
        hour = 6
        while i <= 32:
            dec_hour = 3 if i % 2 == 0 else 0
            color = color_gris_moyen if i % 2 == 0 else color_gris_clair
            draw_rectangle(p, self.DEC_X + (15 * i), self.DEC_Y, 1, self.CHART_H + 5 + dec_hour, color)
            if i % 2 == 0:
                draw_text(p,
                          x=self.DEC_X + (15 * i) - 25,
                          y=self.DEC_Y + self.CHART_H + 5,
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
                           self.DEC_X - 3,
                           self.CHART_H - speed + self.DEC_Y,
                           self.CHART_W + 3,
                           1,
                           color)
            draw_text(p,
                      x=self.DEC_X - 35,
                      y=self.CHART_H - speed + self.DEC_Y - 10,
                      width=30,
                      height=20,
                      color=color_noir,
                      align="D",
                      font_size=8,
                      text=str(speed))
            speed += 50
            i += 1

    def drawing(self, p):
        # self.draw_global_border(p)
        # ____DRAW_CHART___
        self.draw_v_grid(p)  # Grille verticale & légende
        self.draw_h_grid(p)  # Grille horizontale & légende
        self.draw_speed(p)  # Les vitesses
        self.draw_border(p)  # La bordure
