# !/usr/bin/env python
# -*- coding: utf-8 -*-


class Task:

    def __init__(self, start, end, plan_prod=None, event=None):
        self.start = start
        self.end = end
        self.plan_prod = plan_prod
        self.event = event
        self.index = None

    def get_start(self):
        return self.start

    def get_index(self):
        return self.index

    def __repr__(self):
        if self.plan_prod:
            return "Index: {} Plan production: {}".format(self.index, self.plan_prod)
        else:
            return str(self.event)
