# !/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QApplication

from gestion.window.main_window import MainWindow


class Application(QApplication):

    def __init__(self, argv=None):
        if argv is None:
            argv = []
        super(Application, self).__init__(argv)
        self.main_window = MainWindow()
        self.main_window.show()


app = Application()
