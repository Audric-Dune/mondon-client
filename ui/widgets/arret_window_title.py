# !/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import timedelta
from PyQt5.QtGui import QPainter

from constants.colors import color_blanc, color_bleu_gris

from constants.dimensions import (
    padding_arret,
)

from ui.utils.drawing import draw_rectangle, draw_text
from ui.utils.timestamp import timestamp_to_hour_little, timestamp_to_date_little
from ui.widgets.mondon_widget import MondonWidget


class ArretWindowTitle(MondonWidget):
    def __init__(self, arret, parent):
        super(ArretWindowTitle, self).__init__(parent=parent)
        self.arret = arret

    def draw_fond(self, p):
        draw_rectangle(p, 0, 0, self.width(), self.height(), color_bleu_gris)

    def on_data_changed(self):
        self.update()

    def paintEvent(self, event):
        p = QPainter()
        p.begin(self)
        self.draw(p)
        p.end()

    def draw_date(self, p):
        start_time = self.arret.start
        text = str(timestamp_to_date_little(start_time))
        draw_text(p,
                  x=padding_arret,
                  y=0,
                  width=120,
                  height=50,
                  color=color_blanc,
                  align="G",
                  font_size=18,
                  text=text)

    def draw_hour(self, p):
        start_time = self.arret.start
        text = str(timestamp_to_hour_little(start_time))
        draw_text(p,
                  x=self.width()-120-padding_arret,
                  y=0,
                  width=120,
                  height=50,
                  color=color_blanc,
                  align="D",
                  font_size=18,
                  text=text)

    def draw_duration(self, p):
        duration_ts = self.arret.end - self.arret.start
        text = str(timedelta(seconds=round(duration_ts)))
        draw_text(p,
                  x=(self.width()-120)/2,
                  y=0,
                  width=120,
                  height=50,
                  color=color_blanc,
                  align="C",
                  font_size=22,
                  text=text)

    def draw(self, p):
        self.draw_fond(p)
        self.draw_date(p)
        self.draw_hour(p)
        self.draw_duration(p)
