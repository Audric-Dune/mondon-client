# !/usr/bin/env python
# -*- coding: utf-8 -*-


class Event:

    def __init__(self, start, end, type, info=None):
        self.start = start
        self.end = end
        self.type = type
        self.info = info
