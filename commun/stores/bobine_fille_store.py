# !/usr/bin/env python
# -*- coding: utf-8 -*-


class BobineFilleStore:
    def __init__(self):
        self.bobines = []

    def add_bobine(self, bobine):
        self.bobines.append(bobine)

    def get_bobine(self, code):
        for bobine in self.bobines:
            if bobine.code == code:
                return bobine

bobine_fille_store = BobineFilleStore()
