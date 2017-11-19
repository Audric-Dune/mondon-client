# !/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter

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


class Chart(MondonWidget):
    def __init__(self, parent):
        super(Chart, self).__init__(parent=parent)
        self.drag_offset = 0
        self.mouse_move_pos = None

    def on_data_changed(self):
        self.update()

    def on_settings_changed(self, prev_live, prev_day_ago, prev_zoom):
        if prev_zoom != settings_store.zoom:
            ratio = settings_store.zoom / prev_zoom
            self.drag_offset = ratio * self.drag_offset + ratio * self.get_chart_width() / 2 - self.get_chart_width() / 2
            self.adjust_drag_offset()
            self.update()

    def get_chart_width(self):
        return self.width() - chart_margin_left - chart_margin_right

    def get_chart_height(self):
        return self.height() - chart_margin_top - chart_margin_bottom

    def mousePressEvent(self, event):
        self.mouse_move_pos = None
        if event.button() == Qt.LeftButton:
            self.mouse_move_pos = event.globalPos().x()
        super(Chart, self).mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton and self.mouse_move_pos is not None:
            global_pos = event.globalPos().x()
            debut, fin, _ = self.get_drawing_info()
            self.drag_offset -= global_pos - self.mouse_move_pos
            self.adjust_drag_offset()
            self.mouse_move_pos = global_pos
            self.update()
        super(Chart, self).mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        self.mouse_move_pos = None
        super(Chart, self).mouseReleaseEvent(event)

    def wheelEvent(self, event):
        delta = event.pixelDelta().y()
        ratio = 1 -delta / 100
        settings_store.set_zoom(settings_store.zoom * ratio)

    def adjust_drag_offset(self):
            min_offset = 0
            max_offset = self.get_chart_width() * settings_store.zoom - self.get_chart_width()
            if self.drag_offset < min_offset:
                self.drag_offset = min_offset
            if self.drag_offset > max_offset:
                self.drag_offset = max_offset

    def paintEvent(self, event):
        p = QPainter()
        p.begin(self)
        self.draw(p)
        p.end()

    def get_drawing_info(self):
        timestamp = timestamp_at_day_ago(settings_store.day_ago)
        debut = timestamp_at_time(timestamp, hours=chart_min_hour)
        fin = timestamp_at_time(timestamp, hours=chart_max_hour)
        ech = (fin - debut) / (settings_store.zoom * self.get_chart_width())
        return debut, fin, ech

    def draw_horizontal_grille(self, p):
            for i in range(4):
                draw_rectangle(p,
                               x=chart_margin_left,
                               y=self.get_chart_height() + chart_margin_top - i * self.get_chart_height() / 4,
                               width=self.get_chart_width(),
                               height=width_grille,
                               color=color_gris_clair)

    def draw_horizontal_label(self, p):
            for i in range(4):
                draw_text(p,
                          x=chart_margin_left - 10 - 60,
                          y=self.get_chart_height() + chart_margin_top - i * self.get_chart_height() / 4 - 10,
                          width=60,
                          height=20,
                          color=color_blanc,
                          align="D",
                          font_size=10,
                          text='{speed}m/min'.format(speed=50 * i))
                draw_text(p,
                          x=chart_margin_right - 10 + 20 + self.get_chart_width(),
                          y=self.get_chart_height() + chart_margin_top - i * self.get_chart_height() / 4 - 10,
                          width=60,
                          height=20,
                          color=color_blanc,
                          align="G",
                          font_size=10,
                          text='{speed}m/min'.format(speed=50 * i))

    def draw_repere_maximum(self, p):
        draw_rectangle(p,
                       x=chart_margin_left,
                       y=self.get_chart_height() + chart_margin_top - self.get_chart_height() * 0.9,
                       width=self.get_chart_width(),
                       height=width_grille * 2,
                       color=color_noir)
        draw_text(p,
                  x=chart_margin_left - 10 - 60,
                  y=self.get_chart_height() + chart_margin_top - self.get_chart_height() * 0.9 - 10,
                  width=60,
                  height=20,
                  color=color_blanc,
                  align="D",
                  font_size=10,
                  text='180m/min')
        draw_text(p,
                  x=chart_margin_right - 10 + 20 + self.get_chart_width(),
                  y=self.get_chart_height() + chart_margin_top - self.get_chart_height() * 0.9 - 10,
                  width=60,
                  height=20,
                  color=color_blanc,
                  align="G",
                  font_size=10,
                  text='180m/min')

    def draw_principale_x_axis(self, p, i, t):
        draw_rectangle(p,
                       x=i + chart_margin_left,
                       y=chart_margin_top,
                       width=width_grille,
                       height=self.height() - chart_margin_bottom - chart_margin_top + 10,
                       color=color_gris_moyen)
        draw_text(p,
                  x=i + chart_margin_left - 20,
                  y=self.get_chart_height() + chart_margin_top + 10,
                  height=40,
                  width=40,
                  color=color_blanc,
                  align="C",
                  font_size=10,
                  text=hour_in_timestamp(t))

    def draw_secondaire_x_axis(self, p, i):
        draw_rectangle(p,
                       x=i + chart_margin_left,
                       y=chart_margin_top,
                       width=width_grille,
                       height=self.height() - chart_margin_bottom - chart_margin_top + 5,
                       color=color_gris_clair)

    def draw_speed(self, p, i, speed):
        if speed < 0:
            color = color_gris_fonce
            draw_rectangle(p,
                           x=i * 1 + chart_margin_left,
                           y=chart_margin_top + self.get_chart_height() - 10,
                           width=1,
                           height=10,
                           color=color)
        else:
            if speed < 30:
                color = color_rouge
            else:
                color = color_vert
            draw_rectangle(p,
                           x=i * 1 + chart_margin_left,
                           y=chart_margin_top + self.get_chart_height() - speed * (self.get_chart_height()/200) + 1,
                           width=1,
                           height=speed * (self.get_chart_height()/200),
                           color=color)

    def draw_chart_and_vertical_grid(self, p):
        debut, fin, ech = self.get_drawing_info()
        extra_drawing = 10  # Sur combien de pixels supplémentaires on trace à gauche et à droite
        t = debut + (self.drag_offset - extra_drawing) * ech
        i = -extra_drawing
        while i <= self.get_chart_width() + extra_drawing:
            if abs(timestamp_au_debut_de_hour(t) - t) < ech:
                self.draw_principale_x_axis(p, i, t)
            diff = 2 * ech
            for min in (15, 30, 45):
                current_diff = timestamp_au_debut_de_hour(t, min) - t
                if abs(current_diff) < diff:
                    diff = current_diff
            if -ech / 2 <= diff < ech / 2:
                self.draw_secondaire_x_axis(p, i)
            speed = data_store_manager.get_current_store().get_speed(t, t + ech)
            self.draw_speed(p, i, speed)
            t += ech
            i += 1

    def draw_background(self, p):
        draw_rectangle(p, chart_margin_left, chart_margin_top, self.get_chart_width(), self.get_chart_height(), color_blanc)

    def draw_container_horizontal_background(self, p):
        color = color_bleu_gris
        # Bande horizontale haut
        draw_rectangle(p, 0, 0, self.width(), chart_margin_top, color)
        # Bande horizontale haut
        draw_rectangle(p, 0, self.height() - chart_margin_bottom, self.width(), chart_margin_bottom, color)

    def draw_container_vertical_background(self, p):
        color = color_bleu_gris
        # Le 10px de plus est pour cacher les barres de l'axis horizontal.
        height = self.height() - chart_margin_top - chart_margin_bottom + 10
        # Bande verticale gauche
        draw_rectangle(p, 0, chart_margin_top, chart_margin_left, height, color)
        # Bande verticale droite (le +1 pour la coordonnée "x" est pour ne pas cacher la dernière
        # barre de la grille verticale.
        draw_rectangle(p, self.width() - chart_margin_right + 1, chart_margin_top, chart_margin_right, height, color)

    def draw(self, p):
        self.draw_background(p)  # Le fond blanc

        self.draw_container_horizontal_background(p)  # Le haut et bas du fond (bleu) du container
        self.draw_horizontal_grille(p)  # La grille horizontale
        self.draw_chart_and_vertical_grid(p)  # Les données et la grille verticale

        self.draw_container_vertical_background(p)  # Les côtés du fond (bleu) du container
        self.draw_horizontal_label(p)  # Les labels des axes verticaux
        self.draw_repere_maximum(p)  # Le repère de la vitesse maximum

