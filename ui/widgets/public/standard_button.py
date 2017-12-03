# !/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QPushButton


class StandardButton(QPushButton):

    def __init__(self, parent=None):
        super(StandardButton, self).__init__(parent)

    def set_img(self, img):
        pixmap = QPixmap(img)
        self.content.setPixmap(pixmap)
        self.content.setScaledContents(True)
