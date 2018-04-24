# !/usr/bin/env python
# -*- coding: utf-8 -*-


class BobineMere:

    def __init__(self, code=0, laize=0, lenght=0, color="", gr="0g"):
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
