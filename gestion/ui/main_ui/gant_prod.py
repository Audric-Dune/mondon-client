# !/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPen, QPainter, QColor, QFont
from PyQt5.QtCore import Qt, QRect

from commun.utils.timestamp import timestamp_at_day_ago, timestamp_at_time
from commun.constants.param import DEBUT_PROD_MATIN, FIN_PROD_SOIR
from commun.constants.colors import color_gris_noir, color_blanc, color_noir, color_gris_moyen
from gestion.ui.main_ui.event_ui import EventUi
from gestion.ui.main_ui.prod_ui import ProdUi


class GantProd(QWidget):
    DEC_X_LEFT = 100
    DEC_X_RIGHT = 20
    DEC_X = DEC_X_LEFT + DEC_X_RIGHT
    DEC_Y_TOP = 10
    DEC_Y_BOTTOM = 20

    def __init__(self, prods, events):
        super(GantProd, self).__init__()
        self.setFocusPolicy(Qt.ClickFocus)
        self.items = []
        self.labels = []
        self.start_day = None
        self.end_day = None
        self.prods = prods
        self.events = events
        self.setFixedHeight(self.DEC_Y_TOP+self.DEC_Y_BOTTOM+50*4+5*3)
        self.init_ui()

    def resizeEvent(self, e):
        self.init_ui()
        super(GantProd, self).resizeEvent(e)

    def paintEvent(self, e):
        p = QPainter(self)
        self.draw_background(p)
        self.draw_border(p)
        self.draw_init_axis(p)
        self.draw_axis(p)
        self.draw_legend_h(p)
        self.draw_legend_v(p)
        p.end()
        super(GantProd, self).paintEvent(e)

    def draw_init_axis(self, p):
        color = color_noir.rgb_components
        qcolor = QColor(color[0], color[1], color[2])
        pen = QPen()
        pen.setColor(qcolor)
        p.setPen(pen)
        p.drawLine(self.DEC_X_LEFT, self.DEC_Y_TOP, self.DEC_X_LEFT, self.height()-self.DEC_Y_BOTTOM)
        p.drawLine(self.width()-self.DEC_X_RIGHT, self.DEC_Y_TOP, self.width()-self.DEC_X_RIGHT,
                   self.height()-self.DEC_Y_BOTTOM)
        p.drawLine(self.DEC_X_LEFT, self.height()-self.DEC_Y_BOTTOM,
                   self.width()-self.DEC_X_RIGHT, self.height()-self.DEC_Y_BOTTOM)

    def draw_axis(self, p):
        color = color_gris_moyen.rgb_components
        qcolor = QColor(color[0], color[1], color[2])
        pen = QPen()
        pen.setColor(qcolor)
        p.setPen(pen)
        i = 0
        ech_dec = (self.width()-self.DEC_X)/8
        dec = 0
        while i < 7:
            dec += ech_dec
            p.drawLine(self.DEC_X_LEFT+dec, self.DEC_Y_TOP, self.DEC_X_LEFT+dec, self.height()-self.DEC_Y_BOTTOM+2)
            i += 1

    def draw_border(self, p):
        color = color_gris_noir.rgb_components
        qcolor = QColor(color[0], color[1], color[2])
        pen = QPen()
        pen.setColor(qcolor)
        p.setPen(pen)
        p.drawRect(0, 0, self.width()-1, self.height()-1)

    def draw_background(self, p):
        color = color_blanc.rgb_components
        qcolor = QColor(color[0], color[1], color[2])
        p.fillRect(0, 0, self.width()-1, self.height()-1, qcolor)

    def draw_legend_h(self, p):
        size_text = 30
        color = color_noir.rgb_components
        qcolor = QColor(color[0], color[1], color[2])
        pen = QPen()
        pen.setColor(qcolor)
        p.setPen(pen)
        p.setFont(QFont("Arial Narrow", 10))
        i = 0
        ech_dec = (self.width()-self.DEC_X)/8
        dec = self.DEC_X_LEFT - size_text/2
        start_hour = 6
        while i < 9:
            dec += ech_dec
            x = dec-ech_dec
            y = self.height()-self.DEC_Y_BOTTOM
            rec_text = QRect(x, y, size_text, self.DEC_Y_BOTTOM)
            text = "{}:00".format(start_hour)
            p.drawText(rec_text, Qt.AlignCenter, text)
            start_hour += 2
            i += 1

    def draw_legend_v(self, p):
        color = color_noir.rgb_components
        qcolor = QColor(color[0], color[1], color[2])
        pen = QPen()
        pen.setColor(qcolor)
        p.setPen(pen)
        p.setFont(QFont("Arial Narrow", 10))
        text_rect = QRect(0, self.DEC_Y_TOP, self.DEC_X_LEFT-10, 50)
        p.drawText(text_rect, Qt.AlignRight | Qt.AlignVCenter, "Production")
        text_rect = QRect(0, self.DEC_Y_TOP+55, self.DEC_X_LEFT-10, 50)
        p.drawText(text_rect, Qt.AlignRight | Qt.AlignVCenter, "Nettoyage")
        text_rect = QRect(0, self.DEC_Y_TOP+110, self.DEC_X_LEFT-10, 50)
        p.drawText(text_rect, Qt.AlignRight | Qt.AlignVCenter, "Maintenance")
        text_rect = QRect(0, self.DEC_Y_TOP+165, self.DEC_X_LEFT-10, 50)
        p.drawText(text_rect, Qt.AlignRight | Qt.AlignVCenter, "Arrêt production")

    def init_ui(self):
        for item in self.items:
            item.setParent(None)
        ech = (self.width()-self.DEC_X)/57600
        for prod in self.prods:
            new_prod = ProdUi(parent=self, prod=prod, ech=ech)
            x = (prod.start - self.start_day) * ech + self.DEC_X_LEFT
            y = self.DEC_Y_TOP
            new_prod.setGeometry(x, y, new_prod.width(), new_prod.height())
            self.items.append(new_prod)
        for event in self.events:
            new_event = EventUi(parent=self, event=event, ech=ech)
            x = (event.start - self.start_day) * ech + self.DEC_X_LEFT
            if event.p_type == "clean":
                y = self.DEC_Y_TOP + 55
            elif event.p_type == "tool":
                y = self.DEC_Y_TOP + 110
            else:
                y = self.DEC_Y_TOP + 166
            new_event.setGeometry(x, y, new_event.width(), new_event.height())
            self.items.append(new_event)

    def update_data(self, prods, events, day_ago):
        self.start_day = timestamp_at_time(timestamp_at_day_ago(day_ago), hours=DEBUT_PROD_MATIN)
        self.end_day = timestamp_at_time(timestamp_at_day_ago(day_ago), hours=FIN_PROD_SOIR)
        self.prods = prods
        self.events = events
        self.init_ui()
