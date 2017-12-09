# !/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QPushButton, QLabel, QVBoxLayout


class PixmapButton(QPushButton):

    def __init__(self, parent=None):
        super(PixmapButton, self).__init__(parent)
        self.content = QLabel()
        self.vbox = QVBoxLayout()
        self.setContentsMargins()
        self._init_widget()
        self.img = None
        self.hover_img = None

    def _init_widget(self):
        self.vbox.addWidget(self.content, alignment=Qt.AlignVCenter | Qt.AlignCenter)
        self.setLayout(self.vbox)

    def _set_image(self, img):
        self.img = img
        pixmap = QPixmap(img)
        self.content.setPixmap(pixmap)
        self.content.setScaledContents(True)

    def addImage(self, img):
        self.img = img
        self._set_image(img)

    def setContentsMargins(self, margin=5):
        self.vbox.setContentsMargins(margin, margin, margin, margin)