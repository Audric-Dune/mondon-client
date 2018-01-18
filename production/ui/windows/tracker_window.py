# !/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtCore import QSize, QMargins
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QMainWindow, QHBoxLayout, QWidget

from commun.constants.colors import color_bleu_gris
from commun.constants.stylesheets import button_stylesheet
from commun.ui.public.pixmap_button import PixmapButton
from commun.utils.drawing import draw_rectangle

from production.ui.application import app
from production.ui.widgets.prod.chart.live_speed import LiveSpeed


class TrackerWindow(QMainWindow):
    BT_SIZE = QSize(30, 30)
    MARGIN = QMargins(5, 5, 5, 5)
    PADDING = 10

    def __init__(self, on_close):
        super(TrackerWindow, self).__init__(None)
        self.on_close = on_close
        self.live_speed = LiveSpeed(parent=self)
        self.bt_retour = PixmapButton(parent=self)
        self.init_widget()

    def init_widget(self):
        central_widget = QWidget(self)
        central_widget.setContentsMargins(self.MARGIN)

        hbox = QHBoxLayout()
        hbox.addWidget(self.live_speed)
        self.bt_retour.setFixedSize(self.BT_SIZE)
        self.bt_retour.setStyleSheet(button_stylesheet)
        self.bt_retour.clicked.connect(self.new_main_window)
        self.bt_retour.addImage("commun/assets/images/fleche_precedent.png")
        hbox.addWidget(self.bt_retour)

        central_widget.setLayout(hbox)
        self.setCentralWidget(central_widget)

    @staticmethod
    def new_main_window():
        app.create_main_window()

    def closeEvent(self, event):
        self.on_close()

    def draw_fond(self, p):
        """
        Dessine un rectangle de la taille du bloc
        :param p: parametre de dessin
        """
        draw_rectangle(p, self.PADDING, self.PADDING, self.width()-self.PADDING*2, self.height()-self.PADDING*2, color_bleu_gris)

    def paintEvent(self, event):
        p = QPainter()
        p.begin(self)
        self.draw(p)
        p.end()

    def draw(self, p):
        self.draw_fond(p)
