# !/usr/bin/env python
# -*- coding: utf-8 -*-


from PyQt5.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QScrollArea, QVBoxLayout
from PyQt5.QtCore import Qt

from commun.stores.bobine_fille_store import bobine_filles_store
from commun.ui.public.bague_perfo import BaguePerfo
from commun.ui.public.entretoise_perfo import EntretoisePerfo


class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__(parent=None, flags=Qt.Window)
        self.central_widget = QWidget(parent=self, flags=Qt.Widget)
