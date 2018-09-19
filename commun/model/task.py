# !/usr/bin/env python
# -*- coding: utf-8 -*-


class Task:

    def __init__(self, start, plan_prod=None, event=None):
        self.start = start
        self.plan_prod = plan_prod
        self.event = event

    def get_start(self):
        return self.start

    def __repr__(self):
        if self.plan_prod:
            return str(self.plan_prod)
        else:
            return str(self.event)
