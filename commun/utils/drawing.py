# !/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtCore import Qt, QRectF, QRect, QPoint
from PyQt5.QtGui import QBrush, QColor, QPen, QPainterPath, QFont


def draw_rectangle(p, x, y, width, height, color, border_color=None, border_size=1):
    if not border_color:
        border_color = color
    color = color.rgb_components
    brush = QBrush(QColor(color[0], color[1], color[2]))
    p.setBrush(brush)
    border_color = border_color.rgb_components
    pen = QPen(QColor(border_color[0], border_color[1], border_color[2]))  # set lineColor
    pen.setWidth(border_size)  # set lineWidth
    p.setPen(pen)
    p.drawRect(x, y, width, height)


def draw_triangle(p, x, y, width, height, background_color, border_color, border_size=1, reverse=False):
    border_color = border_color.rgb_components
    pen = QPen(QColor(border_color[0], border_color[1], border_color[2]))  # set lineColor
    pen.setWidth(border_size)  # set lineWidth
    background_color = background_color.rgb_components
    brush = QBrush(QColor(background_color[0], background_color[1], background_color[2]))  # set fillColor
    p.setPen(pen)
    p.setBrush(brush)
    if reverse:
        p.drawPolygon(QPoint(x, y), QPoint(width/2+x, height+y), QPoint(width+x, y))
    else:
        p.drawPolygon(QPoint(x, height+y), QPoint(width/2+x, y), QPoint(width+x, height+y))


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
    text_height = text_size.height() if text_size.height() > height else height

    p.drawText(QRectF(x, y, width, text_height), text_flag, text)
    return text_height
