# !/usr/bin/env python
# -*- coding: utf-8 -*-


class Event:

    def __init__(self, start, end, p_type, p_id, info=None):
        self.p_id = p_id
        self.start = start
        self.end = end
        self.p_type = p_type
        self.info = info

    def get_start(self):
        return self.start
