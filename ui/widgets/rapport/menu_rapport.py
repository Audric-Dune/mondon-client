# !/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QHBoxLayout, QLabel, QVBoxLayout, QScrollArea, QWidget
from PyQt5.QtGui import QPainter, QFont
from PyQt5.QtPrintSupport import QPrinter, QPrintDialog
from PyQt5.QtCore import QSize, Qt, QPoint

from ui.widgets.prod.chart.chart import Chart
from ui.widgets.prod.chart_stat.stat_titre import StatTitre
from ui.widgets.prod.tableau_arret.tab_arret_menu import TabArretMenu

from constants.colors import color_bleu_gris
from constants.stylesheets import white_title_label_stylesheet, button_stylesheet, scroll_bar_stylesheet
from ui.widgets.public.mondon_widget import MondonWidget
from ui.widgets.public.pixmap_button import PixmapButton


class RapportMenu(MondonWidget):
    PIXMAPBUTTON_SIZE = QSize(40, 40)

    def __init__(self, parent=None):
        super(RapportMenu, self).__init__(parent=parent)
        self.background_color = color_bleu_gris
        self.bt_impression = PixmapButton(parent=self)
        self.vbox = QVBoxLayout()
        self.hbox = QHBoxLayout()
        self.scrool_bar = QScrollArea()
        self.rapport = self.create_rapport()
        self.init_button()
        self.init_widget()

    def init_widget(self):
        label = QLabel("RAPPORT_MENU")
        label.setStyleSheet(white_title_label_stylesheet)
        self.hbox.addWidget(label)
        self.hbox.addWidget(self.bt_impression)
        self.vbox.addLayout(self.hbox)

        self.scrool_bar.setWidget(self.rapport)
        self.scrool_bar.setStyleSheet(scroll_bar_stylesheet)
        self.vbox.addWidget(self.scrool_bar)

        self.setLayout(self.vbox)

    def init_button(self):
        # Bouton impression
        self.bt_impression.clicked.connect(self.impression)
        self.bt_impression.setStyleSheet(button_stylesheet)
        self.bt_impression.setFixedSize(self.PIXMAPBUTTON_SIZE)
        self.bt_impression.addImage("assets/images/impression.png")

    def impression(self):
        printer = QPrinter()
        # printer.setOutputFileName("print.pdf")
        painter = QPainter()
        painter.begin(printer)
        self.rapport.render(painter, QPoint())
        # self.rapport.render(painter)

        painter.end()

    # def impression(self):
    #     printer = QPrinter(QPrinter.HighResolution)
    #     painter = QPainter()
    #     painter.begin(printer)
    #     # rectangle = painter.viewport()
    #     # size = self.rapport.size()
    #     # size.scale(rectangle.size(), Qt.KeepAspectRatio)
    #     # painter.setViewport(rectangle.x(), rectangle.y(), size.width(), size.height())
    #     self.rapport.render(painter)
    #     painter.end()

    # def impression(self):
    #     widget = self.rapport
    #     painter = QPainter(QPrinter())
    #     rectangle = painter.viewport()
    #     size = widget.size()
    #     size.scale(rectangle.size(), Qt.KeepAspectRatio)
    #     painter.setViewport(rectangle.x(), rectangle.y(), size.width(), size.height())
    #     widget.render(painter)

    # def impression(self):
    #     printer = QPrinter()
    #     dialog = QPrintDialog(printer)
    #     dialog.setModal(True)
    #     dialog.setWindowTitle("Print Document")
    #     if dialog.exec_() == True:
    #         self.rapport.print_(printer)

    def create_rapport(self):
        vbox = QVBoxLayout()

        chart = Chart(parent=self)
        chart.setFixedHeight(300)
        chart.setFixedWidth(750)
        vbox.addWidget(chart)

        stat_menu = StatTitre(parent=self, note=False)
        vbox.addWidget(stat_menu)

        tab_arret_menu = TabArretMenu(parent=self, scrollbar=False)
        vbox.addWidget(tab_arret_menu)

        rapport = QWidget()
        rapport.setLayout(vbox)

        return rapport

