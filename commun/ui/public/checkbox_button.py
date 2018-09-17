# !/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtCore import pyqtSignal

from commun.constants.stylesheets import check_box_off_stylesheet,\
    check_box_on_stylesheet,\
    check_box_disabled_stylesheet
from commun.ui.public.pixmap_button import PixmapButton


class CheckboxButton(PixmapButton):
    ON_CLICK_SIGNAL = pyqtSignal()

    def __init__(self, parent=None, is_check=True,
                 off_stylesheet=check_box_off_stylesheet,
                 on_stylesheet=check_box_on_stylesheet,
                 disbled_stylesheet=check_box_disabled_stylesheet,
                 img_path="commun/assets/images/white_check.png"):
        super(CheckboxButton, self).__init__(parent=parent)
        self.disabled = False
        self.enabled = True
        self.is_check = is_check
        self.img_path = img_path
        self.off_stylesheet = off_stylesheet
        self.on_stylesheet = on_stylesheet
        self.disbled_stylesheet = disbled_stylesheet
        self.flip_button()

    def flip_button(self):
        if self.is_check:
            self.removeImage()
            self.setStyleSheet(self.off_stylesheet)
            self.is_check = False
        else:
            self.addImage(self.img_path)
            self.setStyleSheet(self.on_stylesheet)
            self.is_check = True

    def setDisabled(self, p_bool):
        self.disabled = p_bool
        self.enabled = False if p_bool else True
        if p_bool:
            self.removeImage()
            self.setStyleSheet(self.disbled_stylesheet)

    def mouseReleaseEvent(self, *args, **kwargs):
        if self.enabled:
            self.flip_button()
            self.ON_CLICK_SIGNAL.emit()
