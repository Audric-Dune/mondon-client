# !/usr/bin/env python
# -*- coding: utf-8 -*-

from commun.utils.timestamp import timestamp_to_hour_little


class Event:

    def __init__(self, start, end, p_type, p_id, info=None, ensemble=None):
        self.p_id = p_id
        self.start = start
        self.end = end
        self.p_type = p_type
        self.info = info
        self.ensemble = ensemble

    def get_start(self):
        return self.start

    def __repr__(self):
        return "Event: start {}, end {}".format(timestamp_to_hour_little(self.start),
                                                timestamp_to_hour_little(self.end))
