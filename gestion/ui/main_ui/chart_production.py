# !/usr/bin/env python
# -*- coding: utf-8 -*-


from commun.constants.colors import color_blanc,\
    color_bleu_gris,\
    color_gris_moyen,\
    color_noir,\
    color_gris_fonce,\
    color_gris_clair
from commun.utils.color_bobine import get_color_bobine
from commun.constants.param import DEBUT_PROD_MATIN, FIN_PROD_SOIR
from commun.ui.public.mondon_widget import MondonWidget
from commun.utils.drawing import draw_rectangle, draw_text
from commun.utils.timestamp import timestamp_at_time, hour_in_timestamp


class ChartProd(MondonWidget):
    MARGIN = 10
    MARGIN_TEXT_H = 10
    MARGIN_START_CHART_H = 130
    MARGIN_END_CHART_H = 30
    MARGIN_START_CHART_V = 30
    MARGIN_END_CHART_V = 30
    HEIGHT_LINE = 40
    MARGIN_INTER_LINE = 0

    def __init__(self, parent=None, prods=None, events=None):
        super(ChartProd, self).__init__(parent=parent)
        self.prods = prods
        self.events = events
        self.setMinimumHeight(300)

    def draw_background(self, p):
        draw_rectangle(p, x=0, y=0, width=self.width(), height=self.height(), color=color_bleu_gris)

    def draw_fond_chart(self, p):
        draw_rectangle(p,
                       x=self.MARGIN,
                       y=self.MARGIN,
                       width=self.width()-self.MARGIN*2,
                       height=self.height()-self.MARGIN*2,
                       color=color_blanc)

    def draw_legend_h(self, p, index, text, height_line):
        draw_text(p,
                  x=self.MARGIN,
                  y=self.MARGIN+self.MARGIN_START_CHART_V+height_line*index+self.MARGIN_INTER_LINE*index,
                  width=self.MARGIN_START_CHART_H-self.MARGIN_TEXT_H,
                  height=height_line,
                  color=color_noir,
                  align="D",
                  font_size=12,
                  text=text)

    def draw_axis(self, p, x, width):
        draw_rectangle(p,
                       x=x,
                       y=self.MARGIN+self.MARGIN_START_CHART_V,
                       width=1,
                       height=self.height()-self.MARGIN*2-self.MARGIN_END_CHART_V-self.MARGIN_START_CHART_V+5,
                       color=color_noir)
        height_content_chart = self.height()-self.MARGIN*2-self.MARGIN_END_CHART_V-self.MARGIN_START_CHART_V
        draw_rectangle(p,
                       x=x,
                       y=self.MARGIN+self.MARGIN_START_CHART_V+height_content_chart,
                       width=width,
                       height=1,
                       color=color_noir)
        draw_rectangle(p,
                       x=x+width,
                       y=self.MARGIN+self.MARGIN_START_CHART_V,
                       width=1,
                       height=self.height()-self.MARGIN*2-self.MARGIN_END_CHART_V-self.MARGIN_START_CHART_V+5,
                       color=color_noir)
        draw_rectangle(p,
                       x=x,
                       y=self.MARGIN+self.MARGIN_START_CHART_V,
                       width=width,
                       height=1,
                       color=color_noir)

    def draw_prod(self, p, prod, x_init, width_total, height_line):
        ech = self.get_ech(width_total)
        start_day = self.get_start_day(prod)
        color = get_color_bobine(prod.bobine_papier_selected.color)
        draw_rectangle(p,
                       x=x_init+(prod.start-start_day)*ech,
                       y=self.MARGIN+self.MARGIN_START_CHART_V,
                       width=(prod.end-prod.start)*ech,
                       height=height_line,
                       color=color)
        draw_text(p,
                  x=x_init+((prod.start-start_day)*ech),
                  y=self.MARGIN+self.MARGIN_START_CHART_V,
                  width=(prod.end-prod.start)*ech,
                  height=height_line,
                  color=color_noir,
                  align="C",
                  font_size=12,
                  text=str(prod.index),
                  bold=True)

    def draw_time_end(self, p, prod, x_init, width_total, height_line):
        ech = self.get_ech(width_total)
        start_day = self.get_start_day(prod)
        draw_rectangle(p,
                       x=x_init+(prod.start-start_day)*ech+(prod.end-prod.start)*ech,
                       y=self.MARGIN+self.MARGIN_START_CHART_V-5,
                       width=1,
                       height=height_line+5,
                       color=color_gris_moyen)
        text_width = 50
        draw_text(p,
                  x=x_init+(prod.start-start_day)*ech+(prod.end-prod.start)*ech-text_width/2,
                  y=self.MARGIN_START_CHART_V/3,
                  width=text_width,
                  height=self.MARGIN_END_CHART_V,
                  color=color_noir,
                  align="C",
                  font_size=10,
                  text=hour_in_timestamp(prod.end))

    def draw_stop_time(self, p, event, x_init, width_total, height_line):
        ech = self.get_ech(width_total)
        start_day = self.get_start_day(event)
        draw_rectangle(p,
                       x=x_init+(event.start-start_day)*ech,
                       y=self.height()-self.MARGIN*2-self.MARGIN_START_CHART_V+self.MARGIN_END_CHART_V/3-height_line,
                       width=1,
                       height=height_line+5,
                       color=color_bleu_gris)
        text_width = 50
        draw_text(p,
                  x=x_init+(event.start-start_day)*ech-text_width/2,
                  y=self.height()-self.MARGIN*2-self.MARGIN_START_CHART_V+self.MARGIN_END_CHART_V/3,
                  width=text_width,
                  height=self.MARGIN_END_CHART_V,
                  color=color_noir,
                  align="C",
                  font_size=10,
                  text=hour_in_timestamp(event.start))
        draw_rectangle(p,
                       x=x_init+(event.start-start_day)*ech+(event.end-event.start)*ech,
                       y=self.height()-self.MARGIN*2-self.MARGIN_START_CHART_V+self.MARGIN_END_CHART_V/3-height_line,
                       width=1,
                       height=height_line+5,
                       color=color_bleu_gris)
        draw_text(p,
                  x=x_init+(event.start-start_day)*ech+(event.end-event.start)*ech-text_width/2,
                  y=self.height()-self.MARGIN*2-self.MARGIN_START_CHART_V+self.MARGIN_END_CHART_V/3,
                  width=text_width,
                  height=self.MARGIN_END_CHART_V,
                  color=color_noir,
                  align="C",
                  font_size=10,
                  text=hour_in_timestamp(event.end))

    def draw_time_day(self, p, x_init, width_total, hour, text_hour):
        ech = self.get_ech(width_total)
        text_width = 50
        draw_rectangle(p,
                       x=x_init+(hour-DEBUT_PROD_MATIN)*3600*ech,
                       y=self.MARGIN+self.MARGIN_START_CHART_V,
                       width=1,
                       height=self.height()-self.MARGIN*2-self.MARGIN_END_CHART_V-self.MARGIN_START_CHART_V+5,
                       color=color_gris_clair)
        draw_text(p,
                  x=x_init-text_width/2+(hour-DEBUT_PROD_MATIN)*3600*ech,
                  y=self.height()-self.MARGIN*2-self.MARGIN_START_CHART_V+self.MARGIN_END_CHART_V/3,
                  width=text_width,
                  height=self.MARGIN_END_CHART_V,
                  color=color_noir,
                  align="C",
                  font_size=10,
                  text=text_hour)

    def draw_event(self, p, event, x_init, width_total, height_line):
        ech = self.get_ech(width_total)
        start_day = self.get_start_day(event)
        dec_y = 0
        type = event.type
        if type == "stop":
            dec_y = 4*height_line
        draw_rectangle(p,
                       x=x_init+(event.start-start_day)*ech,
                       y=self.MARGIN+self.MARGIN_START_CHART_V+dec_y,
                       width=(event.end-event.start)*ech,
                       height=height_line,
                       color=color_gris_fonce)

    @staticmethod
    def get_ech(width_total):
        return width_total / ((FIN_PROD_SOIR - DEBUT_PROD_MATIN) * 3600)

    @staticmethod
    def get_start_day(e):
        return timestamp_at_time(e.start, hours=DEBUT_PROD_MATIN)

    def draw(self, p):
        all_margin_h = self.MARGIN*2+self.MARGIN_INTER_LINE*4+self.MARGIN_END_CHART_V+self.MARGIN_START_CHART_V
        height_line = (self.height()-all_margin_h)/5
        width_content_chart = self.width()-self.MARGIN*2-self.MARGIN_START_CHART_H-self.MARGIN_END_CHART_H
        x_content_chart = self.MARGIN+self.MARGIN_START_CHART_H
        self.draw_background(p)
        self.draw_fond_chart(p)
        self.draw_legend_h(p, 0, "Production", height_line=height_line)
        self.draw_legend_h(p, 1, "Réglage", height_line=height_line)
        self.draw_legend_h(p, 2, "Nettoyage", height_line=height_line)
        self.draw_legend_h(p, 3, "Maintenance", height_line=height_line)
        self.draw_legend_h(p, 4, "Sans production", height_line=height_line)
        self.draw_time_day(p, x_init=x_content_chart, width_total=width_content_chart, hour=6, text_hour="06:00")
        self.draw_time_day(p, x_init=x_content_chart, width_total=width_content_chart, hour=8, text_hour="08:00")
        self.draw_time_day(p, x_init=x_content_chart, width_total=width_content_chart, hour=10, text_hour="10:00")
        self.draw_time_day(p, x_init=x_content_chart, width_total=width_content_chart, hour=12, text_hour="12:00")
        self.draw_time_day(p, x_init=x_content_chart, width_total=width_content_chart, hour=14, text_hour="14:00")
        self.draw_time_day(p, x_init=x_content_chart, width_total=width_content_chart, hour=16, text_hour="16:00")
        self.draw_time_day(p, x_init=x_content_chart, width_total=width_content_chart, hour=18, text_hour="18:00")
        self.draw_time_day(p, x_init=x_content_chart, width_total=width_content_chart, hour=20, text_hour="20:00")
        self.draw_time_day(p, x_init=x_content_chart, width_total=width_content_chart, hour=22, text_hour="22:00")
        for prod in self.prods:
            self.draw_prod(p,
                           prod=prod,
                           x_init=x_content_chart,
                           width_total=width_content_chart,
                           height_line=height_line)
        for prod in self.prods:
            self.draw_time_end(p,
                               prod=prod,
                               x_init=x_content_chart,
                               width_total=width_content_chart,
                               height_line=height_line)
        for event in self.events:
            self.draw_event(p,
                            event=event,
                            x_init=x_content_chart,
                            width_total=width_content_chart,
                            height_line=height_line)
            self.draw_stop_time(p,
                                event=event,
                                x_init=x_content_chart,
                                width_total=width_content_chart,
                                height_line=height_line)
        self.draw_axis(p, x=x_content_chart, width=width_content_chart)
