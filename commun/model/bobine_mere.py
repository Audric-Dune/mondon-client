# !/usr/bin/env python
# -*- coding: utf-8 -*-


class BobineMere:

    def __init__(self, code=0, laize=0, length=0, color="", gr="0g"):
        self.code = code
        self.laize = int(laize)
        self.length = int(length)
        self.color = color
        self.gr = gr

    def get_value(self, value_name):
        if value_name == "code":
            return self.code
        if value_name == "laize":
            return self.laize
        if value_name == "length":
            return self.length
        if value_name == "color":
            return self.color
        if value_name == "gr":
            return self.gr
        return 0

    def __str__(self):
        return "REF {}({}, {}, {}m, {})".format(self.code,
                                                self.color.capitalize(),
                                                self.laize,
                                                self.length,
                                                self.gr)
