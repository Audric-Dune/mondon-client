# !/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QScrollArea, QVBoxLayout, QWidget
from PyQt5.QtCore import pyqtSignal
from commun.constants.colors import color_bleu_gris
from commun.constants.stylesheets import scroll_bar_stylesheet
from commun.ui.public.mondon_widget import MondonWidget
from commun.utils.layout import clear_layout
from gestion.ui.line_bobine import LigneBobine


class TabBobine(MondonWidget):
    DRAG_SIGNAL = pyqtSignal(str)
    STOP_DRAG_SIGNAL = pyqtSignal()

    def __init__(self, parent=None, plan_prod=None):
        super(TabBobine, self).__init__(parent=parent)
        self.plan_prod = plan_prod
        self.background_color = color_bleu_gris
        self.master_vbox = QVBoxLayout()
        self.vbox = QVBoxLayout()
        self.scroll_bar = QScrollArea(parent=self)
        self.scroll_bar.setStyleSheet(scroll_bar_stylesheet)
        self.scroll_bar.setWidgetResizable(True)
        self.content_scrollbar = QWidget(parent=self.scroll_bar)
        self.update_widget()

    def update_widget(self):
        clear_layout(self.vbox)
        for bobine in self.plan_prod.bobine_fille_store.bobines:
                line_bobine = LigneBobine(parent=self, bobine=bobine)
                line_bobine.DRAG_SIGNAL.connect(self.handle_drag_bobine_signal)
                line_bobine.STOP_DRAG_SIGNAL.connect(self.handle_stop_drag_bobine_signal)
                line_bobine.setFixedHeight(20)
                self.vbox.addWidget(line_bobine)
        self.content_scrollbar.setLayout(self.vbox)
        self.scroll_bar.setWidget(self.content_scrollbar)
        self.master_vbox.addWidget(self.scroll_bar)
        self.setLayout(self.master_vbox)

    def handle_drag_bobine_signal(self, bobine):
        self.DRAG_SIGNAL.emit(bobine)

    def handle_stop_drag_bobine_signal(self):
        self.STOP_DRAG_SIGNAL.emit()
