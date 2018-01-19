# !/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QApplication


class Application(QApplication):

    def __init__(self, argv=None):
        if argv is None:
            argv = []
        super(Application, self).__init__(argv)

app = Application()
