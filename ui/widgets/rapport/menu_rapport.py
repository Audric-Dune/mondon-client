# !/usr/bin/env python
# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QVBoxLayout, QScrollArea, QFileDialog, QDialog, QWidget, QSizePolicy
from PyQt5.QtGui import QPainter
from PyQt5.QtPrintSupport import QPrinter, QPrintDialog
from PyQt5.QtCore import QSize, Qt

from constants.colors import color_bleu_gris
from constants.stylesheets import white_title_label_stylesheet, button_stylesheet, scroll_bar_stylesheet
from stores.settings_store import settings_store
from ui.widgets.public.mondon_widget import MondonWidget
from ui.widgets.public.pixmap_button import PixmapButton
from ui.widgets.rapport.rapport import Rapport


class RapportMenu(MondonWidget):
    PIXMAPBUTTON_SIZE = QSize(40, 40)
    PAGE_W = 770
    PAGE_H = 1100

    def __init__(self, parent=None):
        super(RapportMenu, self).__init__(parent=parent)
        self.background_color = color_bleu_gris
        self.bt_impression = PixmapButton(parent=self)
        self.bt_save = PixmapButton(parent=self)
        self.bt_jour_plus = PixmapButton(parent=self)
        self.bt_jour_moins = PixmapButton(parent=self)
        self.label_date = QLabel()
        self.vbox = QVBoxLayout()
        self.hbox = QHBoxLayout()
        self.rapport = Rapport(parent=self)
        self.scrool_bar = QScrollArea()
        self.init_button()
        self.init_widget()
        self.scrool_bar.setFixedSize(self.width() - 20, self.height() - 65)

    def on_size_main_window_changed(self):
        self.scrool_bar.setFixedSize(self.width()-20, self.height()-65)

    def init_widget(self):
        label = QLabel("RAPPORT_MENU")
        label.setStyleSheet(white_title_label_stylesheet)
        self.hbox.addWidget(label)
        self.hbox.addWidget(self.bt_jour_moins)
        self.hbox.addWidget(self.bt_jour_plus)
        self.hbox.addWidget(self.bt_save)
        self.hbox.addWidget(self.bt_impression)
        self.vbox.addLayout(self.hbox)
        self.rapport.setFixedSize(771, 1100)
        content_scroll = QHBoxLayout()
        content_scroll.addWidget(self.rapport, alignment=Qt.AlignCenter)
        widget = QWidget(parent=self)
        widget.setLayout(content_scroll)
        self.scrool_bar.setWidget(widget)
        self.scrool_bar.setWidgetResizable(False)
        self.scrool_bar.setStyleSheet(scroll_bar_stylesheet)
        self.scrool_bar.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.vbox.addWidget(self.scrool_bar, alignment=Qt.AlignCenter)
        self.setLayout(self.vbox)

    def init_button(self):
        # Bouton sauvegarder
        self.bt_save.clicked.connect(self.save_pdf)
        self.bt_save.setStyleSheet(button_stylesheet)
        self.bt_save.setFixedSize(self.PIXMAPBUTTON_SIZE)
        self.bt_save.setContentsMargins(8)
        self.bt_save.addImage("assets/images/save_as.png")
        # Bouton impression
        self.bt_impression.clicked.connect(self.impression)
        self.bt_impression.setStyleSheet(button_stylesheet)
        self.bt_impression.setFixedSize(self.PIXMAPBUTTON_SIZE)
        self.bt_impression.addImage("assets/images/impression.png")

        # Bouton jour plus
        self.bt_jour_plus.clicked.connect(self.jour_plus)
        self.bt_jour_plus.setStyleSheet(button_stylesheet)
        self.bt_jour_plus.setFixedSize(self.PIXMAPBUTTON_SIZE)
        self.bt_jour_plus.addImage("assets/images/fleche_suivant.png")

        # Bouton jour moins
        self.bt_jour_moins.clicked.connect(self.jour_moins)
        self.bt_jour_moins.setStyleSheet(button_stylesheet)
        self.bt_jour_moins.setFixedSize(self.PIXMAPBUTTON_SIZE)
        self.bt_jour_moins.addImage("assets/images/fleche_precedent.png")

    def save_pdf(self):
        printer = QPrinter()
        painter = QPainter()
        file = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        name_file = "{}/2017_02_12_rapport_production_bobine.pdf".format(file)
        printer.setOutputFileName(name_file)
        printer.setOutputFormat(QPrinter.PdfFormat)
        printer.setPageMargins(10, 10, 10, 10, QPrinter.Point)
        painter.begin(printer)
        self.rapport.drawing(painter)
        painter.end()
        self.affiche_pdf(name_file)

    def impression(self):
        printer = QPrinter()
        dialog = QPrintDialog(printer, self)
        if dialog.exec_() != QDialog.Accepted:
            return
        painter = QPainter()
        printer.setPageMargins(10, 10, 10, 10, QPrinter.Point)
        painter.begin(printer)
        x_scale = printer.pageRect().width() / self.PAGE_W
        y_scale = printer.pageRect().height() / self.PAGE_H
        scale = min(x_scale, y_scale)
        painter.translate((printer.paperRect().x()) + (printer.pageRect().width() / 2),
                          printer.paperRect().y() + (printer.pageRect().height() / 2))
        painter.scale(scale, scale)
        painter.translate(-1 * self.PAGE_W / 2, -1 * self.PAGE_H / 2)
        self.rapport.drawing(painter)
        painter.end()

    @staticmethod
    def affiche_pdf(name_file):
        import os
        """affiche le pdf créé, dans le visualiseur pdf par défaut de l'OS"""
        if os.path.exists(name_file):
            try:
                # solution pour Windows
                os.startfile(name_file)
            except Exception as e:
                from lib.logger import logger
                logger.log("RAPPORT", "Impossible d'ouvrir le fichier PDF : {}".format(e))

    @staticmethod
    def jour_moins():
        settings_store.set_day_ago(settings_store.day_ago + 1)

    @staticmethod
    def jour_plus():
        settings_store.set_day_ago(settings_store.day_ago - 1)
