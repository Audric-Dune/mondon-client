# !/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout


class Image(QWidget):

    def __init__(self, img, size, background_color=None, parent=None):
        super(Image, self).__init__(parent)
        if background_color:
            self.setStyleSheet("background-color:{};".format(background_color.hex_string))
        self.setFixedSize(size, size)
        self.img = img
        self.content = QLabel()
        self.vbox = QVBoxLayout()
        self.setContentsMargins()
        self._init_widget()

    def _init_widget(self):
        self._set_image()
        self.vbox.addWidget(self.content, alignment=Qt.AlignVCenter | Qt.AlignCenter)
        self.setLayout(self.vbox)

    def _set_image(self):
        pixmap = QPixmap(self.img)
        self.content.setPixmap(pixmap)
        self.content.setScaledContents(True)

    def setContentsMargins(self, margin=0):
        self.vbox.setContentsMargins(margin, margin, margin, margin)
