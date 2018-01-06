# !/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtCore import Qt, QRectF, QRect
from PyQt5.QtGui import QBrush, QColor, QPen, QPainterPath, QFont


def draw_rectangle(p, x, y, width, height, color):
    color = color.rgb_components
    p.fillRect(x, y, width, height, QColor(color[0], color[1], color[2]))


def draw_rectangle_radius(p, x, y, width, height, color, radius=0):
    color = color.rgb_components
    path = QPainterPath()
    path.addRoundedRect(QRectF(x, y, width, height), radius, radius)
    p.fillPath(path, QColor(color[0], color[1], color[2]))


def draw_text(p, x, y, width, height, color, align, font_size, text, bold=False, italic=False):
    pen = QPen(
        QBrush(Qt.SolidPattern),
        1.0,
        Qt.SolidLine,
        Qt.SquareCap,
        Qt.BevelJoin,
    )
    color = color.rgb_components
    pen.setColor(QColor(color[0], color[1], color[2]))
    p.setPen(pen)
    font = QFont("Arial Narrow")
    font.setPointSize(font_size)
    font.setBold(bold)
    font.setItalic(italic)
    p.setFont(font)
    if align == "D":
        qt_align = Qt.AlignRight
    elif align == "G":
        qt_align = Qt.AlignLeft
    else:
        qt_align = Qt.AlignCenter

    text_flag = qt_align | Qt.AlignVCenter | Qt.TextWordWrap
    text_size = p.fontMetrics().boundingRect(QRect(0, 0, width, height), text_flag, text)
    text_height = text_size.height()

    p.drawText(QRectF(x, y, width, text_height), text_flag, text)
    return text_height
