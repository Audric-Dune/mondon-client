# !/usr/bin/env python
# -*- coding: utf-8 -*-


class Task:

    def __init__(self, start, end, plan_prod=None, event=None, day_ago=None):
        self.start = start
        self.end = end
        self.plan_prod = plan_prod
        self.event = event
        self.index = None
        self.day_ago = day_ago

    def get_start(self):
        return self.start

    def get_index(self):
        return self.index - (self.day_ago*100)

    def __repr__(self):
        if self.plan_prod:
            return "Index: {}, Day_ago: {}, Plan production: {}".format(self.index, self.day_ago, self.plan_prod)
        else:
            return str(self.event)
