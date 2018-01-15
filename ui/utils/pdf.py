# !/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtCore import QPointF
from PyQt5.QtGui import QPicture, QPainter
from PyQt5.QtPrintSupport import QPrinter


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


def save_pdf(widget, filename, preview=False):
    # Creation du printer
    printer = QPrinter()
    file_names = filename
    printer.setOutputFileName(file_names)
    printer.setOutputFormat(QPrinter.PdfFormat)
    printer.setPageMargins(10, 10, 10, 10, QPrinter.Point)

    # Calcul le ratio de redimensionnement
    page_width = printer.pageRect().width()
    page_height = printer.pageRect().height()
    widget_width = widget.width()
    widget_height = widget.height()
    ratio = min(page_width / widget_width, page_height / widget_height)

    # Calcul du positionnement
    pos_x = max(0, (page_width - ratio * widget_width) / 2)
    pos_y = max(0, (page_height - ratio * widget_height) / 2)

    # Render le widget dans une image QPicture pour stocker
    # les directives de dessin
    picture = QPicture()
    widget_painter = QPainter(picture)
    widget_painter.scale(ratio, ratio)
    widget.render(widget_painter)
    widget_painter.end()

    # Render la QPicture en utilisant le QPrinter
    picture_painter = QPainter()
    picture_painter.begin(printer)
    picture_painter.drawPicture(QPointF(pos_x, pos_y), picture)
    picture_painter.end()

    if preview:
        affiche_pdf(file_names)
