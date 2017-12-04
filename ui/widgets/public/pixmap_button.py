# !/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtCore import Qt, QEvent
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QPushButton, QLabel, QVBoxLayout


class PixmapButton(QPushButton):

    def __init__(self, parent=None):
        super(PixmapButton, self).__init__(parent)
        self.content = QLabel()
        self.vbox = QVBoxLayout()
        self.setContentsMargins()
        self.__init_widget__()
        self.setMouseTracking(True)
        self.img = None
        self.hover_img = None

    def __init_widget__(self):
        self.vbox.addWidget(self.content, alignment=Qt.AlignVCenter | Qt.AlignCenter)
        self.setLayout(self.vbox)

    def __set_image__(self, img):
        self.img = img
        pixmap = QPixmap(img)
        self.content.setPixmap(pixmap)
        self.content.setScaledContents(True)

    def addImage(self, img):
        self.img = img
        self.__set_image__(img)

    def addHoverImage(self, img):
        self.hover_img = img

    def setContentsMargins(self, margin=5):
        self.vbox.setContentsMargins(margin, margin, margin, margin)

    def enterEvent(self, event):
        if self.hover_img:
            self.__set_image__(self.hover_img)

    def leaveEvent(self, event):
        if self.hover_img:
            self.__set_image__(self.img)
