# !/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtGui import QPixmap, QPainter
from PyQt5.QtWidgets import QSplashScreen, QWidget, QVBoxLayout, QLabel


class LoadingWindow(QSplashScreen):
    def __init__(self, is_loaded):
        super(LoadingWindow, self).__init__(None)
        self.central_widget = QWidget(parent=self)
        self.content = QLabel()
        self.is_loaded = is_loaded
        self.init_widget()
        self.show()

    def init_widget(self):
        vbox = QVBoxLayout()
        pixmap = QPixmap("assets/images/arrow_down_vert_fonce.png")
        self.content.setPixmap(pixmap)
        self.content.setScaledContents(True)
        self.content.setFixedHeight(50)
        vbox.addWidget(self.content)
        self.setLayout(vbox)

    def on_close(self):
        self.is_loaded()
        self.close()

    def draw_fond(self, p):
        """
        Dessine un rectangle de la taille du bloc
        :param p: parametre de dessin
        """
        from ui.utils.drawing import draw_rectangle
        from constants.colors import color_bleu_gris
        draw_rectangle(p, 0, 0, self.width(), self.height(), color_bleu_gris)

    def paintEvent(self, event):
        p = QPainter()
        p.begin(self)
        self.draw(p)
        p.end()

    def draw(self, p):
        self.draw_fond(p)
