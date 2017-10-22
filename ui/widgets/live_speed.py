# !/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtGui import QPainter

from constants.colors import color_blanc, color_bleu_gris

from stores.data_store_manager import data_store_manager
from ui.widgets.mondon_widget import MondonWidget
from ui.utils.drawing import draw_rectangle, draw_text


class LiveSpeed(MondonWidget):
    def __init__(self, parent=None):
        super(LiveSpeed, self).__init__(parent=parent)
        self.last_speed = None
        self.update()

    def on_data_changed(self):
        self.last_speed = data_store_manager.get_most_recent_store().get_last_speed()
        self.update()

    def paintEvent(self, event):
        p = QPainter()
        p.begin(self)
        self.draw(p)
        p.end()

    def draw_fond(self, p):
        draw_rectangle(p, 0, 0, self.width(), self.height(), color_bleu_gris)

    def draw_speed_actuelle(self, p):
        text = "0 m/min"
        if self.last_speed:
            speed = self.last_speed[1]
            text = "{speed} m/min".format(speed=speed)
        text_width = self.width()
        text_height = self.height()
        draw_text(p,
                  x=10,
                  y=0,
                  width=text_width,
                  height=text_height,
                  color=color_blanc,
                  align="G",
                  font_size=22,
                  text=text)

    def draw(self, p):
        self.draw_fond(p)
        self.draw_speed_actuelle(p)
