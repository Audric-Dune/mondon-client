# !/usr/bin/env python
# -*- coding: utf-8 -*-

from commun.ui.public.mondon_widget import MondonWidget


class BobineMere(MondonWidget):

    def __init__(self, parent=None, code=0, laize=0, lenght=0, color="", gr="0g"):
        super(BobineMere, self).__init__(parent=parent)
        self.code = code
        self.laize = int(laize)
        self.lenght = int(lenght)
        self.color = color
        self.gr = gr

    def __str__(self):
        return "REF {}({}, {}, {}m, {})".format(self.code,
                                                self.color.capitalize(),
                                                self.laize,
                                                self.lenght,
                                                self.gr)
