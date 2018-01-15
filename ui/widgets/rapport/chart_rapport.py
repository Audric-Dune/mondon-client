# !/usr/bin/env python
# -*- coding: utf-8 -*-

from constants.colors import (
    color_gris_clair,
    color_gris_fonce,
    color_gris_moyen,
    color_noir,
    color_rouge,
    color_vert,
    color_bleu_gris,
)
from constants.param import VITESSE_LIMITE_ASSIMILATION_ARRET
from stores.data_store_manager import data_store_manager
from ui.widgets.public.mondon_widget import MondonWidget
from ui.utils.timestamp import timestamp_to_day
from ui.utils.drawing import draw_rectangle, draw_text
from ui.utils.timestamp import timestamp_at_day_ago


class ChartRapport(MondonWidget):

    def __init__(self, parent=None):
        super(ChartRapport, self).__init__(parent=parent)
        self.W_CHART = 640
        self.H_CHART = 200
        self.X_CHART = 0
        self.Y_CHART = 0

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
            draw_rectangle(p, self.X_CHART + i, self.H_CHART - speed + self.Y_CHART, 1, speed + 1, color)
            i += 1
        current_store = data_store_manager.get_current_store()
        vendredi = timestamp_to_day(timestamp_at_day_ago(current_store.day_ago)) == "vendredi"
        if vendredi:
            draw_rectangle(p, self.X_CHART + (40*14), self.Y_CHART, 40*2, self.H_CHART, color_gris_moyen)
            draw_text(p,
                      self.X_CHART + (40*14),
                      self.Y_CHART, 40*2,
                      self.H_CHART,
                      color_gris_fonce,
                      align="C",
                      font_size=10,
                      text="Vendredi")

    def draw_border(self, p):
        draw_rectangle(p, self.X_CHART, self.Y_CHART, 1, self.H_CHART, color_bleu_gris)
        draw_rectangle(p, self.X_CHART, self.Y_CHART, self.W_CHART, 1, color_bleu_gris)
        draw_rectangle(p, self.X_CHART + self.W_CHART, self.Y_CHART, 1, self.H_CHART + 1, color_bleu_gris)
        draw_rectangle(p, self.X_CHART, self.Y_CHART + self.H_CHART, self.W_CHART, 1, color_bleu_gris)

    def draw_v_grid(self, p):
        i = 0
        hour = 6
        while i <= 32:
            dec_hour = 3 if i % 2 == 0 else 0
            color = color_gris_moyen if i % 2 == 0 else color_gris_clair
            draw_rectangle(p, self.X_CHART + (20 * i), self.Y_CHART, 1, self.H_CHART + 5 + dec_hour, color)
            if i % 2 == 0:
                draw_text(p,
                          x=self.X_CHART + (20 * i) - 25,
                          y=self.Y_CHART + self.H_CHART + 5,
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
                           self.X_CHART - 3,
                           self.H_CHART - speed + self.Y_CHART,
                           self.W_CHART + 3,
                           1,
                           color)
            draw_text(p,
                      x=self.X_CHART - 35,
                      y=self.H_CHART - speed + self.Y_CHART - 10,
                      width=30,
                      height=20,
                      color=color_noir,
                      align="D",
                      font_size=8,
                      text=str(speed))
            speed += 50
            i += 1

    def draw(self, p):
        self.X_CHART = (self.width() - self.W_CHART) / 2
        self.Y_CHART = 0
        self.draw_h_grid(p)  # Grille horizontale & légende
        self.draw_v_grid(p)  # Grille verticale & légende
        self.draw_speed(p)  # Les vitesses
        self.draw_border(p)  # La bordure
