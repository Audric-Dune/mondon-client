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
        self.__init_widget__()

    def __init_widget__(self):
        self.vbox.addWidget(self.content, alignment=Qt.AlignVCenter | Qt.AlignCenter)
        self.setLayout(self.vbox)

    def set_image(self, img):
        pixmap = QPixmap(img)
        self.content.setPixmap(pixmap)
        self.content.setScaledContents(True)

    def setContentsMargins(self, margin=5):
        self.vbox.setContentsMargins(margin, margin, margin, margin)
