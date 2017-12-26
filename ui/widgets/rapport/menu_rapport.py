# !/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QHBoxLayout, QLabel, QFileDialog, QDialog, QPushButton
from PyQt5.QtGui import QPainter
from PyQt5.QtPrintSupport import QPrinter, QPrintDialog
from PyQt5.QtCore import QSize, Qt

from constants.colors import color_bleu_gris
from constants.stylesheets import button_stylesheet, white_22_label_stylesheet, button_little_stylesheet
from stores.settings_store import settings_store
from ui.utils.timestamp import timestamp_at_day_ago, timestamp_to_date, timestamp_to_inverse_date
from ui.widgets.public.mondon_widget import MondonWidget
from ui.widgets.public.pixmap_button import PixmapButton
from ui.widgets.rapport.rapport import Rapport


class RapportMenu(MondonWidget):
    PIXMAPBUTTON_SIZE = QSize(40, 40)
    BUTTON_HEIGHT = 40
    BUTTON_WIDTH = 100
    PAGE_W = 770
    PAGE_H = 1100
    MINIMUN_WIDTH_LABEL = 350

    def __init__(self, parent=None):
        super(RapportMenu, self).__init__(parent=parent)
        self.background_color = color_bleu_gris
        self.bt_impression = PixmapButton(parent=self)
        self.bt_save = PixmapButton(parent=self)
        self.bt_jour_plus = PixmapButton(parent=self)
        self.bt_jour_moins = PixmapButton(parent=self)
        self.bt_live = QPushButton("Aujourd'hui")
        self.label_date = QLabel()
        self.rapport = Rapport(parent=self)
        self.rapport.hide()
        self.init_button()
        self.init_widget()
        self.update_button()
        self.update_label()

    def on_settings_changed(self, prev_live, prev_day_ago, prev_zoom):
        self.update_button()
        self.update_label()

    def init_widget(self):
        menu_hbox = QHBoxLayout()

        left_hbox = QHBoxLayout()
        left_hbox.addWidget(self.bt_live)
        left_hbox.addStretch(1)
        menu_hbox.addLayout(left_hbox)

        date_hbox = QHBoxLayout()
        date_hbox.addStretch(1)
        date_hbox.addWidget(self.bt_jour_moins)
        self.label_date.setStyleSheet(white_22_label_stylesheet)
        date_hbox.addWidget(self.label_date)
        date_hbox.addWidget(self.bt_jour_plus)
        date_hbox.addStretch(1)
        menu_hbox.addLayout(date_hbox)

        right_hbox = QHBoxLayout()
        right_hbox.addStretch(1)
        right_hbox.addWidget(self.bt_save)
        right_hbox.addWidget(self.bt_impression)
        menu_hbox.addLayout(right_hbox)

        self.setLayout(menu_hbox)

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

        # Bouton live
        self.bt_live.clicked.connect(self.live)
        self.bt_live.setFixedSize(self.BUTTON_WIDTH, self.BUTTON_HEIGHT)
        self.bt_live.setStyleSheet(button_little_stylesheet)

    def update_button(self):
        self.bt_jour_plus.setEnabled(settings_store.day_ago > 0)
        self.bt_live.setEnabled(settings_store.day_ago > 0)

    def update_label(self):
        ts = timestamp_at_day_ago(settings_store.day_ago)
        date = timestamp_to_date(ts)
        self.label_date.setMinimumWidth(self.MINIMUN_WIDTH_LABEL)
        self.label_date.setAlignment(Qt.AlignCenter)
        self.label_date.setText(date)

    @staticmethod
    def live():
        settings_store.set_day_ago(0)

    def save_pdf(self):
        printer = QPrinter()
        painter = QPainter()
        defaut_path = 'I:\Programme mondon\Rapport production bobines'
        ts = timestamp_at_day_ago(settings_store.day_ago)
        defaut_name = "{} Rapport production bobines".format(timestamp_to_inverse_date(ts))
        file_names = QFileDialog.getSaveFileName(self,
                                                 caption='Enregistrer sous',
                                                 directory='{}\{}.pdf'.format(defaut_path, defaut_name),
                                                 filter="Fichiers pdf (*.pdf)")
        if not file_names[0]:
            return
        printer.setOutputFileName(file_names[0])
        printer.setOutputFormat(QPrinter.PdfFormat)
        printer.setPageMargins(10, 10, 10, 10, QPrinter.Point)
        painter.begin(printer)
        self.rapport.drawing(painter)
        painter.end()
        self.affiche_pdf(file_names[0])

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
