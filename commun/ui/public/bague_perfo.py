# !/usr/bin/env python
# -*- coding: utf-8 -*-

from commun.ui.public.mondon_widget import MondonWidget
from commun.utils.drawing import draw_rectangle, draw_text, draw_triangle
from commun.constants.colors import color_noir, color_rouge, color_beige


class BaguePerfo(MondonWidget):
    BAGUE_HEIGHT = 60  # with pic
    PIC_NUMBER = 10
    PIC_HEIGHT = 8
    # ARROW_LENGTH = 20
    ARROW_LENGTH = 0
    ARROW_SIZE = 5
    BORDER_SIZE = 1

    def __init__(self, parent=None, width_value=80, ech=1):
        super(BaguePerfo, self).__init__(parent=parent)
        self.width_value = width_value
        self.ech = ech
        self.setFixedSize(self.width_value*self.ech, (self.BAGUE_HEIGHT+self.ARROW_LENGTH*2)*self.ech)

    def draw_bague(self, p, pic_height, arrow_length):
        x = 0
        y = pic_height + arrow_length
        w = self.width() - 1
        h = self.height() - 2 * (pic_height + arrow_length)
        draw_rectangle(p, x, y, w, h, color=color_beige, border_color=color_noir)
        font_size = 16 * self.ech
        draw_text(p, x, y, w, h, color=color_noir, align="C", font_size=font_size, text=str(self.width_value))

    def draw_pic(self, p, pic_height, arrow_length):
        pic_count = 0
        while pic_count < self.PIC_NUMBER:
            y = arrow_length
            w = self.width() / self.PIC_NUMBER
            x = 0 + w * pic_count
            h = pic_height
            draw_triangle(p, x, y, w, h,
                          background_color=color_beige,
                          border_color=color_noir,
                          border_size=self.BORDER_SIZE)
            y = self.height() - pic_height - arrow_length
            draw_triangle(p, x, y, w, h,
                          background_color=color_beige,
                          border_color=color_noir,
                          border_size=self.BORDER_SIZE,
                          reverse=True)
            pic_count += 1

    def draw_arrow(self, p, arrow_length, arrow_size):
        x = self.width() / 2
        y = self.height() - arrow_length
        w = self.BORDER_SIZE
        h = arrow_length
        draw_rectangle(p, x, y, w, h, color=color_rouge)
        x = x - arrow_size / 2
        y = self.height() - arrow_size
        w = arrow_size + 2
        h = arrow_size
        draw_triangle(p, x, y, w, h,
                      background_color=color_rouge,
                      border_size=self.BORDER_SIZE,
                      reverse=True)

    def draw(self, p):
        pic_height = self.PIC_HEIGHT * self.ech
        arrow_length = self.ARROW_LENGTH * self.ech
        # arrow_size = self.ARROW_SIZE * self.ech
        self.draw_bague(p, pic_height, arrow_length)
        self.draw_pic(p, pic_height, arrow_length)
        # self.draw_arrow(p, arrow_length, arrow_size)
