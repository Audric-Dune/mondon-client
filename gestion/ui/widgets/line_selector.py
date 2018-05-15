# !/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtCore import Qt

from commun.constants.colors import color_vert_fonce
from commun.ui.public.mondon_widget import MondonWidget


class LineSelector(MondonWidget):

    def __init__(self, parent=None):
        super(LineSelector, self).__init__(parent=parent)
        self.setFocusPolicy(Qt.ClickFocus)
        self.memo_button_press = 0
        self.setFocus()

    def mousePressEvent(self, e):
        self.memo_button_press += 1
        if self.memo_button_press > 1:
            self.clearFocus()
        super(LineSelector, self).mousePressEvent(e)

    def focusInEvent(self, e):
        self.memo_button_press = 0
        self.set_border(color=color_vert_fonce, size=1)
        super(LineSelector, self).focusInEvent(e)

    def focusOutEvent(self, e):
        self.set_border(color=color_vert_fonce, size=0)
        super(LineSelector, self).focusOutEvent(e)
