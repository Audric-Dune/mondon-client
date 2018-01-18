# !/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtCore import QEvent, pyqtSignal

from commun.constants.stylesheets import (
    check_box_off_stylesheet, check_box_on_stylesheet,
    check_box_disabled_stylesheet, )
from commun.ui.public.pixmap_button import PixmapButton


class CheckboxButton(PixmapButton):
    ON_CLICK_SIGNAL = pyqtSignal()

    def __init__(self, parent=None, is_check=True):
        super(CheckboxButton, self).__init__(parent=parent)
        self.disabled = False
        self.enabled = True
        self.installEventFilter(self)
        self.is_check = is_check
        self.img_path = "commun/assets/images/white_check.png"
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

    def setDisabled(self, bool):
        self.disabled = bool
        self.enabled = False if bool else True
        if bool:
            self.removeImage()
            self.setStyleSheet(check_box_disabled_stylesheet)

    def eventFilter(self, src, event):
        if event.type() == QEvent.MouseButtonRelease and self.enabled:
            self.flip_button()
            self.ON_CLICK_SIGNAL.emit()
            return True
        return False
