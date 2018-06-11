# !/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt

from commun.utils.timestamp import timestamp_at_day_ago, timestamp_at_time
from commun.constants.param import DEBUT_PROD_MATIN, FIN_PROD_SOIR
from gestion.ui.main_ui.event_ui import EventUi
from gestion.ui.main_ui.prod_ui import ProdUi


class GantProd(QWidget):
    def __init__(self, prods, events):
        super(GantProd, self).__init__()
        self.setFocusPolicy(Qt.ClickFocus)
        self.items = []
        self.start_day = None
        self.end_day = None
        self.prods = prods
        self.events = events
        self.setFixedHeight(290)
        self.init_ui()

    def resizeEvent(self, e):
        self.init_ui()
        super(GantProd, self).resizeEvent(e)

    def init_ui(self):
        for item in self.items:
            item.setParent(None)
        ech = self.width()/57600
        for prod in self.prods:
            new_prod = ProdUi(parent=self, prod=prod, ech=ech)
            x = (prod.start - self.start_day) * ech
            y = 5
            new_prod.setGeometry(x, y, new_prod.width(), new_prod.height())
            self.items.append(new_prod)
        for event in self.events:
            new_event = EventUi(parent=self, event=event, ech=ech)
            x = (event.start - self.start_day) * ech
            if event.p_type == "clean":
                y = 115
            elif event.p_type == "tool":
                y = 170
            else:
                y = 235
            new_event.setGeometry(x, y, new_event.width(), new_event.height())
            self.items.append(new_event)

    def update_data(self, prods, events, day_ago):
        self.start_day = timestamp_at_time(timestamp_at_day_ago(day_ago), hours=DEBUT_PROD_MATIN)
        self.end_day = timestamp_at_time(timestamp_at_day_ago(day_ago), hours=FIN_PROD_SOIR)
        self.prods = prods
        self.events = events
        self.init_ui()
