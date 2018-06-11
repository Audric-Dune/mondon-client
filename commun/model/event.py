# !/usr/bin/env python
# -*- coding: utf-8 -*-


class Event:

    def __init__(self, start, end, p_type, info=None):
        self.start = start
        self.end = end
        self.p_type = p_type
        self.info = info
