# !/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.Qt import Qt
from PyQt5.QtCore import QMargins
from PyQt5.QtGui import QPainter, QPixmap
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout

from constants.colors import color_vert_fonce, color_blanc, color_noir
from constants.stylesheets import create_qlabel_stylesheet
from ui.utils.drawing import draw_rectangle_radius


class StandardButton(QWidget):
    # _____DEFINITION CONSTANTE CLASS_____
    INIT_HEIGHT = 40
    INIT_WIDTH = 40
    INIT_RADIUS = 5
    INIT_VBOX_MARGIN = QMargins(20, 0, 20, 0)
    INIT_VBOX_NO_MARGIN = QMargins(0, 0, 0, 0)
    COLOR = color_blanc
    FONT_SIZE = 22

    def __init__(self, text=None, parent=None):
        super(StandardButton, self).__init__(parent=parent)
        # _____PARAMETRES INITIALS_____
        self.background_color = color_vert_fonce
        self.label_stylesheet = create_qlabel_stylesheet(color=self.COLOR, font_size="{}px".format(self.FONT_SIZE), background_color=color_noir)
        # _____INIT WIDGET_____
        self.vbox = QVBoxLayout(self)
        self.content = QLabel(text)
        self.content.setFixedHeight(self.INIT_HEIGHT)
        self.content.setStyleSheet(self.label_stylesheet)
        self.vbox.addWidget(self.content, alignment=Qt.AlignCenter)
        self.setLayout(self.vbox)
        if text:
            self.setFixedHeight(self.INIT_HEIGHT)
            self.vbox.setContentsMargins(self.INIT_VBOX_MARGIN)
        else:
            self.setFixedSize(self.INIT_WIDTH, self.INIT_HEIGHT)
            self.vbox.setContentsMargins(self.INIT_VBOX_NO_MARGIN)

    def set_img(self, img):
        pixmap = QPixmap(img)
        self.content.setPixmap(pixmap)
        self.content.setScaledContents(True)

    def draw_fond(self, p):
        """
        Dessine un rectangle de la taille du bloc
        :param p: parametre de dessin
        """
        draw_rectangle_radius(p, 0, 0, self.width(), self.height(), self.background_color, radius=self.INIT_RADIUS)

    def paintEvent(self, event):
        p = QPainter()
        p.begin(self)
        self.draw(p)
        p.end()

    def draw(self, p):
        self.draw_fond(p)
