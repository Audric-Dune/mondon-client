# !/usr/bin/env python
# -*- coding: utf-8 -*-


class PerfoStore:
    def __init__(self):
        self.perfos = []

    def add_item(self, perfo):
        self.perfos.append(perfo)


perfo_store = PerfoStore()
