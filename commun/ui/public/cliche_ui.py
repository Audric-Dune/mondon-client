# !/usr/bin/env python
# -*- coding: utf-8 -*-


from PyQt5.QtGui import QPen, QPainter, QColor

from commun.ui.public.mondon_widget import QWidget
from commun.utils.drawing import draw_rectangle, draw_text
from commun.utils.color_cliche import get_color_cliche
from commun.utils.cliches import get_cliche_from_code
from commun.constants.colors import color_noir


class ClicheUi(QWidget):
    CLICHE_HEIGHT = 80

    def __init__(self, color, parent=None, bobine_selected=None, ech=1):
        super(ClicheUi, self).__init__(parent=parent)
        self.laize = bobine_selected.laize * bobine_selected.pose
        self.bobine_selected = bobine_selected
        self.ech = ech
        self.color = color
        self.cliche = self.get_cliche()
        self.setFixedSize(self.laize*self.ech, self.CLICHE_HEIGHT*self.ech)

    def get_cliche(self):
        for code_cliche in self.bobine_selected.codes_cliche:
            cliche = get_cliche_from_code(code_cliche)
            if self.color in cliche.colors:
                return cliche

    def paintEvent(self, e):
        p = QPainter(self)
        color = color_noir.rgb_components
        qcolor_gris = QColor(color[0], color[1], color[2])
        pen = QPen()
        pen.setColor(qcolor_gris)
        p.setPen(pen)
        self.draw(p)

    def draw_cliche(self, p):
        x = 0
        y = 0
        w = self.laize * self.ech - 1
        h = (self.CLICHE_HEIGHT - 1) * self.ech
        color = get_color_cliche(self.color)
        draw_rectangle(p, x, y, w, h, color=color, border_color=color_noir)

    def draw_text(self, p):
        x = 0
        y = -20
        w = self.laize * self.ech
        h = self.CLICHE_HEIGHT * self.ech
        font_size = 14 * self.ech
        text = self.cliche.code
        draw_text(p, x, y, w, h, color=color_noir, align="C", font_size=font_size, text=text)
        pose = self.bobine_selected.pose
        text = "({} pose)".format(pose) if pose == 1 else "({} poses)".format(pose)
        y = 10
        draw_text(p, x, y, w, h, color=color_noir, align="C", font_size=font_size, text=text)

    def draw(self, p):
        self.draw_cliche(p)
        self.draw_text(p)
