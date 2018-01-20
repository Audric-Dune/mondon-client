# !/usr/bin/env python
# -*- coding: utf-8 -*-


from PyQt5.QtWidgets import QMainWindow, QWidget, QHBoxLayout
from PyQt5.QtCore import Qt

from commun.ui.public.bague_perfo import BaguePerfo
from commun.ui.public.entretoise_perfo import EntretoisePerfo

class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__(parent=None, flags=Qt.Window)
        self.central_widget = QWidget(parent=self, flags=Qt.Widget)
        self.init_window()

    def init_window(self):
        hbox = QHBoxLayout()
        hbox.setSpacing(0)
        hbox.addStretch(1)
        hbox.addWidget(EntretoisePerfo(width_value=30))
        hbox.addWidget(BaguePerfo(width_value=80))
        hbox.addWidget(EntretoisePerfo(width_value=50))
        hbox.addWidget(BaguePerfo(width_value=80))
        hbox.addWidget(EntretoisePerfo(width_value=70))
        hbox.addWidget(BaguePerfo(width_value=80))
        hbox.addWidget(EntretoisePerfo(width_value=60))
        hbox.addWidget(BaguePerfo(width_value=80))
        hbox.addWidget(EntretoisePerfo(width_value=60))
        hbox.addWidget(BaguePerfo(width_value=80))
        hbox.addWidget(EntretoisePerfo(width_value=60))
        hbox.addWidget(BaguePerfo(width_value=80))
        hbox.addWidget(EntretoisePerfo(width_value=60))
        hbox.addWidget(BaguePerfo(width_value=80))
        hbox.addWidget(EntretoisePerfo(width_value=100))
        hbox.addStretch(1)
        self.central_widget.setLayout(hbox)
        self.setCentralWidget(self.central_widget)
