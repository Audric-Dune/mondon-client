# !/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.Qt import Qt


def focus_window(window):
    """
    Focus une window
    :param window: La window a focus
    """
    window.setWindowState(window.windowState() & ~Qt.WindowMinimized | Qt.WindowActive)
    window.raise_()
    window.activateWindow()
