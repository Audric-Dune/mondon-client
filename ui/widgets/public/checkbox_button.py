# !/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtCore import QEvent, pyqtSignal
from ui.widgets.public.pixmap_button import PixmapButton
from constants.stylesheets import check_box_off_stylesheet, check_box_on_stylesheet


class CheckboxButton(PixmapButton):
    ON_CLICK_SIGNAL = pyqtSignal()

    def __init__(self, parent=None, is_check=True):
        super(CheckboxButton, self).__init__(parent=parent)
        self.installEventFilter(self)
        self.is_check = is_check
        self.img_path = "assets/images/white_check.png"
        self.flip_button()

    def flip_button(self):
        if self.is_check:
            self.removeImage()
            self.setStyleSheet(check_box_off_stylesheet)
            self.is_check = False
        else:
            self.addImage(self.img_path)
            self.setStyleSheet(check_box_on_stylesheet)
            self.is_check = True

    def eventFilter(self, src, event):
        if event.type() == QEvent.MouseButtonRelease:
            self.flip_button()
            self.ON_CLICK_SIGNAL.emit()
            return True
        return False
