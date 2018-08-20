# !/usr/bin/env python
# -*- coding: utf-8 -*-


class ReglageStore:
    def __init__(self):
        self.reglages = []

    def add_reglage(self, reglage):
        self.reglages.append(reglage)


reglage_store = ReglageStore()
