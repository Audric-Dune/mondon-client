from PyQt5.QtCore import Qt, QRectF
from PyQt5.QtGui import QBrush, QColor, QPen, QPainterPath


def draw_rectangle(p, x, y, width, height, color):
    p.fillRect(x, y, width, height, QColor(color[0], color[1], color[2]))


def draw_rectangle_radius(p, x, y, width, height, color):
    path = QPainterPath()
    path.addRoundedRect(QRectF(x, y, width, height), height/2, height/2)
    p.fillPath(path, QColor(color[0], color[1], color[2]))


def draw_text(p, x, y, width, height, color, align, font_size, text):
    pen = QPen(
        QBrush(Qt.SolidPattern),
        1.0,
        Qt.SolidLine,
        Qt.SquareCap,
        Qt.BevelJoin,
    )
    pen.setColor(QColor(color[0], color[1], color[2]))
    p.setPen(pen)
    font = p.font()
    font.setPointSize(font_size)
    p.setFont(font)
    if align == "D":
        qt_align = Qt.AlignRight
    elif align == "G":
        qt_align = Qt.AlignLeft
    else:
        qt_align = Qt.AlignCenter
    p.drawText(QRectF(x, y, width, height), qt_align | Qt.AlignVCenter, text)
