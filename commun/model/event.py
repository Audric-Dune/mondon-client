# !/usr/bin/env python
# -*- coding: utf-8 -*-


from commun.ui.public.mondon_widget import MondonWidget


class Event(MondonWidget):

    def __init__(self, start, end, type, parent=None, info=None):
        super(Event, self).__init__(parent=parent)
        self.start = start
        self.end = end
        self.type = type
        self.info = info
